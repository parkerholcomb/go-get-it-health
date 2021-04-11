from lib.Messager import Messager
from lib.Subscriber import Subscriber
from lib.GeoZipCache import GeoZipCache

def main(event, context):
    # print("event:", event)
    # print("context:", context)
    messager = Messager()
    msgContent = messager.parse_inbound_msg(event)
    print("msgContent", msgContent)
    body = msgContent['Body'][0]
    zip_ = GeoZipCache().extract_valid_zip(body)
    sender_number = msgContent['From'][0]
    if zip_:
        # env = Messager().get_env(msgContent['To'][0])
        subscriber = Subscriber()
        
        subscriber.add_subscriber(sender_number, zip_, msgContent)
        response_sms_body = f"Congrats! You're registered to received notifications for {zip_} + {subscriber.default_radius} miles. You're almost ready to #gogetit"
    else: 
        response_sms_body = f"Reply with your 5 digit TX zip code to get notified when vaccines become available in your area."

    messager.send_sms(sender_number, response_sms_body)
    
    response = {
        "statusCode": 200
    }

    return response

if __name__ == "__main__":
    main("","")