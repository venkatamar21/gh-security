import os
import boto3
from botocore.config import Config


def run():
    bucket = os.environ.get('INPUT_BUCKET')
    bucket_region = os.environ.get('INPUT_BUCKET_REGION', 'us-east-1')
    dist_folder = os.environ.get('INPUT_DIST_FOLDER')

    if not bucket:
        raise ValueError("INPUT_BUCKET environment variable is required")
    if not dist_folder:
        raise ValueError("INPUT_DIST_FOLDER environment variable is required")

    configuration = Config(region_name=bucket_region)
    s3_client = boto3.client('s3', config=configuration)

    uploaded_files = 0
    for root, subdirs, files in os.walk(dist_folder):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, dist_folder).replace('\\', '/')
            try:
                s3_client.upload_file(file_path, bucket, s3_key)
                print(f"Uploaded: {s3_key}")
                uploaded_files += 1
            except Exception as e:
                print(f"Failed to upload {s3_key}: {str(e)}")
                raise

    print(f"Successfully uploaded {uploaded_files} files to S3 bucket '{bucket}'")
    website_url = f'http://{bucket}.s3-website-{bucket_region}.amazonaws.com'
    print(f'::set-output name=website-url::{website_url}')


if __name__ == '__main__':
    run()
