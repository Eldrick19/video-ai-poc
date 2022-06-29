# Video AI POC
 
This repository holds the code for a Vision POC. The Vision POC leverages GCP and its services to detect social distancing among people from a livecam. Worked on this at Adastra Corporation

![A detection from this app](https://github.com/Eldrick19/video-ai-poc/blob/d7c3e03c1789729bb5bf468117f934407bc5b96e/artifacts/img/detection.png)

Before running main.py, ensure that you have done the following:

## Online or Local Storage
In the main.py file, you can either activate or or deactivate online storage by setting the 'storage_online' variable as True or False.

## Cloud Storage
Make sure you have access to the appropriate cloud storage bucket if you have decided to go with online storage. 
Add the video file you want to analyze to the 'input' folder in the appropriate bucket.
Ask Eldrick if you need access.

## Before Running
1. Go to your repository file path in your CMD
2. Create a virtual environment. In CMD write: `python -m venv [c:\path\to\myenv]`
3. Activate your virtual environment. In CMD write `[c:\path\to\myenv]\Scripts\activate`
4. Download dependencies. In CMD write `pip install -r requirements.txt`
5. Initalize API key.
    - Let [_PATH_] be youre API key path (it is found in this repo under the name `apikey.json`)
    - In the command prompt write `set GOOGLE_APPLICATION_CREDENTIALS=[PATH]`.
6. To run the function, make sure your CMD format is the following: 
    - `python main.py [VIDEO_NAME] [DETECTION_CALL_1] (optional)[DETECTION_CALL_2]`
     - For example: `python main.py people-detection PERSON_DETECTION HOG_OPENCV`
	
## Test Videos
[Here](https://software.intel.com/content/www/us/en/develop/articles/overview-of-sample-videos-created-for-inference.html) is a link with interesting test videos.

