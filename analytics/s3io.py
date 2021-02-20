import boto3
import json
import smart_open
import os
import csv
import pandas as pd
import numpy as np
from io import StringIO, BytesIO
import zipfile


def pandas_to_csv(df, bucket_nm, prefix, file_nm, header=True):
    '''
    --------------------------------------------------------------------
    Takes a pandas dataframe and saves as a .csv file to S3.

    pandas_to_csv(df, bucket_nm, prefix, file_nm, header=True)

    df:        pandas dataframe, object to be saved to S3
    bucket_nm: string, name of S3 bucket
    prefix:    string, path to save the file, do not include '/' at
               beginning or end
    file_nm:   string, name of file to be saved, include '.csv' at end
    header:    boolean or list of strings, True if headers should be
               written as the first row of the .csv file

    --------------------------------------------------------------------
    '''

    s3r = boto3.resource("s3")
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=header)
    s3r.Object(bucket_nm, f"{prefix}/{file_nm}") \
        .put(Body=csv_buffer.getvalue())


def csv_to_pandas(bucket_nm, prefix=None, file_nm=None, sep=',', columns=None, dtype_dict=None):
    '''
    --------------------------------------------------------------------
    Loads a .csv file from S3 and creates pandas dataframe object.

    csv_to_pandas(
                  bucket_nm,
                  prefix,
                  file_nm,
                  sep=',',
                  columns=None,
                  dtype_dict=None
                  )

    bucket_nm:  string, name of S3 bucket
    prefix:     string, path where file is located, do not include
                '/' at beginning or end
    file_nm:    string, name of file to be loaded, include '.csv'
                at end
    sep:        string identifier used to separate columns in '.csv'
                file
    columns:    list of strings, 'None' if first row of .csv file
                should be used as column names, else the list of
                strings should be used as the column names
    dtype_dict: dictionary, keys are columns, values are the type of
                data in that column. Available types are: str, int,
                float. Dates are not currently supported.

    returns:    pandas dataframe

    --------------------------------------------------------------------
    '''

    s3c = boto3.client("s3")
    if prefix == None:
        ky = file_nm
    else:
        ky = f'{prefix}/{file_nm}'
    csv_obj = s3c.get_object(Bucket=bucket_nm,
                             Key=ky)
    csv_body = csv_obj['Body']
    csv_string = csv_body.read().decode('utf-8')
    if columns == None and dtype_dict == None:
        df = pd.read_csv(StringIO(csv_string), sep=sep)
    elif dtype_dict == None:
        df = pd.read_csv(StringIO(csv_string),
                         header=None,
                         sep=sep,
                         engine='python',
                         names=columns)
    elif columns == None:
        df = pd.read_csv(StringIO(csv_string),
                         sep=sep,
                         engine='python',
                         dtype=dtype_dict)
    else:
        df = pd.read_csv(StringIO(csv_string),
                         header=None,
                         sep=sep,
                         engine='python',
                         names=columns,
                         dtype=dtype_dict)
    return df


