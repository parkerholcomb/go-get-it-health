from lib.Messager import Messager
from lib.Subscriber import Subscriber
from lib.GeoZipCache import GeoZipCache

def main(event, context):
    # print("event:", event)
    # print("context:", context)
    msgContent = Messager.parse_inbound_msg(event)
    print("msgContent", msgContent)
    body = msgContent['Body'][0]
    zip_ = GeoZipCache().extract_valid_zip(body)
    if zip_:
        env = Messager().get_env(msgContent['To'][0])
        subscriber = Subscriber(env)
        subscriber.add_subscriber(msgContent['From'][0], zip_, msgContent)
        response_sms_body = f"Congrats! You're registered to received notifications for {zip_} + {subscriber.default_radius} miles. You're almost ready to #goandgetit"
    else: 
        response_sms_body = f"Hmmm. Doesn't look like you gave us a valid TX zip code. Please reply with your 5 digit zip code to subscribe."

    response = {
        "statusCode": 200,
        "body": response_sms_body
    }

    return response