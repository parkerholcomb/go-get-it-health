import boto3
import json
from datetime import datetime
import requests
import pandas as pd

class Fetcher:

    def __init__(self, source):
        if source == 'heb':
            self.fetch_heb()
        elif source == 'tdem':
            self.fetch_tdem()
    
    now_partition_str = f"{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H:%M')}"

    @staticmethod
    def fetch_heb(source = 'heb'):
        response = requests.get('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json')
        data = response.json()['locations']
        s3_bucket = boto3.resource('s3').Bucket(f'ggi-data-{source}')
        s3_bucket.Object(key=f"raw/{Fetcher.now_partition_str}/{source}-vaccine-supply.json").put(Body=json.dumps(data))
        s3_bucket.Object(key=f"raw/latest/{source}-vaccine-supply.json").put(Body=json.dumps(data))
        print(f"fetched latest from {source}")
    
    @staticmethod    
    def fetch_tdem(source = 'tdem'):
        df = pd.read_csv("https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv")
        df.to_csv(f's3://ggi-data-{source}/raw/{Fetcher.now_partition_str}/{source}-vaccine-supply.csv', index=False)
        df.to_csv(f's3://ggi-data-{source}/raw/latest/{source}-vaccine-supply.csv', index=False)
        print(f"fetched latest from {source}")