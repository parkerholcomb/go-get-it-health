from lib.Fetcher import Fetcher
from lib.Notifier import Notifier

def main(event, context):
    source = 'heb'
    env = 'dev'
    if env != 'dev':
        Fetcher(source)
    notifier = Notifier(source, env)
    update_count = notifier.process_push_notifications()
    return f'pushed to {update_count} subscribers'

if __name__ == "__main__":
    main("","")