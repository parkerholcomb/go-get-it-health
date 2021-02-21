import pandas as pd
from datetime import datetime
import regex as re


def _calc_drops(today, hr_min, new_df, old_df):
    dttm = datetime.strptime(f'{today} {hr_min}', '%Y-%m-%d %H:%M')
    # lower case without special char > NAME#ZIP
    new_df['name_id'] = [f'{re.sub("[^0-9a-zA-Z]+", "", nm).lower()}#{zp}'
                         for nm, zp
                         in zip(new_df['NAME'], new_df['ZIP'])]
    new_df['extract_dttm'] = dttm
    new_df['last_update_dttm'] = [datetime.strptime(f'{dt} {tm}', '%Y-%m-%d %H:%M')
                                  for dt, tm in zip(new_df['LAST_UPDATE_VAC'],
                                                    new_df['LAST_UPDATE_TIME_VAC'])]
    old_df['name_id'] = [f'{re.sub("[^0-9a-zA-Z]+", "", nm).lower()}#{zp}'
                         for nm, zp
                         in zip(old_df['NAME'], old_df['ZIP'])]
    new_df.rename(columns={'Total_Shipped': 'new_shipped',
                           'VACCINES_AVAILABLE': 'new_available',
                           'TYPE': 'location_type'},
                  inplace=True)
    old_df.rename(columns={'Total_Shipped': 'old_shipped',
                           'VACCINES_AVAILABLE': 'old_available'},
                  inplace=True)
    new_counts = new_df[['name_id', 'new_shipped', 'new_available',
                         'location_type', 'last_update_dttm']]
    old_counts = old_df[['name_id', 'old_shipped', 'old_available']]

    comp_df = new_counts.join(old_counts, on='name_id', how='left')
    new_sites = comp_df[comp_df['old_shipped'].isnull()].reset_index(drop=True)
    new_sites.rename(columns={'new_shipped': 'drop_ct'})
    new_sites['jab_ct'] = [0 if avail == 0 else shp - avail
                           for shp, avail
                           in zip(new_sites['new_shipped'],
                                  new_sites['new_available'])]

    updates = comp_df[comp_df['old_shipped'].notnull()]
    updates['drop_ct'] = [new - old
                          for new, old
                          in zip(updates['new_shipped'],
                                 updates['old_shipped'])]
    updates['jab_ct'] = [0 if old == 0 else old - (new - drp)
                         for old, new, drp
                         in zip(updates['old_available'],
                                updates['new_available'],
                                updates['drop_ct'])]

    changes = updates[updates['drop_ct'] > 0 | updates['jab_ct'] > 0].reset_index(drop=True)

    drop_df = pd.concat([new_sites[['name_id', 'location_type', 'extract_dttm', 'last_update_dttm',
                                    'drop_ct', 'jab_ct']],
                         changes[['name_id', 'location_type', 'extract_dttm', 'last_update_dttm',
                                  'drop_ct', 'jab_ct']]],
                        axis=1)

    return drop_df


def _save_partitions(today, hr_min, df, drop_df, source='tdem'):
    df.to_csv(f's3://data-{source}/raw/{today}/{hr_min}/{source}-vaccine-supply.csv', index=False)
    df.to_csv(f's3://data-{source}/raw/latest/{source}-vaccine-supply.csv', index=False)
    drop_df.to_csv(f's3://data-{source}/changes/{today}/{hr_min}/{source}-daily-changes.csv', index=False)


def main(event, context):
    today = datetime.now().strftime('%Y-%m-%d')
    hr_min = datetime.now().strftime('%H:%M')

    df = pd.read_csv("https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv")

    s3c = boto3.client("s3")
    latest_obj = s3c.get_object(Bucket='data-tdem',
                                Key='raw/latest/tdem-vaccine-supply.csv')
    latest_body = latest_obj['Body']
    latest_string = latest_body.read().decode('utf-8')
    latest_df = pd.read_csv(StringIO(latest_string), sep='\t')
    drop_df = _calc_drops(today, hr_min, df, latest_df)

    _save_partitions(today, hr_min, df, drop_df)
    msg = f"{len(df)} records moved to S3 at {datetime.now().strftime('%Y-%m-%d')}"
    print(msg)
    response = {
        "statusCode": 200,
        "body": msg
    }
    return response

# main("","")