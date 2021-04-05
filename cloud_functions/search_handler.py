import json
import pandas as pd
from lib.GeoZipCache import GeoZipCache
from geopy.distance import geodesic

geo_zip_cache = GeoZipCache()

def _miles_away(lat_lng_a, lat_lng_b):
    try:
        return int(geodesic(lat_lng_a, lat_lng_b).miles)
    except:
        return 9999

def _vaccine_type_stats(df):
    return dict(
        locations_count = int(df['NAME'].count()),
        total_available = int(df['VACCINES_AVAILABLE'].sum()),
        pfizer_available = int(df['PFIZER_AVAILABLE'].sum()),
        moderna_available = int(df['MODERNA_AVAILABLE'].sum()),
        jj_available = int(df['JJ_AVAILABLE'].sum())
    )


def _location_type_stats(df):
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
    zip_lat_lng = geo_zip_cache.geocode_zip(params['zip_'])
    df = pd.read_csv('https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv') # see if s3 is faster?
    df = df[df['VACCINES_AVAILABLE'] > 0]
    print(f"There are {len(df)} locations in TX with availability")
    # df['lat_lng'] = df['ZIP'].apply(geo_zip_cache.geocode_zip)
    # df['miles_away'] = df['lat_lng'].apply(_miles_away, args=(zip_lat_lng,))
    # df = df[df['miles_away'] < params['radius']]
    # df = df.sort_values(by='miles_away').reset_index(drop=True)
    
    # data = {
    #     "stats": {
    #         "byLocationType": _location_type_stats(df),
    #         "byVaccineType": _vaccine_type_stats(df)
    #     },
    #     "locations": df.to_dict(orient='records')
    # }

    df = df.head()

    data = {
        "byLocationType": _location_type_stats(df),
        "byVaccineType": _vaccine_type_stats(df)
        
    }

    response = {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        "body": df.to_json(orient ='records')
    }

    print(response)
    return response

if __name__ == "__main__":
    body = {
        'zip_': '78741',
        'radius': 20
    }
    event = {'body': json.dumps(body)}
    main(event,"")