import pandas as pd
from twilio.rest import Client
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import boto3
import json
from datetime import datetime

ENV = "stage"

secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
secret = json.loads(get_secret_value_response['SecretString'])
client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])

s3_bucket = boto3.resource('s3').Bucket('data-tdem')

with open('tx_zip_geo_cache.json', 'r') as f:
    zip_geo_cache = json.load(f)

## first grab and save updated data
def fetch_and_save_data(source='tdem'):
    df = pd.read_csv("https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv")
    df.to_csv(f"s3://data-{source}/raw/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H:%M')}/{source}-vaccine-supply.csv", index=False)
    df.to_csv(f"s3://data-{source}/raw/latest/{source}-vaccine-supply.csv", index=False)
    print("tdem data saved")

## then lets do the notification logic
def _get_current_prev_dfs(source = 'tdem'):
    raw_keys = [obj.key for obj in s3_bucket.objects.all() if obj.key.startswith('raw') and ~obj.key.startswith('raw/latest')]
    prev_df = pd.read_csv(f"s3://data-{source}/{raw_keys[-2]}")
    current_df = pd.read_csv(f"s3://data-{source}/{raw_keys[-1]}")
    return [prev_df, current_df]

def _get_filtered_location_updates(zip_, max_distance = 100):
    print(type(zip_), zip_, _geocode_zip(zip_))
    prev_df, current_df = _get_current_prev_dfs()
    current_df = current_df[current_df['VACCINES_AVAILABLE'] > 0]
    current_df['lat_lng'] = current_df['ZIP'].apply(_geocode_zip)
    current_df['miles_away'] = current_df['lat_lng'].apply(_miles_away, args=(_geocode_zip(zip_),) )
    current_df = current_df[current_df['miles_away'] < max_distance]
    print(current_df)
    prev_df = prev_df[prev_df['NAME'].isin(current_df['NAME'])]

    # # add some random availability for testing
    # for i in [777, 616, 1674]:
    #     current_df['VACCINES_AVAILABLE'][i] = 100
    # # and have one be the the same as the last
    # prev_df['VACCINES_AVAILABLE'][5] = 100
    
    # generate updates...i.e. did new - old increase?
    updates = []
    for idx in current_df.index:
        if current_df['VACCINES_AVAILABLE'][idx] > prev_df['VACCINES_AVAILABLE'][idx]:
            print(idx)
            updates.append(idx)
    df = current_df[current_df.index.isin(updates)].sort_values(by='miles_away')
    print(df)
    return df

def _geocode_zip(zip_str):
    zip_str = str(zip_str)
    if zip_str in zip_geo_cache.keys():
        return zip_geo_cache[zip_str]
    else:
        ## todo persist to tx_zip_geo_cache.json
        # geolocator = Nominatim(user_agent="vtx")
        # location = geolocator.geocode(zip_str)
        # return f"{location.latitude},{location.longitude}"
        return '0'

def _miles_away(lat_lng_a, lat_lng_b):
    try:
        return int(geodesic(lat_lng_a, lat_lng_b).miles)
    except:
        return 9999

def _generate_body(df, zip_):
    body = ['New availability within 100 miles:\n']
    for idx in df.index:
        body.append(f"💉 {df.loc[idx]['NAME']} has {df.loc[idx]['VACCINES_AVAILABLE']} vaccines available, {df.loc[idx]['miles_away']} miles away")
    body.append(f'\nVisit vaccinatetexas.org/?q={zip_} for more information. Now #goandgetgetit')
    return '\n'.join(body)

def send_msg(zip_, to_):
    locations_df = _get_filtered_location_updates(zip_)
    if len(locations_df) == 0:
        print(f'no updates within 100 miles for {zip_}')
        return

    body = _generate_body(locations_df, zip_)
    from_ = "+1 512 488 6383"
    if ENV == 'dev':
        print(body)
        resp = f"Message sent {from_} to {to_} with locations -- ENV=DEV"
    elif ENV in ['stage','prod']: 
        msg = client.messages.create(body=body,from_=from_,to=to_)
        resp = f"Message sent {from_} to {to_} with locations -- {msg.sid}"
        print(resp)
    return resp
    
def process_push_notifications():
    if ENV == 'dev': 
        print("DEBUG MODE - WILL NOT SEND SMS")
        to_df = pd.read_csv("./to_list-dev.csv")
    else:
        to_df = pd.read_csv("./to_list-prod.csv")
    print(to_df)
    for i in to_df.index:
        send_msg(to_df['zip_'][i], to_df['to_'][i])

def main(event, context): 
    fetch_and_save_data()
    process_push_notifications()
    return 'success'


if __name__ == "__main__":
    main("","")