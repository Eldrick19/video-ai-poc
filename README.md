# video-ai-poc
 
This repository holds the code for Adastra's Vision POC. The Vision POC leverages GCP and its services to detect social distancing among people from a livecam. Currently WIP

Before running main.py, ensure that you have done the following:

## ONLINE OR LOCAL STORAGE
In the main.py file, you can either activate or or deactivate online storage by setting the 'storage_online' variable as True or False.

## CLOUD STORAGE
Make sure you have access to the appropriate cloud storage bucket if you have decided to go with online storage. 
Add the video file you want to analyze to the 'input' folder in the appropriate bucket.
Ask Eldrick if you need access.

## BEFORE RUNNING
1) Go to your repository file path in your CMD
2) Create a virtual environment. In CMD write: 'python -m venv [c:\path\to\myenv]'
2) Activate your virtual environment. In CMD write '[c:\path\to\myenv]\Scripts\activate'
3) Download dependencies. In CMD write 'pip install -r requirements.txt'
4) Initalize API key.
	a) Let [PATH] be youre API key path (it is found in this repo under the name 'apikey.json')
	b) In the command prompt write 'set GOOGLE_APPLICATION_CREDENTIALS=[PATH]'.
5) To run the function, make sure your CMD format is the following: 
	a) _"python main.py [VIDEO_NAME] [DETECTION_CALL_1] (optional)[DETECTION_CALL_2]"_
	b) For example: _"python main.py people-detection PERSON_DETECTION HOG_OPENCV"_
	
## TEST VIDEOS
Here is a link with interesting test videos:
https://software.intel.com/content/www/us/en/develop/articles/overview-of-sample-videos-created-for-inference.html

Ask Eldrick if you would like a few more videos.

Please contact Eldrick at 'eldrick.wega@gmail.com' if you have any questions or concerns.
