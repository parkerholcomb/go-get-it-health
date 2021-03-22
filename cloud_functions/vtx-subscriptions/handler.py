import json
import base64
from twilio.rest import Client
from urllib import parse
import boto3
import time

ENV = 'dev'

def _load_twilio_client():
    secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
    get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
    secret = json.loads(get_secret_value_response['SecretString'])
    return Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])

twilio_client = _load_twilio_client()
from_ = "+1 512 488 6383"

# get the message
def _parse_inbound_msg(event):
    base64_message = event['body']
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return parse.parse_qs(message)
    
# if body has a valid zip...save and respond confirm

def send_sms(to_, body):
    if ENV == 'dev':
        print(f"Message sent {from_} to {to_} -- ENV=DEV:\n", body)
        return 

    msg = twilio_client.messages.create(body=body,from_=from_,to=to_)
    resp = f"Message sent {from_} to {to_} with locations -- {msg.sid}"
    print(resp)

def _extract_valid_zip(body):
    with open("https://vtx-public.s3.amazonaws.com/tx_zip_geo_cache.json", 'r') as f:
        data = json.load(f)
    valid_zips = data.keys()
    tokens = body.split(" ")
    for token in tokens:
        if token in valid_zips:
            return token
    raise Exception

def subscribe(to_, zip_, msgContent, radius = 100):
    data = dict(
        to_ = to_,
        zip_ = zip_,
        radius = radius,
        created = int(time.time()),
        meta = msgContent
    )
    s3_bucket = boto3.resource('s3').Bucket('vtx-subscriptions')
    s3_bucket.Object(key=f"{to_}#{zip_}").put(Body=json.dumps(data))
    return 'saved'

def send_invalid_repsonse(from_):
    to_ = from_
    body = f"Nah that didn't work"
    send_sms(to_, body)
    print(body)

def send_subscribe_confirmation(from_, zip_, radius = 100):
    to_ = from_
    body = f"Thanks. You're registered to received notifications for {zip_} + {radius} miles."
    send_sms(to_, body)

def try_suscribe(msgContent):
    body = msgContent['Body'][0]
    from_ = body = msgContent['From'][0]
    try: 
        zip_ = _extract_valid_zip(body)
        subscribe(from_, zip_, msgContent)
        send_subscribe_confirmation(from_, zip_)
    except:
        send_invalid_repsonse(from_)

def main(event, context):
    print("event:", event)
    print("context:", context)
    
    msgContent = _parse_inbound_msg(event)
    print("msgContent", msgContent)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response