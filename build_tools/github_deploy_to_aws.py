import datetime
import json
import mimetypes
import os
import sys
import pickle
from tempfile import NamedTemporaryFile
import boto3
import botocore.exceptions
import site_hasher

TIMESTAMP_STR = datetime.datetime.now().strftime("%Y%M%d%H%M%S%f")

aws_credentials = None
s3_hash_dict = {}
local_hash_dict = {}

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
if AWS_ACCESS_KEY is not None and AWS_SECRET_KEY is not None:
    aws_credentials = {
        'access_key_id': AWS_ACCESS_KEY,
        'access_key': AWS_SECRET_KEY
    }
else:
    with open('aws_jehtech_uploader_credentials.json', 'r', encoding='ascii') as fh:
        aws_credentials = json.load(fh)

s3 = boto3.client(
    's3', 
    aws_access_key_id=aws_credentials['access_key_id'],
    aws_secret_access_key=aws_credentials['access_key'],
    region_name='eu-west-2'
)

cf = boto3.client(
    'cloudfront',
    aws_access_key_id=aws_credentials['access_key_id'],
    aws_secret_access_key=aws_credentials['access_key'],
    region_name='eu-west-2'
)

with NamedTemporaryFile() as tmp_file:
    try:
        print("Downloading remote site hash file... ", end="")
        s3.download_file('jehtech.com', 'site_hashes.dat', tmp_file.name)
        print("Done")
        s3_hash_dict = site_hasher.LoadHashDict(tmp_file.name)
    except botocore.exceptions.ClientError as exc:
        if exc.response['Error']['Code'] == '404':
            print("NOTE: The remote site hash data file did not exist")
            s3_hash_dict = {}
        else:
            raise exc

local_hash_dict = site_hasher.LoadHashDict('../output/site_hashes.dat')

local_hash_dict_keys = set(local_hash_dict.keys())
s3_hash_dict_keys = set(s3_hash_dict.keys())


# All the files in local_hash_dict are either new or updated. Deleted files have been received on the command line.
# Update the s3_hash_dict with hashes from local_hash_dict and delete any keys in s3_hash_dict who's file names are
# in those received on the command line.
files_for_upload = list()
if local_hash_dict_keys:
    for file_path in local_hash_dict_keys:
        s3_hash_dict[file_path] = local_hash_dict[file_path]
        files_for_upload.append(file_path)       
        
        file_mime_type =  mimetypes.guess_type(file_path)[0]

        print(f'Uploading {file_path} as {file_mime_type}')
        s3.upload_file(
            f'../output/site/{file_path}',
            'jehtech.com',
            file_path,
            ExtraArgs={
                'ContentType': file_mime_type
            }
        )

    print("Creating CloudFront invalidations for uploaded files...")
    cf.create_invalidation(
        DistributionId="E1CW0OHDVEVITS",
        InvalidationBatch={
            'Paths': {
                'Quantity': len(files_for_upload),
                'Items': list(f'/{x}' for x in files_for_upload)
            },
            'CallerReference': f'{TIMESTAMP_STR}-JEHTech-Upload-Script-Added-Files'
        },
    )
else:
    print("Nothing to upload to remote")
    
deleted_files = list()
if len(sys.argv) > 1 and sys.argv[1].strip() != "":
    deleted_files = sys.argv[1].split(" ")

if deleted_files:
    for file_path in deleted_files:
        if file_path in s3_hash_dict:        
            del s3_hash_dict[hash]

            print(f'Deleting {file_path}')
            s3.delete_object(
                Bucket='jehtech.com',
                Key=file_path
            )

    print("Creating CloudFront invalidations for deleted files...")
    cf.create_invalidation(
        DistributionId="E1CW0OHDVEVITS",
        InvalidationBatch={
            'Paths': {
                'Quantity': len(deleted_files),
                'Items': list(f'/{x}' for x in deleted_files)
            },
            'CallerReference': f'{TIMESTAMP_STR}-JEHTech-Upload-Script-Deleted-Files'
        },
    )
else:
    print("Nothing to delete on remote")

if files_for_upload or deleted_files:
    print("Overwriting site_hashes.dat")
    with open('../output/site_hashes.dat', 'wb') as handle:
        pickle.dump(s3_hash_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Uploading site_hashes.dat")
    s3.upload_file('../output/site_hashes.dat', 'jehtech.com', 'site_hashes.dat')
