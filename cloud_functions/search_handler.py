import json
import pandas as pd
from lib.GeoZipCache import GeoZipCache
from geopy.distance import geodesic
import time

geo_zip_cache = GeoZipCache()

def _miles_away(lat_lng_a, lat_lng_b):
    try:
        return int(geodesic(lat_lng_a, lat_lng_b).miles)
    except:
        return 9999

def _vaccine_stats(df):
    return dict(
        locations_count = int(df['NAME'].count()),
        total_available = int(df['VACCINES_AVAILABLE'].sum()),
        pfizer_available = int(df['PFIZER_AVAILABLE'].sum()),
        moderna_available = int(df['MODERNA_AVAILABLE'].sum()),
        jj_available = int(df['JJ_AVAILABLE'].sum())
    )

def _location_stats(df):
    stats = df.groupby(['TYPE']).agg(
        locations_count=('NAME','count'), 
        total_available=('VACCINES_AVAILABLE','sum'),
        pfizer_available=('PFIZER_AVAILABLE','sum'),
        moderna_available=('MODERNA_AVAILABLE','sum'),
        jj_available=('JJ_AVAILABLE','sum')
    ).reset_index()

    return stats.to_dict(orient='records')

def main(event, context):
    params = eval(event['body'])
    print("search params: ", params)
    zip_lat_lng = geo_zip_cache.geocode_zip(params['zip_'])
    t0 = time.time()
    df = pd.read_csv('https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv') # see if s3 is faster?
    # df = pd.read_csv("s3://data-tdem/raw/latest/tdem-vaccine-supply.csv")
    print("time to df load: ", time.time() - t0)
    df = df[df['VACCINES_AVAILABLE'] > 0]
    print(f"There are {len(df)} locations in TX with availability")
    df['lat_lng'] = df['ZIP'].apply(geo_zip_cache.geocode_zip)
    df['miles_away'] = df['lat_lng'].apply(_miles_away, args=(zip_lat_lng,))
    df = df[df['miles_away'] < params['radius']]
    df = df.sort_values(by='miles_away').reset_index(drop=True)
    
    selected_fields = ['NAME','TYPE','VACCINES_AVAILABLE','PFIZER_AVAILABLE','MODERNA_AVAILABLE','JJ_AVAILABLE', 'miles_away']
    dft = df[selected_fields]
    dft = dft.rename(columns={'PFIZER_AVAILABLE':'pfizer','MODERNA_AVAILABLE':'moderna','JJ_AVAILABLE':'jj','VACCINES_AVAILABLE':'total','TYPE':'type'})
    print(dft)
    response_data = {
        "locations": dft.to_dict(orient='records'),
        "location_stats": _location_stats(df),
        "vax_stats": _vaccine_stats(df)
    }

    response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(response_data)
    }
    print("time to response: ", time.time() - t0)
    print(response)
    return response

if __name__ == "__main__":
    body = {
        'zip_': '78741',
        'radius': 20
    }
    event = {'body': json.dumps(body)}
    main(event,"")