def list_to_csv(list_nm, bucket_nm, prefix, file_nm):
    '''
    --------------------------------------------------------------------
    Takes a list of lists and saves as a .csv file to S3.

    list_to_csv(list_nm, bucket_nm, prefix, file_nm)

    list_nm:   list of lists, object to be saved to S3
    bucket_nm: string, name of S3 bucket
    prefix:    string, path to save the file, do not include '/' at
               beginning or end
    file_nm:   string, name of file to be saved, include '.csv' at end

    --------------------------------------------------------------------
    '''

    with smart_open.open(f"s3://{bucket_nm}/{prefix}/{file_nm}",
                         "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(list_nm)


# save a dictionary as a json file in S3
def dict_to_json(dict_obj, bucket_nm, prefix, file_nm):
    '''
    --------------------------------------------------------------------
    Takes a dictionary object and saves as a .json file to S3.

    dict_to_json(dict_obj, bucket_nm, prefix, file_nm)

    dict_obj:  dictionary, object to be saved to S3
    bucket_nm: string, name of S3 bucket
    prefix:    string, path to save the file, do not include '/' at
               beginning or end
    file_nm:   string, name of file to be saved, include '.json' at end

    --------------------------------------------------------------------
    '''

    with smart_open.open(f's3://{bucket_nm}/{prefix}/{file_nm}',
                         'wb', encoding='utf-8') as fp:
        json.dump(dict_obj, fp)


def json_to_dict(bucket_nm, prefix, file_nm):
    '''
    --------------------------------------------------------------------
    Loads a .json file from S3 and creates dictionary object.

    json_to_dict(bucket_nm, prefix, file_nm)

    bucket_nm: string, name of S3 bucket
    prefix:    string, path where file is located, do not include
               '/' at beginning or end
    file_nm:   string, name of file to be loaded, include '.csv'
               at end

    returns:   dictionary object

    --------------------------------------------------------------------
    '''

    with smart_open.open(f"s3://{bucket_nm}/{prefix}/{file_nm}",
                         'rb', encoding='utf-8') as fp:
        loaded_dict = json.load(fp)
    return loaded_dict


def delete_file(bucket_nm, prefix, file_nm):
    '''
    --------------------------------------------------------------------
    Deletes a file from S3.

    delete_file(bucket_nm, prefix, file_nm)

    bucket_nm: string, name of S3 bucket
    prefix:    string, path for file to be deleted, do not include
               '/' at beginning or end
    file_nm:   string, name of file to be deleted, include '.csv' at end
    header:    boolean or list of strings, True if headers should be
               written as the first row of the csv file

    --------------------------------------------------------------------
    '''

    s3r = boto3.resource("s3")
    s3r.Object(bucket_nm, f"{prefix}/{file_nm}").delete()


def list_files(bucket_nm, prefix=None):
    '''
    --------------------------------------------------------------------
    Lists all files found in a bucket and/or specific prefix in S3.

    list_files(bucket_nm, prefix=None)

    bucket_nm: string, name of S3 bucket
    prefix:    None or string, if string only files with this prefix
               will be returned

    --------------------------------------------------------------------
    '''

    s3r = boto3.resource("s3")
    bucket = s3r.Bucket(bucket_nm)
    if prefix == None:
        file_list = bucket.objects.all()
    else:
        file_list = bucket.objects.filter(Prefix=prefix)
    for k in file_list:
        print(k.key)


def get_file_list(bucket_nm, prefix=None):
    '''
    --------------------------------------------------------------------
    returns a list with all files found in a bucket and/or specific
    prefix in S3.

    get_file_list(bucket_nm, prefix=None)

    bucket_nm:  string, name of S3 bucket
    prefix:     None or string, if string only files with this prefix
                will be returned

    returns:    list, with all files found in bucket / prefix

    --------------------------------------------------------------------
    '''

    s3r = boto3.resource("s3")
    bucket = s3r.Bucket(bucket_nm)
    if prefix == None:
        file_list = bucket.objects.all()
    else:
        file_list = bucket.objects.filter(Prefix=prefix)

    return file_list


def zip_extract(bucket_nm, zip_key, save_prefix):
    '''
    --------------------------------------------------------------------
    Loads a .zip file from S3 and extracts all files to a folder
    location in S3.

    zip_extract(bucket_nm, zip_key, save_prefix)

    bucket_nm: string, name of S3 bucket
    zip_key:   string, name of .zip file to be unzipped, include
               '.zip' at end
    prefix:    string, path where extracted files should be saved, do
               not include '/' at beginning or end

    --------------------------------------------------------------------
    '''

    s3r = boto3.resource('s3')
    zip_obj = s3r.Object(bucket_name=bucket_nm, key=zip_key)
    buffer = BytesIO(zip_obj.get()["Body"].read())

    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        s3r.meta.client.upload_fileobj(
            z.open(filename),
            Bucket=bucket_nm,
            Key=f'{save_prefix}/{filename}')