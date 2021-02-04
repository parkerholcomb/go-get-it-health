import requests
import boto3
from datetime import datetime
import json

def _save_partitions(data, source='heb'):
    s3_bucket = boto3.resource("s3").Bucket("data-{source}")
    today = datetime.now().strftime('%Y-%m-%d')
    hr_min = datetime.now().strftime('%H:%M')
    s3_bucket.Object(key=f"raw/{today}/{hr_min}/{source}-vaccine-supply.json").put(Body=json.dumps(data))
    s3_bucket.Object(key=f"raw/latest/{source}-vaccine-supply.json").put(Body=json.dumps(data))
    
def _fetch_data():
    response = requests.get('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json')
    return response.json()['locations']

def main(event, context):
    data = _fetch_data()
    _save_partitions(data)
    msg = "captured from heb"
    print(msg)
    response = {
        "statusCode": 200,
        "body": msg
    }
    return response

# main("","")