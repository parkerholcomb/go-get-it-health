import requests
import boto3
from datetime import datetime
import json

headers = {
    'Referer': 'https://vaccine.heb.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
}

def main(event, context):
    response = requests.get('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json', headers=headers)
    data = response.json()['locations']
    s3_bucket = boto3.resource("s3").Bucket("data-heb")
    fname = "heb-vaccine-locations.json"
    raw_key = f"raw/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H:%M')}/{fname}"
    s3_bucket.Object(key=raw_key).put(Body=json.dumps(data))
    s3_bucket.Object(key=f"raw/latest/{fname}").put(Body=json.dumps(data))
    msg = "captured from heb"
    print(msg)
    response = {
        "statusCode": 200,
        "body": msg
    }
    return response

# main("","")