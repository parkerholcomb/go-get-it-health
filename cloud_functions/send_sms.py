# from helpers import get_secret
from twilio.rest import Client
import pandas as pd
from datetime import datetime, timedelta
import json
import boto3

secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
secret = json.loads(get_secret_value_response['SecretString'])
client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])
    
def _find_nearby_supply(zip_code, last_n_days=2):
    df = pd.read_csv("s3://vaccinate-texas/latest/vaccine-supply.csv", delimiter='\t')
    print(df)
    df['zip'] = df['zip'].astype(str)
    df = df[df['zip'].apply(lambda x: x.startswith(zip_code[0:3]))] # this could get updated to geodesic distance
    df = df[df['total_available'].apply(lambda x: x > 0)]
    df = df[df['last_update'] > (datetime.now() - timedelta(days=last_n_days)).strftime('%Y-%m-%d')]
    df = df.sort_values(by='last_update_vac', ascending=False) #tbd on this being the best format
    df = df[['name','type','address','city','zip','total_available','total_shipped','publicphone','last_update']]
    return df

def _top_n(df, n=5):
    df = df.sort_values(by='total_available', ascending=False)[['name','total_available']].head(n).reset_index()
    top_n = []
    for i in range(0,n):
        top_n.append(f"{df.loc[i]['total_available']} doses @ {df.loc[i]['name'].title()}")
    return '\n'.join(top_n)

def _generate_body(zip_code):
    df = _find_nearby_supply(zip_code)
    url = f"http://www.vaccinatetexas.org.s3-website-us-east-1.amazonaws.com/availability/{zip_code}.html"
    body = '\n'.join(
        [
            f"COVID Vaccine updates for {zip_code} residents. In the last two days, {df.total_available.sum()} COVID vaccine became "
            f"available across {len(df)} locations in your area.",
            "\nTop Locations include:",
            _top_n(df),
            f"\nGet information for all {len(df)} locations here: {url}",
            "\nPlease remember that supply is extremely limited, and that eligibility restritions apply. Best of luck!"
        ]
    )
    print(body)
    return body

def main(event, context):
    data = json.loads(event['body'])
    from_ = "+1 512 488 6383"
    msg = client.messages.create(body=_generate_body(data['zip_']),from_=from_,to=data['to_'])
    print(msg.sid)
    response = {
        "statusCode": 200,
        "body": msg.sid
    }
    return response

# event = {
#     "zip_": "78741",
#     "to_": "+1 713 824 8581"
# }

# __main__(event, "")