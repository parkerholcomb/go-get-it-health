import pandas as pd 


def fetch_tdem_direct():
    return pd.read_csv("https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv")

def fetch_tdem_s3_latest():
    return pd.read_csv("s3://vaccinate-texas/data-tdem/raw/latest/tdem-vaccine-supply.csv")

def _clean_domain(website):
    if not website:
        return ""
    domain = website.lower()
    domain = domain.replace("https://","")
    domain = domain.replace("http://","")
    domain = domain.replace("www.","")
    domain = domain.split("/")[0]
    domain = domain.replace("local.","")
    domain = domain.replace("pharmacy.","")
    return domain


def rollup_by_domain(df):
    df['domain'] = df['WEBSITE']
    dft = df.groupby(['domain']).agg(
        count=('name','count'),
        total_shipped=('total_shipped','sum')
    ).reset_index().sort_values(by='count')
    return dft

def filter_by_3zip(df, zip_starts_with):
    if len(zip_starts_with) != 3:
        return None
    return df[df['zip'].apply(lambda x: x.startswith(zip_starts_with))]