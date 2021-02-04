import pandas as pd
from datetime import datetime


def _save_partitions(df, source='tdem'):
    today = datetime.now().strftime('%Y-%m-%d')
    hr_min = datetime.now().strftime('%H:%M')
    df.to_csv(f's3://data-{source}/raw/{today}/{hr_min}/{source}-vaccine-supply.csv', index=False)
    df.to_csv(f's3://data-{source}/raw/latest/{source}-vaccine-supply.csv', index=False)

def main(event, context):
    df = pd.read_csv("https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv")
    _save_partitions(df)
    msg = f"{len(df)} records moved to S3 at {today} {hr_min}"
    print(msg)
    response = {
        "statusCode": 200,
        "body": msg
    }
    return response

# main("","")