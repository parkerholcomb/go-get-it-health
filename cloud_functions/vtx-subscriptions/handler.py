import json
import base64
from urllib import parse
import boto3
import time
# from lib import send_sms

def _parse_inbound_msg(event):
    base64_message = event['body']
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return parse.parse_qs(message)
    
def _extract_valid_zip(body):
    s3_bucket = boto3.resource('s3').Bucket('vtx-public')
    data = json.load(s3_bucket.Object(key='tx_zip_geo_cache.json').get()['Body'])
    valid_zips = data.keys()
    tokens = body.split(" ")
    print("tokens:\n", tokens)
    for token in tokens:
        if token in valid_zips:
            print(token)
            return token
    return None

def subscribe(to_, zip_, radius, msgContent):
    data = dict(
        to_ = to_,
        zip_ = zip_,
        radius = radius,
        created = int(time.time()),
        meta = msgContent
    )
    s3_bucket = boto3.resource('s3').Bucket('vtx-subscriptions')
    subscription_key = f"{to_}#{zip_}"
    s3_bucket.Object(key=subscription_key).put(Body=json.dumps(data))
    print("subscription added:", subscription_key)
    
    return f"subscription_key {subscription_key} added"

def main(event, context):
    # print("event:", event)
    # print("context:", context)
    msgContent = _parse_inbound_msg(event)
    # print("msgContent", msgContent)
    body = msgContent['Body'][0]
    from_ = msgContent['From'][0]
    zip_ = _extract_valid_zip(body)
    radius = 100
    if zip_:
        subscribe(from_, zip_, radius, msgContent)
        response_sms_body = f"Congrats! You're registered to received notifications for {zip_} + {radius} miles. You're almost ready to #goandgetit"
        # send_sms(from_, response_sms_body)
    else: 
        response_sms_body = f"Hmmm. Doesn't look like you gave us a valid TX zip code. Please reply with your 5 digit zip code to subscribe."
        #  send_sms(from_, response_sms_body)

    response = {
        "statusCode": 200,
        "body": response_sms_body
    }

    return response