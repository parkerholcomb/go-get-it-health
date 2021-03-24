import json
import boto3
from twilio.rest import Client

class Messager:
    def __init__(self):
        self.twilio_client = self._load_twilio_client()
        self.from_ = "+1 512 488 6383"
        self.env = 'stage'

    @staticmethod
    def _load_twilio_client():
        secrets_client = boto3.session.Session().client(service_name='secretsmanager', region_name="us-east-1")
        get_secret_value_response = secrets_client.get_secret_value(SecretId='vaccinate-texas')
        secret = json.loads(get_secret_value_response['SecretString'])
        client = Client(secret['TWILIO_SID'], secret['TWILIO_SECRET'])
        return client

    def send_sms(self, to_, body):
        if self.env == 'dev':
            print(f"Message sent {self.from_} to {to_} -- ENV=DEV:\n", body)
            return 
        msg = self.twilio_client.messages.create(body=body,from_=self.from_,to=to_)
        resp = f"Message sent {self.from_} to {to_}:\n {body}\n -- {msg.sid}"
        print(resp)