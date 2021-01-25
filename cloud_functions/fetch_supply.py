import requests
import pandas as pd
from datetime import datetime, timedelta
import time

headers = {
    'authority': 'services5.arcgis.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://tdem.maps.arcgis.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b',
    'accept-language': 'en-US,en;q=0.9',
    'if-none-match': 'sd1949_-2034662753',
    'if-modified-since': 'Fri, 22 Jan 2021 12:16:32 GMT',
}

params = (
    ('f', 'json'),
    ('where', '1=1'),
    ('returnGeometry', 'true'),
    ('spatialRel', 'esriSpatialRelIntersects'),
    ('outFields', '*'),
    ('maxRecordCountFactor', '4'),
    ('outSR', '102100'),
    ('resultOffset', '0'),
    ('resultRecordCount', '8000'),
    ('cacheHint', 'true'),
    ('quantizationParameters', '{"mode":"view","originPosition":"upperLeft","tolerance":1.0583354500042332,"extent":{"xmin":-11864749.745014807,"ymin":2986125.9341450464,"xmax":-10435895.933896504,"ymax":4355735.017881977,"spatialReference":{"wkid":102100,"latestWkid":3857}}}'),
)

def _format_date(date_str = '01/01/2020'):
    try: 
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        # hmm whats the most accurate here? just call it today? H
        # Well whatever it is, a "false oversupply" (and then calling) is better than missing one
        return (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

def main(event, context):
    response = requests.get('https://services5.arcgis.com/Rvw11bGpzJNE7apK/arcgis/rest/services/VaccinesPublic_gdb/FeatureServer/0/query', headers=headers, params=params)
    data = response.json()['features']
    locations = [d['attributes'] for d in data]
    df = pd.DataFrame(locations)
    df = df.drop(columns=['OBJECTID','RemoveRecord'])
    df.columns = map(str.lower, df.columns)
    df['fetched_at'] = str(int(time.time()))
    df['last_update'] = df['last_update_vac'].apply(_format_date)
    today = datetime.now().strftime('%Y-%m-%d')
    hr_min = datetime.now().strftime('%H:%M')
    df.to_csv(f's3://vaccinate-texas/{today}/{hr_min}/vaccine-supply.csv', index=False, sep ='\t')
    df.to_csv(f's3://vaccinate-texas/latest/vaccine-supply.csv', index=False, sep ='\t')
    msg = f"{len(df)} records moved to S3 at {today} {hr_min}"
    print(msg)
    response = {
        "statusCode": 200,
        "body": msg
    }
    return response

