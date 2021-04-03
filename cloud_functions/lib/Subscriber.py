import boto3
import json
import time
from .GeoZipCache import GeoZipCache

class Subscriber:

    default_radius = 50

    def __init__(self, env = 'stage'):
        self.env = env

    def _get_radius(self, key):
        if self.env == 'dev':
            return 200
        else: 
            return int(key.split("+")[-1])

    def load_subscribers(self):
        s3_bucket = boto3.resource('s3').Bucket('vtx-subscriptions')
        raw_keys = [obj.key for obj in s3_bucket.objects.all() if obj.key.startswith(f"{self.env}/+")]
        subscriptions = []
        geo_zip_cache = GeoZipCache()
        for raw_key in raw_keys:
            try:
                key = raw_key.split("/")[1]
                phone = key.split("#")[0]
                zip_ = key.split("#")[1].split("+")[0]
                subscriptions.append(
                    dict(
                        phone = phone,
                        zip_ = zip_,
                        lat_lng = geo_zip_cache.geocode_zip(zip_),        
                        radius = self._get_radius(key)
                    )
                )
            except: 
                print(raw_key)

        return subscriptions

    def add_subscriber(self, phone, zip_, msgContent):
        radius = self.default_radius
        data = dict(
            phone = phone,
            zip_ = zip_,
            radius = radius,
            created = int(time.time()),
            meta = msgContent
        )
        s3_bucket = boto3.resource('s3').Bucket('vtx-subscriptions')
        subscription_key = f"{self.env}/{phone}#{zip_}+{radius}"
        s3_bucket.Object(key=subscription_key).put(Body=json.dumps(data))
        print("subscription added:", subscription_key)
        return f"subscription_key {subscription_key} added"