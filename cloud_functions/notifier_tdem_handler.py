import os
from lib.Notifier import Notifier
from lib.Fetcher import Fetcher

def main(event, context):
    # print("event:", event)
    # print("context:", context)
    source = 'tdem'
    
    env = os.environ.get('DEPLOY_STAGE')
    if env != 'dev':
        Fetcher(source)
    notifier = Notifier(source, env)
    update_count = notifier.process_push_notifications()
    return f'pushed to {update_count} subscribers'

if __name__ == "__main__":
    main("","")