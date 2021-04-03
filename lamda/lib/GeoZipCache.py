import boto3
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoZipCache:
    def __init__(self):
        self.zip_geo_cache = self._load_zip_geo_cache()

    def extract_valid_zip(self, text):
        valid_zips = self.zip_geo_cache.keys()
        tokens = text.split(" ")
        print("tokens:", tokens)
        for token in tokens:
            if token in valid_zips:
                print(token)
                return token
        
    # def miles_away(self, zip_a, zip_b):
    #     lat_lng_a, lat_lng_b = self.geocode_zip(zip_a), self.geocode_zip(zip_b)
    #     try:
    #         return int(geodesic(lat_lng_a, lat_lng_b).miles)
    #     except:
    #         # todo tighten this up
    #         print(f"geocoding failed for {zip_a}, {zip_b}")
    #         return 9999
    
    @staticmethod
    def _load_zip_geo_cache():
        s3_bucket = boto3.resource('s3').Bucket('vtx-public')
        data = eval(s3_bucket.Object(key='tx_zip_geo_cache.json').get()['Body'])
        return data

    def geocode_zip(self, zip_str):
        zip_str = str(zip_str)
        zip_str = zip_str.strip()
        zip_str = zip_str.split("-")[0]
        if zip_str in self.zip_geo_cache.keys():
            return self.zip_geo_cache[zip_str]
        else:
            # geolocator = Nominatim(user_agent="vtx")
            # location = geolocator.geocode(zip_str)
            # return f"{location.latitude},{location.longitude}"
            return 'todo'