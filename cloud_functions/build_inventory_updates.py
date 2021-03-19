import pandas as pd
import boto3
import time
## currently takes about 40 seconds to run, could probs optimize this
def main(event, context):
    t0 = int(time.time())
    s3_bucket = boto3.resource('s3').Bucket('data-tdem')
    raw_keys = [obj.key for obj in s3_bucket.objects.all() if ~obj.key.startswith('latest')]
    df = pd.concat([pd.read_csv(f"s3://data-tdem/{key}") for key in raw_keys])
    # df = df[['name','type','total_available','last_update']]
    df['total_available'] = df['total_available'].fillna(0)
    df = df[df['total_available'] > 0]
    df = df.drop_duplicates(subset=['name','last_update'], keep='last') #last_update = #YYYY-MM-DD
    df = df.sort_values(by='last_update', ascending=False)
    df.to_csv('s3://data-tdem/latest/inventory_updates.csv', index=False)

    response = {
        "statusCode": 200,
        "body": f"transformed {len(df)} update events in {int(time.time()) - t0} seconds"
    }
    print(response)
    return response

main("","")