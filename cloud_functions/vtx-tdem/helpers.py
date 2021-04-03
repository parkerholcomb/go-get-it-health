import json
from twilio.rest import Client
import boto3
from geopy.geocoders import Nominatim

# class Subscribers:
#     def __init__(self, env = 'stage'):
#         self.subscribers = self.load_subscribers(env)

#     def load_subscribers(self, env):
#         s3_bucket = boto3.resource('s3').Bucket('vtx-subscriptions')
#         raw_keys = [obj.key for obj in s3_bucket.objects.all() if obj.key.startswith(env)]
#         subscriptions = []
#         for raw_key in raw_keys:
#             try:
#                 key = raw_key.split("/")[1]
#                 subscriptions.append(
#                     dict(
#                         to_ = key.split("#")[0],
#                         zip_ = key.split("#")[1].split("+")[0],
#                         radius = 200 #int(key.split("#")[1].split("+")[1])
#                     )
#                 )
#             except: 
#                 print(raw_key)

#         return subscriptions

# class Messager:
#     def __init__(self, env = 'dev'):
#         self.twilio_client = self._load_twilio_client()
#         self.env = env
#         self.from_ = self.from_number()
        

#     def from_number(self):
#         if self.env == 'dev':
#             return "+1 512 489 9353"
#         elif self.env == 'stage':
#             return "+1 512 488 6383"
#         elif self.env == 'prod':
#             return "+1 512 488 6383"
    
#     @staticmethod
#     def _load_twilio_client():
#         secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
#         get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
#         secret = json.loads(get_secret_value_response['SecretString'])
#         client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])
#         return client

#     def send_sms(self, to_, body):
#         if self.env == 'test':
#             print(f"Message sent {self.from_} to {to_} -- ENV=DEV:\n", body)
#             return 
#         msg = self.twilio_client.messages.create(body=body,from_=self.from_,to=to_)
#         resp = f"Message sent {self.from_} to {to_} with locations -- {msg.sid}"
#         print(resp)

# class GeoZipCache:
#     def __init__(self):
#         self.zip_geo_cache = self._load_zip_geo_cache()

#     @staticmethod
#     def _load_zip_geo_cache():
#         s3_bucket = boto3.resource('s3').Bucket('vtx-public')
#         data = json.load(s3_bucket.Object(key='tx_zip_geo_cache.json').get()['Body'])
#         return data

#     def geocode_zip(self, zip_str):
#         zip_str = str(zip_str)
#         zip_str = zip_str.strip()
#         zip_str = zip_str.split("-")[0]
#         if zip_str in self.zip_geo_cache.keys():
#             return self.zip_geo_cache[zip_str]
#         else:
#             # geolocator = Nominatim(user_agent="vtx")
#             # location = geolocator.geocode(zip_str)
#             # return f"{location.latitude},{location.longitude}"
#             return 'unknown'