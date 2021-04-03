import json
import boto3
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
from helpers import GeoZipCache, Messager, Subscribers

# class Loader:
#     def __init__(self, source):
#         self.source = source
#         self.s3_bucket = boto3.resource('s3').Bucket(f'data-{source}')

#     @staticmethod
#     def _get_filetype(key):
#         if key.endswith('json'):
#             return 'json' 
#         elif key.endswith('csv'):
#             return 'csv' 
    
#     def get_current_prev_dfs(self):
#         raw_keys = [obj.key for obj in self.s3_bucket.objects.all() if (obj.key.startswith('raw') and not obj.key.startswith('raw/latest'))]
#         if self._get_filetype(raw_keys[-1]) == 'csv':
#             # stored as csv (vs heb is in json)
#             prev_df = pd.read_csv(f"s3://data-{self.source}/{raw_keys[-2]}")
#             current_df = pd.read_csv(f"s3://data-{self.source}/{raw_keys[-1]}")
#         else: 
#             prev_df = pd.read_json(f"s3://data-{self.source}/{raw_keys[-2]}")
#             current_df = pd.read_json(f"s3://data-{self.source}/{raw_keys[-1]}")
#         return [prev_df, current_df]

    

# class Notifier:

#     def __init__(self, source, env = 'stage'):
#         self.env = env
#         self.source = source
#         self.current_df, self.prev_df = Fetcher(self.source).get_current_prev_dfs()
#         self.geo_zip = GeoZipCache()
#         self.geocode_dfs()
#         self.subscribers = Subscribers(env).subscribers
#         self.messager = Messager()

#     def geocode_dfs(self):
#         self.current_df['lat_lng'] = self.current_df['ZIP'].apply(self.geo_zip.geocode_zip)
#         self.prev_df['lat_lng'] = self.prev_df['ZIP'].apply(self.geo_zip.geocode_zip)
    
#     @staticmethod
#     def _miles_away(lat_lng_a, lat_lng_b):
#         try:
#             return int(geodesic(lat_lng_a, lat_lng_b).miles)
#         except:
#             return 9999

#     def get_filtered_location_updates(self, subscriber):
#         print(subscriber)
#         old_df, new_df = self.prev_df, self.current_df
#         # first filter out locations with 0 availabilities
#         new_df = new_df[new_df['VACCINES_AVAILABLE'] > 1]
#         # then filter out locations outside max radius
#         zip_lat_lng = self.geo_zip.geocode_zip(subscriber['zip_'])
#         new_df['miles_away'] = new_df['lat_lng'].apply(self._miles_away, args=(zip_lat_lng,))
#         new_df = new_df[new_df['miles_away'] < subscriber['radius']].sort_values(by='miles_away')
        
#         df = pd.merge(old_df, new_df, on=['NAME','TYPE','ZIP'], how='outer')
#         df = df.fillna(0)
#         df['VACCINES_AVAILABLE_delta'] = df['VACCINES_AVAILABLE_y'] - df['VACCINES_AVAILABLE_x']
#         df = df[df['VACCINES_AVAILABLE_delta'] > 0]
#         df['VACCINES_AVAILABLE_delta'] = df['VACCINES_AVAILABLE_delta'].astype(int)
#         df['miles_away'] = df['miles_away'].astype(int)
#         df = df.sort_values(by='miles_away')
#         print(df)
#         return df

#     @staticmethod
#     def _generate_body(df):
#         body = []
#         for idx in df.index:
#             body.append(f"💉 {df.loc[idx]['NAME']} has {df.loc[idx]['VACCINES_AVAILABLE_delta']} new vaccines available, {df.loc[idx]['miles_away']} miles away")
#         # todo save the zip of the first record
#         body.append(f'\nVisit https://www.vaccinatetexas.org/map?= for more information #goandgetgetit')
#         return '\n'.join(body)

#     def process_push_notifications(self):
#         for subscriber in self.subscribers:
#             updates = self.get_filtered_location_updates(subscriber)
#             if len(updates) > 0:
#                 body = self._generate_body(updates)
#                 self.messager.send_sms(subscriber['to_'], body)
#         return 'success'


