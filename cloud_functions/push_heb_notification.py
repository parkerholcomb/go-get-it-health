import pandas as pd
from twilio.rest import Client
from geopy.distance import geodesic
import boto3
import json
from geopy.geocoders import Nominatim

secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
secret = json.loads(get_secret_value_response['SecretString'])
client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])

def _get_current_prev_dfs():
    s3_bucket = boto3.resource('s3').Bucket('data-heb')
    raw_keys = [obj.key for obj in s3_bucket.objects.all() if not obj.key.startswith('raw/latest')]
    prev_df = pd.read_json(f"s3://data-heb/{raw_keys[-2]}")
    current_df = pd.read_json(f"s3://data-heb/{raw_keys[-1]}")
    return [prev_df, current_df]

def _get_filtered_location_updates(zip_, max_distance = 100):
    zip_lat_lng = _geocode_zip(zip_)
    
    prev_df,current_df = _get_current_prev_dfs()
    current_df = current_df[current_df['openAppointmentSlots'] > 0]
    prev_df[prev_df['name'].isin(current_df['name'])]

    # # add some random availability
    # for i in [5, 24, 45, 110, 127, 200]:
    #     current_df['openAppointmentSlots'][i] = 100
    # # and have one be the the same as the last
    # prev_df['openAppointmentSlots'][5] = 100
    
    updates = []
    for idx in current_df.index:
        if current_df['openAppointmentSlots'][idx] > prev_df['openAppointmentSlots'][idx]:
            updates.append(idx)
    df = current_df[current_df.index.isin(updates)]
    df['lat_lng'] = df.apply(_geocode, axis=1)
    df['miles_away'] = df['lat_lng'].apply(lambda location_lat_lng: int(geodesic(location_lat_lng, zip_lat_lng).miles))
    df = df[df['miles_away'] < max_distance].sort_values(by='miles_away')
    print(df)
    return df
    
def _geocode_zip(zip_ = "78741"):
    if zip_ == '78741':
        return '30.231252,-97.716'
    else:
        geolocator = Nominatim(user_agent="vtx")
        location = geolocator.geocode(zip_)
        return f"{location.latitude},{location.longitude}"

def _geocode(row):
    return f"{row['latitude']},{row['longitude']}"
    
def _generate_body(zip_ = "78741"):
    df = _get_filtered_location_updates(zip_)
    body = ['New availability detected at HEB:\n']
    for idx in df.index:
        body.append(f"💉 {df.loc[idx]['name']} has {df.loc[idx]['openAppointmentSlots']} appoinments, {df.loc[idx]['miles_away']} miles away")
    body.append('\nVisit https://vaccine.heb.com/scheduler to schedule. #goandgetgetit')
    return '\n'.join(body)

def send_msg(zip_, to_):
    body = _generate_body(zip_)
    from_ = "+1 512 488 6383"
    msg = client.messages.create(body=body,from_=from_,to=to_)
    resp = f"Message sent {from_} to {to_} with locations -- {msg.sid}"
    print(resp)
    return resp

def main(event, context): 
    send_msg('78741', "+1 713 824 8581") # parker
    send_msg('78741', "‭+1 585 329 4284‬") # steve denero
    send_msg('78741', "‭‭+1 817 637 2734‬") # scott wynd
    
    response = {
        "statusCode": 200,
        "body": 'success'
    }
    return response


if __name__ == "__main__":
    main("","")