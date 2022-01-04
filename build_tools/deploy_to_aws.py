import datetime
import json
from tempfile import NamedTemporaryFile
import boto3
import botocore.exceptions
import site_hasher

TIMESTAMP_STR = datetime.datetime.now().strftime("%Y%M%d%H%M%S%f")

aws_credentials = None
s3_hash_dict = {}
local_hash_dict = {}

with open('aws_jehtech_uploader_credentials.json', 'r', encoding='ascii') as fh:
    aws_credentials = json.load(fh)

s3 = boto3.client(
    's3', 
    aws_access_key_id=aws_credentials['access_key_id'],
    aws_secret_access_key=aws_credentials['access_key']
)

cf = boto3.client(
    'cloudfront',
    aws_access_key_id=aws_credentials['access_key_id'],
    aws_secret_access_key=aws_credentials['access_key']
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
        print(f'Deleting {file_path}')
        s3.delete_object(
            'jehtech.com',
            file_path
        )
    print("Creating CloudFront invalidations for deleted files...")
    cf.create_invalidation(
        "E1CW0OHDVEVITS",
        {
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
        print(f'Uploading {file_path}')
        s3.upload_file(f'../output/site/{file_path}', 'jehtech.com', file_path)
    print("Creating CloudFront invalidations for uploaded files...")
    cf.create_invalidation(
        "E1CW0OHDVEVITS",
        {
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
