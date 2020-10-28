# When running this script locally, please enter the name of the video as an additional argument (i.e. "name".mp4 - dont include mp4)
# Make sure the mp4 video in question is in the \videos\input folder
# For example, a call could be 'python main.py sep-8-2011-propsal'

#######################################################################
# TURN ON OR OFF FUNCTION TAGS HERE
#######################################################################

storage_online = False
blur_faces = True

#######################################################################

# Import Libraries
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from storage import videoDownloader, videoUploader
from extraction import personTrackingExtractor, personTrackingExtractor2, personTrackingExtractor3, frameBoxesExtractor, lightDataManipulator
from algorithms import socialDistancingTagger
from data import bqJobHelper
from frontend import outputVisualizer, comparisonVisualizer
from pathlib import Path
import pandas as pd
import sys
import time

def social_distancing_detection(video_name, call, storage_online, blur_faces):
    # Define important variables
    video_path = ['videos/input/', video_name + '.mp4']
    output_path = ['videos/output/', video_name + '_' + call + '.avi']

    # STORAGE - Download video from Cloud Storage
    if storage_online:
        print('\nPulling video from Cloud Storage...')
        videoDownloader.download_video(video_path)
    else:
        print('\nYou have decided to pull video locally from the "videos/input/" folder...')

    fps, frame_count, video_dimensions = frameBoxesExtractor.get_video_data(video_path) # Get video metadata
    video_already_analyzed = bqJobHelper.video_analyzed(video_name, call) # Verify if video has already been analyzed

    if video_already_analyzed:

        # DATA - Skip re-analysis by just pulling data from BigQuery
        print('\nData has already been analyzed, pulling video data from BigQuery.')
        frame_detections = bqJobHelper.pull_from_bq(video_name, call)

    else:

        # EXTRACTION - Extract person tracking data using either Google API or OpenCV
        print('\nCalling Person Tracking with feature '+call+'...')
        if call == 'PERSON_DETECTION':
            person_tracking_array = personTrackingExtractor.detect_person(video_path)
        elif call == 'OBJECT_TRACKING':
            person_tracking_array = personTrackingExtractor2.detect_person(video_path)
        elif call == 'HOG_OPENCV':
            person_tracking_array = personTrackingExtractor3.detect_person(video_path, fps, video_dimensions)
            
        # EXTRACTION - Perform light data manipulation
        frame_detections = lightDataManipulator.format_data(person_tracking_array, fps)

        # EXTRACTION - Perform heavier data manipulation. Gets all bounding boxes to be displayed at each frame
        print('\nHeavy data manipulation (bounding box at each frame)...')
        frame_detections = frameBoxesExtractor.detections_at_each_frame(frame_detections, frame_count, video_dimensions, fps, call)
        
        # ALGORITHMS - Highlight all instances of non social distancing
        print('\nRunning social distanding algorithms...')
        frame_detections = socialDistancingTagger.tag_social_distancing(frame_detections, video_dimensions)

        # DATA - Persist the social distancing data to BigQuery
        print('\nSaving social distancing data to the Cloud...')
        bqJobHelper.push_to_bq(frame_detections, video_name, call)

        # STORAGE - Upload video to Cloud Storage
        print('\nPushing video to Cloud Storage...')
        videoUploader.upload_video(output_path)

    detection_interval = frameBoxesExtractor.detection_frame_interval(frame_detections, call) # Get detection interval (variable that helps with face pixelization)

    # FRONTEND - Display person tracking
    print('\nDisplaying Results of '+call+'...')
    outputVisualizer.draw_detections(video_path, output_path, frame_detections, fps, video_dimensions, detection_interval, blur_faces)

    print('\nDone.\n')

    # Return just an output for now
    return 'Analyzed video should be saved...'

# Call the funtion
if len(sys.argv) >= 3 and len(sys.argv) <= 4:
    video_name = sys.argv[1]
    calls = []
    for i in range(2,len(sys.argv)):
        call = sys.argv[i]
        social_distancing_detection(video_name, call, storage_online, blur_faces)
        calls.append(call)
else:
    print('Please make sure the format is as follows: "python main.py [VIDEO_NAME] [DETECTION_CALL_1] (optional)[DETECTION_CALL_2]"\n')
    print('For example: "python main.py peope-detection PERSON_DETECTION HOG_OPENCV"')

# COMPARISON - If you have  put in more than one call, a comparison file will be made between the 2
if len(calls) > 1:
    print('\nDisplaying comparison of '+calls[0]+' and '+calls[1]+'...')
    comparisonVisualizer.show_comparison(video_name, calls)