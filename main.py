# When running this script please enter the name of the video as an additional argument (i.e. "name".mp4 - dont include mp4)
# For example, a call could be 'python main.py sep-8-2011-propsal'

# Import Libraries
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from extraction import personTrackingExtractor, personTrackingExtractor2, frameBoxesExtractor
from algorithms import socialDistancingTagger
from frontend import outputVisualizer
from infrastructure import tools
import pandas as pd
import sys

def social_distancing_detection(video_name, storage_online):
    # Define important variables
    if storage_online: # Get video files from Cloud Storage
        print('You decided to pull from from Cloud Storage.')
        video_path = ['gs://test-bucket-1997/input/', video_name + '.mp4']
        output_path = ['videos/output/', video_name + '.avi']
        data_path = ['videos/data/', video_name + '.csv']
    else: # Get video files locally
        print('File taken from local "videos/input/" folder.')
        video_path = ['videos/input/', video_name + '.mp4']
        output_path = ['videos/output/', video_name + '.avi']
        data_path = ['videos/data/', video_name + '.csv']


    # EXTRATION - Extract person tracking data
    print('\nCalling Video Intelligence API...\n')
    person_tracking_array = personTrackingExtractor2.detect_person(video_path, storage_online)
    detection_df = pd.DataFrame(person_tracking_array, columns=['start_s', 'end_s', 'left', 'top', 'right', 'bottom'])
    print(detection_df)

    # Exporting dataframe to CSV
    detection_df.to_csv(path_or_buf=''.join(data_path),index=False)

    # EXTRACTION - Perform light data manipulation
    detection_df.sort_values(by=['start_s']) # Sort by Start time
    fps, frame_count, video_dimensions = frameBoxesExtractor.get_video_data(video_path)
    detection_df['start_s'] = detection_df['start_s'].multiply(fps) # Convert to frames
    detection_df['end_s'] = detection_df['end_s'].multiply(fps) # Convert to frames 
    detection_df.rename(columns={"start_s": "start_f", "end_s": "end_f"}, inplace=True) # Rename columns to describe fps
    print(detection_df)

    # EXTRACTION - Perform heavier data manipulation 
    # Gets all bounding boxes to be displayed at each frame
    print('\nHeavy data manipulation (bounding box at each frame)... \n')
    detections_per_frame = frameBoxesExtractor.detections_at_each_frame(video_path, detection_df, fps, frame_count, video_dimensions)

    # ALGORITHMS - Highlight all instances of non social distancing
    frame_detections = socialDistancingTagger.tag_social_distancing(detections_per_frame, video_dimensions)
    for x, y in frame_detections.items():
        print(x, y)

    # FRONTEND - Display person tracking
    outputVisualizer.draw_detections(video_path, output_path, frame_detections, fps, video_dimensions)

    # Return just an output for now
    return 'Video should be uploaded to GitHub...'


# Call the funtion
if len(sys.argv) > 1:
    video_name = sys.argv[1]
    storage_online = False
else:
    video_name = 'one-by-one-person-detection'
    storage_online = True

social_distancing_detection(video_name, storage_online)