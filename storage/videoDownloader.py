import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime

import urllib.request as req
import cv2

def generate_image_url(bucket, blob_path):
    """ generate signed URL of a video stored on google storage. 
        Valid for 300 seconds in this case. You can increase this 
        time as per your requirement. 
    """                                                        
    blob = bucket.blob(blob_path) 
    return blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

def download_video(video_name):
    video_name += '.mp4'
    cred = credentials.Certificate('apikey.json')
    app = firebase_admin.initialize_app(cred, {'storageBucket': 'test-bucket-1997/input'}, name='storage')
    bucket = storage.bucket(app=app)

    url = generate_image_url(bucket, video_name)
    req.urlretrieve(url, "videos/input/"+video_name)