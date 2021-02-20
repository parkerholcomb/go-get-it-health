import boto3
import pandas as pd
from datetime import datetime
from s3io import get_file_list, csv_to_pandas, pandas_to_csv

pd.set_option('display.max_columns',20)


# Let's use Amazon S3
s3r = boto3.resource('s3')

print('all the buckets:\n')
for bucket in s3r.buckets.all():
    print(bucket.name)

print('all the files in data-tdem:\n')
vtx_files = get_file_list('data-tdem')

print([fl.key for fl in vtx_files])
# capture when updates are happening for each location
#   (i.e., some number changed?
#   or do they only show up if there's an update?)
# calculate how many vaccines are showing up at each location
#   (previous total_shipped - current total_shipped)
# calculate how many vaccines are being administered at each location
#   (previous vaccines_available - current vaccines_available)
# roll these numbers up to the county level and compare to population

full_list = []
old_counts = {}
drop_admin_list = []

for fl_path in vtx_files:
    if not fl_path.key.startswith('raw/latest'):
        path_split = fl_path.key.split('/')
        ky = path_split[0]
        fl = '/'.join(path_split[1:])
        dttm = datetime.strptime(f'{path_split[1]} {path_split[2]}', '%Y-%m-%d %H:%M')
        hr_df = csv_to_pandas('data-tdem', ky, fl)
        # lower case without special char > NAME#ZIP
        hr_df['nm_st'] = [f'{nm} - {st}' for nm, st in zip(hr_df['NAME'], hr_df['ADDRESS'])]
        new_counts = {nm_st: [zip, shipped, available]
                      for nm_st, zip, shipped, available
                      in zip(hr_df['nm_st'],
                             hr_df['ZIP'],
                             hr_df['Total_Shipped'],
                             hr_df['VACCINES_AVAILABLE'])}

        if old_counts == {}:
            pass
        else:
            for new_ky in new_counts.keys():
                if new_ky not in old_counts.keys():
                    drop_admin_list.append([new_ky, new_counts[new_ky][0],
                                            dttm, 'new site',
                                            new_counts[new_ky][1], new_counts[new_ky][2]])
                else:
                    drp_ct = new_counts[new_ky][1] - old_counts[new_ky][1]
                    if old_counts[new_ky][2] == 0:
                        adm_ct = 0
                    else:
                        adm_ct = old_counts[new_ky][2] - (new_counts[new_ky][2] - drp_ct)
                    if drp_ct > 0 or adm_ct > 0:
                        drop_admin_list.append([new_ky, new_counts[new_ky][0],
                                                dttm, 'update', drp_ct, adm_ct])
        old_counts = new_counts
        if len(full_list) == 0:
            full_list = hr_df.nm_st.to_list()
        else:
            new_places = [n for n in hr_df.nm_st if n not in full_list]
            full_list.extend(new_places)
            print(f'found {len(new_places)} new places in {dttm}')

print(hr_df.columns)


drop_admin_df = pd.DataFrame(drop_admin_list,
                             columns=['name-address', 'zip', 'datetime',
                                      'update_type', 'drop_ct', 'administered_ct'])

pop_df = csv_to_pandas('data-income-by-zip', file_nm='irs-by-zip-2018-tx.csv')

for c in pop_df.columns:
    print(c)

print(pop_df[['zipcode', 'agi_stub', 'N1', 'N2', 'NUMDEP', 'A00100']].head(50))
print(pop_df.shape)
print(pop_df.dtypes)

# pop_df['N2'] = pop_df['N2'].astype('int32')

zip_list = []
for zp in drop_admin_df['zip'].drop_duplicates():
    try:
        zp_int = int(zp)
        zp_df = pop_df[pop_df['zipcode'] == zp_int]
        pop_total = zp_df['N2'].sum()
        low_inc = zp_df[zp_df['agi_stub'].isin([1, 2, 3])]
        hi_inc = zp_df[zp_df['agi_stub'].isin([4, 5, 6])]

        print(low_inc[['agi_stub', 'N2']])

        low_total = low_inc['N2'].sum()
        hi_total = hi_inc['N2'].sum()

        zip_list.append([zp, pop_total, round(low_total / hi_total, 3)])
    except:
        print(f'{zp} could not be converted to int')
        pass

zp_info = pd.DataFrame(zip_list, columns=['zip', 'pop_ct', 'income_ratio'])

drop_admin_pop_df = pd.merge(drop_admin_df, zp_info, on='zip', how='left')

drop_admin_pop_df.to_csv('drop_admin_pop_df_021021.csv', index=False)