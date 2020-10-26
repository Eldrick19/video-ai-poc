# When running this script locally, please enter the name of the video as an additional argument (i.e. "name".mp4 - dont include mp4)
# Make sure the mp4 video in question is in the \videos\input folder
# For example, a call could be 'python main.py sep-8-2011-propsal'

# Import Libraries
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from extraction import personTrackingExtractor, personTrackingExtractor2, personTrackingExtractor3, frameBoxesExtractor
from algorithms import socialDistancingTagger
from data import bqJobHelper
from frontend import outputVisualizer
from pathlib import Path
import pandas as pd
import sys
import time

def social_distancing_detection(video_name, storage_online, call, blur_faces):
    # Define important variables
    if storage_online: # Get video files from Cloud Storage
        print('\nYou decided to pull video from from Cloud Storage.')
        video_path = ['gs://test-bucket-1997/input/', video_name + '.mp4']
        output_path = ['videos/output/', video_name + '.avi']
        data_path = ['videos/data/', video_name + '.xlsx']
    else: # Get video files locally
        print('\nYou decided to pull video locally from "videos/input/" folder.')
        video_path = ['videos/input/', video_name + '.mp4']
        output_path = ['videos/output/', video_name + '.avi']
        data_path = ['videos/data/', video_name + '.xlsx']

    fps, frame_count, video_dimensions = frameBoxesExtractor.get_video_data(video_path)
  
    # EXTRACTION - Extract person tracking data using Google API
    print('\nCalling Video Intelligence API with feature '+call+'...')
    start_time = time.time()
    if call == 'PERSON_DETECTION':
        person_tracking_array = personTrackingExtractor.detect_person(video_path, storage_online)
    elif call == 'OBJECT_TRACKING':
        person_tracking_array = personTrackingExtractor2.detect_person(video_path, storage_online)
    elif call == 'HOG_OPENCV':
        person_tracking_array = personTrackingExtractor3.detect_person(video_path, fps, video_dimensions)
    detection_df = pd.DataFrame(person_tracking_array, columns=['d_id','start_s', 'left', 'top', 'right', 'bottom'])
    detection_df.to_excel(''.join(data_path),sheet_name='0')  # Exporting dataframe to CSV            

    # EXTRACTION - Perform light data manipulation
    start_time = time.time()
    detection_df = detection_df.sort_values(by=['start_s']) # Sort by Start time
    detection_df = detection_df.reset_index(drop=True)
    detection_df['start_s'] = detection_df['start_s'].multiply(fps) # Convert to frames
    detection_df.rename(columns={"start_s": "start_f"}, inplace=True) # Rename columns to describe fps

    # EXTRACTION - Perform heavier data manipulation. Gets all bounding boxes to be displayed at each frame
    print('\nHeavy data manipulation (bounding box at each frame)...')
    frame_detections = frameBoxesExtractor.detections_at_each_frame(detection_df, frame_count, video_dimensions, fps)
    detection_interval = frameBoxesExtractor.detection_frame_interval(frame_detections, call)
    
    # ALGORITHMS - Highlight all instances of non social distancing
    print('\nRunning social distanding algorithms...')
    start_time = time.time()
    frame_detections = socialDistancingTagger.tag_social_distancing(frame_detections, video_dimensions)

    # DATA - Persist the social distancing data to BigQuery
    print('\nSaving social distancing data to the Cloud...')
    for detection in frame_detections:
        detection['video_name'] = video_name
    sd_df = pd.DataFrame(frame_detections)
    bqJobHelper.push_to_bq(sd_df)

    # FRONTEND - Display person tracking
    print('\nDisplaying Results...')
    start_time = time.time()
    outputVisualizer.draw_detections(video_path, output_path, frame_detections, fps, video_dimensions, detection_interval, blur_faces)

    print('\nDone.\n')

    # Return just an output for now
    return 'Video should be uploaded...'

# Call the funtion
if len(sys.argv) > 1:
    video_name = sys.argv[1]
    storage_online = False
else:
    video_name = 'one-by-one-person-detection'
    storage_online = True

social_distancing_detection(video_name, storage_online, 'HOG_OPENCV', blur_faces=True)