import json
import boto3
import pandas as pd
from twilio.rest import Client
import requests
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

class Fetcher:
    def __init__(self, fetch = True):
        self.source = 'heb'
        self.s3_bucket = boto3.resource('s3').Bucket('data-heb')
        if fetch:
            self.fetch_latest()
        self.prev_df, self.current_df = self.get_current_prev_dfs()
        
    def get_current_prev_dfs(self):
        raw_keys = [obj.key for obj in self.s3_bucket.objects.all() if not obj.key.startswith('raw/latest')]
        prev_df = pd.read_json(f"s3://data-heb/{raw_keys[-2]}")
        current_df = pd.read_json(f"s3://data-heb/{raw_keys[-1]}")
        return [prev_df, current_df]

    def fetch_latest(self):
        response = requests.get('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json')
        data = response.json()['locations']
        self.s3_bucket.Object(key=f"raw/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H:%M')}/{self.source}-vaccine-supply.json").put(Body=json.dumps(data))
        self.s3_bucket.Object(key=f"raw/latest/{self.source}-vaccine-supply.json").put(Body=json.dumps(data))
        print(f"{self.source} data updated")
        return pd.DataFrame(data)
    

class Notifier:

    def __init__(self, source, env = 'dev'):
        self.env = 'dev'
        self.source = source
        self.s3_bucket = boto3.resource('s3').Bucket('data-heb')
        self.current_df, self.prev_df = Fetcher().get_current_prev_dfs()
        self.twilio_client = self._load_twilio_client()
        self.from_ = "+1 512 488 6383"
        self.zip_geo_cache = self._load_zip_geo_cache()
        self.subscribers = self.load_subscribers()
        self.geocode_dfs()

    def geocode_dfs(self):
        self.current_df['lat_lng'] = self.current_df.apply(lambda row: f"{row['latitude']},{row['longitude']}", axis=1)
        self.prev_df['lat_lng'] = self.prev_df.apply(lambda row: f"{row['latitude']},{row['longitude']}", axis=1)
    
    def load_subscribers(self):
        return pd.read_csv(f"./to_list-{self.env}.csv")
    
    @staticmethod
    def _load_zip_geo_cache():
        # todo: put this in s3
        with open('tx_zip_geo_cache.json', 'r') as f:
            zip_geo_cache = json.load(f)
        return zip_geo_cache

    @staticmethod
    def _load_twilio_client():
        secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
        get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
        secret = json.loads(get_secret_value_response['SecretString'])
        client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])
        return client

    def geocode_zip(self, zip_str):
        zip_str = str(zip_str)
        if zip_str in self.zip_geo_cache.keys():
            return self.zip_geo_cache[zip_str]
        else:
            geolocator = Nominatim(user_agent="vtx")
            location = geolocator.geocode(zip_str)
            return f"{location.latitude},{location.longitude}"

    def get_filtered_location_updates(self, zip_, radius = 100):
        old_df, new_df = self.prev_df, self.current_df
        # first filter out locations with 0 appointments
        new_df = new_df[new_df['openAppointmentSlots'] > 1]
        # then filter out locations outside max radius
        zip_lat_lng = self.geocode_zip(zip_)
        new_df['miles_away'] = new_df['lat_lng'].apply(lambda location_lat_lng: int(geodesic(location_lat_lng, zip_lat_lng).miles))
        new_df = new_df[new_df['miles_away'] < radius].sort_values(by='miles_away')
        # then filter down old_df so we're apples to apples
        old_df = old_df[old_df['name'].isin(new_df['name'])]
        
        # now find the delta, and return updates
        new_df['appts_delta'] = new_df['openAppointmentSlots'] - old_df['openAppointmentSlots']
        return new_df[new_df['appts_delta'] > 1]

    @staticmethod
    def _generate_body(df):
        body = []
        for idx in df.index:
            body.append(f"💉 {df.loc[idx]['name']} has {df.loc[idx]['openAppointmentSlots']} appoinments, {df.loc[idx]['miles_away']} miles away")
        # todo save the zip of the first record
        body.append(f'\nVisit https://vaccine.heb.com/scheduler?q=todo to schedule. #goandgetgetit')
        return '\n'.join(body)

    def send_sms(self, to_, body):
        if self.env == 'dev':
            print(f"Message sent {self.from_} to {to_} -- ENV=DEV:\n", body)
            return 
    
        msg = self.twilio_client.messages.create(body=body,from_=self.from_,to=to_)
        resp = f"Message sent {self.from_} to {to_} with locations -- {msg.sid}"
        print(resp)

    def process_push_notifications(self):
        for i in range(len(self.subscribers)):
            person = self.subscribers.loc[i]
            updates = self.get_filtered_location_updates(person['zip_'], person['radius'])
            if len(updates) > 0:
                body = self._generate_body(updates)
                self.send_sms(person['to_'], body)
        return i