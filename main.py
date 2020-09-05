# When running this script locally, please enter the name of the video as an additional argument (i.e. "name".mp4 - dont include mp4)
# Make sure the mp4 video in question is in the \videos\input folder
# For example, a call could be 'python main.py sep-8-2011-propsal'

# Import Libraries
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from extraction import personTrackingExtractor, personTrackingExtractor2, frameBoxesExtractor
from algorithms import socialDistancingTagger
from frontend import outputVisualizer
from infrastructure import tools
from pathlib import Path
import pandas as pd
import openpyxl
import sys
import time



def social_distancing_detection(video_name, storage_online, call):
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

    if not Path(''.join(data_path)).is_file():
        # EXTRACTION - Extract person tracking data using Google API
        print('\nCalling Video Intelligence API with feature '+call+'...')
        start_time = time.time()
        if call == 'PERSON_DETECTION':
            person_tracking_array = personTrackingExtractor.detect_person(video_path, storage_online)
        elif call == 'OBJECT_TRACKING':
            person_tracking_array = personTrackingExtractor2.detect_person(video_path, storage_online)
        detection_df = pd.DataFrame(person_tracking_array, columns=['d_id','start_s', 'left', 'top', 'right', 'bottom'])
        detection_df.to_excel(''.join(data_path),sheet_name='0')  # Exporting dataframe to CSV
        # Save runtime data
        if storage_online == False:
            api_runtime = time.time() - start_time
            runtime_df = pd.DataFrame(columns=['function', 'runtime_s'])
            runtime_df = runtime_df.append({'function': 'api_call_'+call, 'runtime_s': api_runtime}, ignore_index=True)              
    else:
        detection_df = pd.read_excel(''.join(data_path),sheet_name='0')
        runtime_df = pd.read_excel(''.join(data_path),sheet_name='1')
        if 'api_call_'+call not in list(runtime_df['function']): # EXTRACTION - Data has already been extracted but not using the new call
            print('\nData already extracted for this video, but not using the '+call+' call. Calling Video Intelligence API with feature '+call+'...')
            start_time = time.time()
            if call == 'PERSON_DETECTION':
                person_tracking_array = personTrackingExtractor.detect_person(video_path, storage_online)
            elif call == 'OBJECT_TRACKING':
                person_tracking_array = personTrackingExtractor2.detect_person(video_path, storage_online)
            detection_df = pd.read_excel(''.join(data_path),sheet_name='0')
            if storage_online == False:
                api_runtime = time.time() - start_time
                runtime_df = pd.read_excel(''.join(data_path),sheet_name='1')
                runtime_df = runtime_df.append({'function': 'api_call_'+call, 'runtime_s': api_runtime}, ignore_index=True) 
        else: # EXTRACTION - If it has already been extracted, just get from saved data
            print('\nData already extracted for this video using the '+call+' call. No need to call API.')



    # EXTRACTION - Perform light data manipulation
    start_time = time.time()
    detection_df = detection_df.sort_values(by=['start_s']) # Sort by Start time
    detection_df = detection_df.reset_index(drop=True)
    fps, frame_count, video_dimensions = frameBoxesExtractor.get_video_data(video_path)
    detection_df['start_s'] = detection_df['start_s'].multiply(fps) # Convert to frames
    detection_df.rename(columns={"start_s": "start_f"}, inplace=True) # Rename columns to describe fps

    # EXTRACTION - Perform heavier data manipulation. Gets all bounding boxes to be displayed at each frame
    print('\nHeavy data manipulation (bounding box at each frame)...')
    detections_per_frame = frameBoxesExtractor.detections_at_each_frame(detection_df, frame_count, video_dimensions)
    if storage_online == False:
        data_runtime = time.time() - start_time
        runtime_df = runtime_df.append({'function': 'data_manipulation', 'runtime_s': data_runtime}, ignore_index=True)


    # ALGORITHMS - Highlight all instances of non social distancing
    print('\nRunning social distanding algorithms...')
    start_time = time.time()
    frame_detections = socialDistancingTagger.tag_social_distancing(detections_per_frame, video_dimensions)
    if storage_online == False:
        algo_runtime = time.time() - start_time
        runtime_df = runtime_df.append({'function': 'distancing_algorithms', 'runtime_s': algo_runtime}, ignore_index=True)

    # FRONTEND - Display person tracking
    print('\nDisplaying Results...')
    start_time = time.time()
    outputVisualizer.draw_detections(video_path, output_path, frame_detections, fps, video_dimensions)
    if storage_online == False:
        output_runtime = time.time() - start_time
        runtime_df = runtime_df.append({'function': 'video_output', 'runtime_s': output_runtime}, ignore_index=True)

    if storage_online == False:
        excelBook = openpyxl.load_workbook(''.join(data_path))
        with pd.ExcelWriter(''.join(data_path), engine='openpyxl') as writer:
            writer.book = excelBook
            writer.sheets = dict((ws.title, ws) for ws in excelBook.worksheets)
            runtime_df.to_excel(writer,'1', index=False)
            writer.save()

    print('\nDone.\n')

    # Return just an output for now
    return 'Video should be uploaded to GitHub...'


# Call the funtion
if len(sys.argv) > 1:
    video_name = sys.argv[1]
    storage_online = False
else:
    video_name = 'one-by-one-person-detection'
    storage_online = True

social_distancing_detection(video_name, storage_online, 'PERSON_DETECTION')