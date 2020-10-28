import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime

import urllib.request as req
import cv2
import random

def generate_image_url(bucket, blob_path):
    """ generate signed URL of a video stored on google storage. 
        Valid for 300 seconds in this case. You can increase this 
        time as per your requirement. 
    """                                                        
    blob = bucket.blob(blob_path) 
    return blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

def download_video(video_path):
    cred = credentials.Certificate('apikey.json')
    name = 'storage' + str(random.random())
    app = firebase_admin.initialize_app(cred, {'storageBucket': 'test-bucket-1997/input'}, name=name)
    bucket = storage.bucket(app=app)

    url = generate_image_url(bucket, video_path[1])
    req.urlretrieve(url, ''.join(video_path))