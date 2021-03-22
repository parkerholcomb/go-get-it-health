import boto3
import json
from twilio.rest import Client

ENV = 'stage'

def send_sms(to_, body):
    twilio_client = _load_twilio_client()
    from_ = "+1 512 488 6383"
    if ENV == 'dev':
        print(f"Message sent {from_} to {to_} -- ENV=DEV:\n", body)
        return 
    msg = twilio_client.messages.create(body=body,from_=from_,to=to_)
    resp = f"Message sent {from_} to {to_} with locations -- {msg.sid}"
    print(resp)

def _load_twilio_client():
    secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
    get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
    secret = json.loads(get_secret_value_response['SecretString'])
    return Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])