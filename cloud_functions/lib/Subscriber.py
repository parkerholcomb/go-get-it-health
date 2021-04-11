import boto3
import json
import time
from .GeoZipCache import GeoZipCache
import os

class Subscriber:

    default_radius = 50

    def __init__(self):
        self.env = os.environ.get('DEPLOY_STAGE')
        self.bucket_name = 'ggi-subscriptions'

    def _get_radius(self, key):
        if self.env in ['dev', 'staging']:
            return 100
        else: 
            return int(key.split("+")[-1])

    def load_subscribers(self):
        s3_bucket = boto3.resource('s3').Bucket(self.bucket_name)
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
        s3_bucket = boto3.resource('s3').Bucket(self.bucket_name)
        subscription_key = f"{self.env}/{phone}#{zip_}+{radius}"
        s3_bucket.Object(key=subscription_key).put(Body=json.dumps(data))
        print("subscription added:", subscription_key)
        return f"subscription_key {subscription_key} added"