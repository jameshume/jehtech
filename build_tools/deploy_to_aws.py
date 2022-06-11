import datetime
import json
import mimetypes
import os
import sys
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

if len(sys.argv) > 1 and sys.argv[1] == "refresh":
    print("NOTE: Forcing refresh")
    s3_hash_dict = {}
else:
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

# Everything in the local dict but not in the s3 dict needs to be uploaded
# Anything else that has a different hash needs to be uploaded
local_hash_dict_keys = set(local_hash_dict.keys())
s3_hash_dict_keys = set(s3_hash_dict.keys())
local_files_not_in_remote = local_hash_dict_keys - s3_hash_dict_keys
common_files_between_local_and_remote = local_hash_dict_keys.intersection(s3_hash_dict_keys)
local_files_different_to_remote = set(f for f in common_files_between_local_and_remote if s3_hash_dict[f] != local_hash_dict[f])
files_for_upload = local_files_not_in_remote
files_for_upload.update(local_files_different_to_remote)

# Everything in the s3 dict but not in the local dict needs to be deleted
remote_files_not_in_local = s3_hash_dict_keys - local_hash_dict_keys

# Delete everything no longer needed
if remote_files_not_in_local:
    for file_path in remote_files_not_in_local:
        print(f'FAKE Deleting {file_path}')
        continue
        s3.delete_object(
            Bucket='jehtech.com',
            Key=file_path
        )
    print("Creating CloudFront invalidations for deleted files...")
    cf.create_invalidation(
        DistributionId="E1CW0OHDVEVITS",
        InvalidationBatch={
            'Paths': {
                'Quantity': len(remote_files_not_in_local),
                'Items': list(f'/{x}' for x in remote_files_not_in_local)
            },
            'CallerReference': f'{TIMESTAMP_STR}-JEHTech-Upload-Script-Deleted-Files'
        },
    )
else:
    print("Nothing to delete on remote")

# Upload the new & changed files
if files_for_upload:
    for file_path in files_for_upload:
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

if files_for_upload or remote_files_not_in_local:
    print("Uploading site_hashes.dat")
    s3.upload_file(f'../output/site_hashes.dat', 'jehtech.com', 'site_hashes.dat')
