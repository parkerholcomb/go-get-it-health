import pandas as pd
from twilio.rest import Client
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import boto3
import json
import requests
from datetime import datetime

if __name__ == "__main__":
    main("","")
    print("DEBUG MODE - WILL NOT SEND SMS")
    ENV = "dev"
else:
    ENV = "stage"

secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
secret = json.loads(get_secret_value_response['SecretString'])
client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])

s3_bucket = boto3.resource('s3').Bucket('data-heb')

# todo put this in s3
with open('tx_zip_geo_cache.json', 'r') as f:
    zip_geo_cache = json.load(f)

## first grab and save updated data
def fetch_and_save_data(source='heb'):
    response = requests.get('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json')
    data = response.json()['locations']
    s3_bucket.Object(key=f"raw/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H:%M')}/{source}-vaccine-supply.json").put(Body=json.dumps(data))
    s3_bucket.Object(key=f"raw/latest/{source}-vaccine-supply.json").put(Body=json.dumps(data))
    print(f"{source} data updated")

## then all the notifications logic
def _get_current_prev_dfs():
    raw_keys = [obj.key for obj in s3_bucket.objects.all() if not obj.key.startswith('raw/latest')]
    prev_df = pd.read_json(f"s3://data-heb/{raw_keys[-2]}")
    current_df = pd.read_json(f"s3://data-heb/{raw_keys[-1]}")
    return [prev_df, current_df]

def _get_filtered_location_updates(zip_, max_distance = 100):
    prev_df,current_df = _get_current_prev_dfs()
    current_df = current_df[current_df['openAppointmentSlots'] > 1]
    prev_df = prev_df[prev_df['name'].isin(current_df['name'])] # todo: handle new locations better

    # # add some random availability for testing
    # for i in [5, 24, 45, 110, 127, 200]:
    #     current_df['openAppointmentSlots'][i] = 100
    # # and have one be the the same as the last
    # prev_df['openAppointmentSlots'][5] = 100
    
    # generate updates...i.e. did new - old increase?
    updates = []
    for idx in current_df.index:
        if current_df['openAppointmentSlots'][idx] > prev_df['openAppointmentSlots'][idx]:
            updates.append(idx)
    df = current_df[current_df.index.isin(updates)]
    
    # then let's geocode it 
    df['lat_lng'] = df.apply(lambda row: f"{row['latitude']},{row['longitude']}", axis=1)
    df['miles_away'] = df['lat_lng'].apply(lambda location_lat_lng: int(geodesic(location_lat_lng, _geocode_zip(zip_)).miles))
    df = df[df['miles_away'] < max_distance].sort_values(by='miles_away')
    print(df)
    return df
    
def _geocode_zip(zip_str):
    zip_str = str(zip_str)
    if zip_str in zip_geo_cache.keys():
        return zip_geo_cache[zip_str]
    else:
        geolocator = Nominatim(user_agent="vtx")
        location = geolocator.geocode(zip_str)
        return f"{location.latitude},{location.longitude}"
    
def _generate_body(df, zip_):
    body = []
    for idx in df.index:
        body.append(f"💉 {df.loc[idx]['name']} has {df.loc[idx]['openAppointmentSlots']} appoinments, {df.loc[idx]['miles_away']} miles away")
    body.append(f'\nVisit https://vaccine.heb.com/scheduler?q={zip_} to schedule. #goandgetgetit')
    return '\n'.join(body)

def send_msg(to_, zip_, radius = 100):
    locations_df = _get_filtered_location_updates(zip_, radius)
    if len(locations_df) > 0:
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
    else: 
        print(f'no updates within 100 miles for {zip_}')

def process_push_notifications():
    to_df = pd.read_csv(f"./to_list-{ENV}.csv")
    print(to_df)
    for i in to_df.index:
        send_msg( to_df['to_'][i], to_df['zip_'][i], to_df['radius'])

def main(event, context): 
    print(f"ENV: {ENV}")
    fetch_and_save_data() #todo whether to save or not
    process_push_notifications() # dev prints to consolve
    return 'success'


# also todo : don't reload prev_current df for each person. 