import boto3
import pandas as pd
from datetime import datetime
import regex as re


def _get_file_list(bucket_nm, prefix):
    s3r = boto3.resource("s3")
    bucket = s3r.Bucket(bucket_nm)
    file_list = bucket.objects.filter(Prefix=prefix)

    return file_list


def _csv_to_pandas(bucket_nm, ky=None):
    s3c = boto3.client("s3")
    csv_obj = s3c.get_object(Bucket=bucket_nm,
                             Key=ky)
    csv_body = csv_obj['Body']
    csv_string = csv_body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string), sep='\t')

    return df


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


def _save_drops(today, hr_min, drop_df, source='tdem'):
    drop_df.to_csv(f's3://data-{source}/test/changes/{today}/{hr_min}/{source}-daily-changes.csv', index=False)


def main():
    hist_files = [fl for fl in _get_file_list('data-tdem', 'raw') if not fl.key.startswith('raw/latest')]
    old_df = None

    for fl_path in hist_files:
        new_df = _csv_to_pandas('data-tdem', fl_path)
        if old_df == None:
            old_df = new_df.copy()
        else:
            path_split = fl_path.key.split('/')
            today = path_split[1]
            hr_min = path_split[2]
            drop_df = _calc_drops(today, hr_min, new_df, old_df)
            _save_drops(today, hr_min, drop_df)
            old_df = new_df.copy()
            msg = f"{len(df)} records moved to S3 at {datetime.now().strftime('%Y-%m-%d')}"
            print(msg)

# main()