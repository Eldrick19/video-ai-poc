from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os


def upload_video(output_path):
    client = storage.Client.from_service_account_json('apikey.json')
    bucket = client.get_bucket('test-bucket-1997')
    blob = bucket.blob('output/'+output_path[1])
    blob.upload_from_filename(''.join(output_path))