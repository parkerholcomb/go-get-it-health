import json
from lib import Messager

def main(event, context):
    print("event:\n", event)
    data = json.loads(event['body'])
    to_ = data['phone']
    message = "You're almost ready to #gogetit. Reply to this thread with your zip code to receive updates about vaccine availability in your area. To unsubscribe at anytime reply STOP"
    Messager().send_sms(to_, message)

    response = {
        "statusCode": 200,
        "body": f"prompt message sent to {to_}"
    }

    return response