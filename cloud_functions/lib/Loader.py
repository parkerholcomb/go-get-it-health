import boto3
import pandas as pd
from GeoZipCache import GeoZipCache

class Loader:
    def __init__(self, source):
        self.source = source
        self.s3_bucket = boto3.resource('s3').Bucket(f'data-{source}')
        self.prev_df, self.current_df = self.get_current_prev_dfs()

    @staticmethod
    def _get_filetype(key):
        if key.endswith('json'):
            return 'json' 
        elif key.endswith('csv'):
            return 'csv' 
    
    def get_current_prev_dfs(self):
        raw_keys = [obj.key for obj in self.s3_bucket.objects.all() if (obj.key.startswith('raw') and not obj.key.startswith('raw/latest'))]
        if self._get_filetype(raw_keys[-1]) == 'csv':
            # stored as csv (vs heb is in json)
            prev_df = pd.read_csv(f"s3://data-{self.source}/{raw_keys[-2]}")
            current_df = pd.read_csv(f"s3://data-{self.source}/{raw_keys[-1]}")
        else: 
            prev_df = pd.read_json(f"s3://data-{self.source}/{raw_keys[-2]}")
            current_df = pd.read_json(f"s3://data-{self.source}/{raw_keys[-1]}")
        return [prev_df, current_df]


class TdemLoader(Loader):

    def __init__(self):
        super().__init__('tdem')
        self.changeset_df = self._changeset_df()
        self._geocode_changeset()
        self._normalize_field_names()

        self.updates_df = self.changeset_df[self.changeset_df['vaccines_delta'] > 0] 

    def _changeset_df(self):
        df = pd.merge(self.prev_df, self.current_df, on=['NAME','TYPE','ZIP'], how='outer')
        df = df.fillna(0)
        df['vaccines_delta'] = df['VACCINES_AVAILABLE_y'] - df['VACCINES_AVAILABLE_x']
        return df

    def _geocode_changeset(self):
        geo_zip_cache = GeoZipCache()
        self.changeset_df['lat_lng'] = self.changeset_df['ZIP'].apply(geo_zip_cache.geocode_zip)

    def _normalize_field_names(self):
        self.changeset_df['name'] = self.changeset_df['NAME']
        self.changeset_df['zip_'] = self.changeset_df['ZIP']