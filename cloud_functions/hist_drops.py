import boto3
from io import StringIO
import pandas as pd
from datetime import datetime
import regex as re


def _get_file_list(bucket_nm, prefix):
    s3r = boto3.resource("s3")
    bucket = s3r.Bucket(bucket_nm)
    file_list = bucket.objects.filter(Prefix=prefix)

    return file_list


def _calc_drops(today, hr_min, new_df, old_df):
    dttm = datetime.strptime(f'{today} {hr_min}', '%Y-%m-%d %H:%M')
    new_df['name_id'] = [f'{re.sub("[^0-9a-zA-Z]+", "", nm).lower()}#{zp}'
                         for nm, zp
                         in zip(new_df['NAME'], new_df['ZIP'])]
    new_df['extract_dttm'] = dttm
    new_df['LAST_UPDATE_VAC'] = new_df['LAST_UPDATE_VAC'].fillna(value='01/01/2021')
    new_df['LAST_UPDATE_TIME_VAC'] = new_df['LAST_UPDATE_TIME_VAC'].fillna(value='00:00')
    new_df['last_update_dttm'] = [datetime.strptime(f'{dt.strip()} {tm.strip()[:5]}', '%m/%d/%Y %H:%M')
                                  for dt, tm in zip(new_df['LAST_UPDATE_VAC'],
                                                    new_df['LAST_UPDATE_TIME_VAC'])]
    old_df['name_id'] = [f'{re.sub("[^0-9a-zA-Z]+", "", nm).lower()}#{zp}'
                         for nm, zp
                         in zip(old_df['NAME'], old_df['ZIP'])]
    new_df.rename(columns={'Total_Shipped': 'new_shipped',
                           'VACCINES_AVAILABLE': 'new_available',
                           'TYPE': 'location_type'},
                  inplace=True)
    new_counts = new_df[['name_id', 'new_shipped', 'new_available',
                         'location_type', 'extract_dttm', 'last_update_dttm']]
    old_counts = old_df[['name_id', 'old_shipped', 'old_available']]

    comp_df = new_counts.merge(old_counts, on='name_id', how='left')
    new_sites = comp_df[comp_df['old_shipped'].isnull()].reset_index(drop=True)
    new_sites['jab_ct'] = [0 if avail == 0 else shp - avail
                           for shp, avail
                           in zip(new_sites['new_shipped'],
                                  new_sites['new_available'])]
    new_sites.rename(columns={'new_shipped': 'drop_ct'}, inplace=True)

    updates = comp_df[comp_df['old_shipped'].notnull()].copy()
    updates['drop_ct'] = [new - old
                          for new, old
                          in zip(updates['new_shipped'],
                                 updates['old_shipped'])]
    updates['jab_ct'] = [0 if old == 0 else old - (new - drp)
                         for old, new, drp
                         in zip(updates['old_available'],
                                updates['new_available'],
                                updates['drop_ct'])]

    changes = updates[(updates['drop_ct'] > 0) | (updates['jab_ct'] > 0)].reset_index(drop=True)

    drop_df = pd.concat([new_sites[['name_id', 'location_type', 'extract_dttm', 'last_update_dttm',
                                    'drop_ct', 'jab_ct']],
                         changes[['name_id', 'location_type', 'extract_dttm', 'last_update_dttm',
                                  'drop_ct', 'jab_ct']]],
                        axis=0)

    return drop_df


def _save_drops(today, hr_min, drop_df, source='tdem'):
    drop_df.to_csv(f's3://data-{source}/test/changes/{today}/{hr_min}/{source}-daily-changes.csv', index=False)


def main():
    hist_files = [fl for fl in _get_file_list('data-tdem', 'raw') if not fl.key.startswith('raw/latest')]
    old_df = None

    for fl_path in hist_files:
        new_df = pd.read_csv(f's3://data-tdem/{fl_path.key}')
        if old_df is None:
            old_df = new_df.rename(columns={'Total_Shipped': 'old_shipped',
                                            'VACCINES_AVAILABLE': 'old_available'}).copy()
        else:
            path_split = fl_path.key.split('/')
            today = path_split[1]
            hr_min = path_split[2]
            drop_df = _calc_drops(today, hr_min, new_df, old_df)
            _save_drops(today, hr_min, drop_df)
            old_df = new_df.rename(columns={'new_shipped': 'old_shipped',
                                            'new_available': 'old_available'}).copy()
            msg = f"{len(new_df)} records saved to S3 at {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            print(msg)


main()
