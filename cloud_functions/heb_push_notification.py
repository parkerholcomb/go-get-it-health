import pandas as pd
from twilio.rest import Client
from geopy.distance import geodesic
import boto3
import json

secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
secret = json.loads(get_secret_value_response['SecretString'])
client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])

def _get_df():
    s3_bucket = boto3.resource('s3').Bucket('data-heb')
    raw_keys = [obj.key for obj in s3_bucket.objects.all() if not obj.key.startswith('raw/latest')]
    prev_df = pd.read_json(f"s3://data-heb/{raw_keys[-2]}")
    current_df = pd.read_json(f"s3://data-heb/{raw_keys[-1]}")

    # # add some random availability
    # for i in [5, 24, 45, 110, 127, 200]:
    #     current_df['openAppointmentSlots'][i] = 100
    # # and have one be the the same as the last
    # prev_df['openAppointmentSlots'][5] = 100
    
    current_df = current_df[current_df['openAppointmentSlots'] > 0]
    prev_df[prev_df['name'].isin(current_df['name'])]

    updates = []
    for idx in current_df.index:
        if current_df['openAppointmentSlots'][idx] > prev_df['openAppointmentSlots'][idx]:
            updates.append(idx)

    df = current_df[current_df.index.isin(updates)]
    df['lat_lng'] = df.apply(_geocode, axis=1)
    df['miles_away'] = df['lat_lng'].apply(_get_miles_away)
    return df.sort_values(by='miles_away')
    
def _geocode(row):
    return f"{row['latitude']},{row['longitude']}"

def _get_miles_away(lat_lng_a, lat_lng_b = '30.231252,-97.716'):
    return int(geodesic(lat_lng_a, lat_lng_b).miles)
    
def _generate_body(df):
    body = ['New availability detected at HEB:\n']
    for idx in df.index:
        body.append(f"💉 {df.loc[idx]['name']} has {df.loc[idx]['openTimeslots']} timeslots, {df.loc[idx]['openAppointmentSlots']} appoinments, {df.loc[idx]['miles_away']} miles away")
    body.append('\nVisit https://vaccine.heb.com/scheduler to schedule')
    return '\n'.join(body)

def main(event, context): 
    df = _get_df()
    from_ = "+1 512 488 6383"
    to_ = "+1 713 824 8581"
    body = _generate_body(df)
    msg = client.messages.create(body=body,from_=from_,to=to_)
    resp = f"Message sent {from_} to {to_} with {len(df)} locations -- {msg.sid}"
    print(resp)
    response = {
        "statusCode": 200,
        "body": resp
    }
    return response


if __name__ == "__main__":
    main("","")