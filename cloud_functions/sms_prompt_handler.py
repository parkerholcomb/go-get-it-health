import json
from lib.Messager import Messager
import os

def main(event, context):
    print("event:\n", event)
    data = json.loads(event['body'])
    to_ = data['phone']
    message = "You're almost ready to #gogetit. Reply to this thread with your TX zip code to receive updates about vaccine availability in your area. To unsubscribe at anytime reply STOP"
    # env = 'stage'
    Messager().send_sms(to_, message)

    response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        "body": f"prompt message sent to {to_} for stage: {os.environ.get('DEPLOY_STAGE')}"
    }

    return response