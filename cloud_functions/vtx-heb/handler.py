from lib import Notifier

def main(event, context):
    notifier = Notifier('heb', 'stage')
    count = notifier.process_push_notifications()
    return f'pushed to {count} subscribers'

if __name__ == "__main__":
    main("","")