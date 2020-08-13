# When running this script please enter the name of the video as an additional argument (i.e. "name".mp4 - dont include mp4)
# For example, a call could be 'python main.py sep-8-2011-propsal'

# Import Libraries
from extraction import personTrackingExtractor, personTrackingExtractor2
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from frontend.visualoutput.visualization import get_fps, draw_detections
from infrastructure import tools
import pandas as pd
import sys

# Define important variables
video_name = sys.argv[1]
# Getting video fies locally
video_path = ['videos/input/', video_name + '.mp4']
output_path = ['videos/output/', video_name + '.avi']

# Extract person tracking data
person_tracking_array = personTrackingExtractor2.detect_person(video_path)
detection_df = pd.DataFrame(person_tracking_array, columns=['start_s', 'end_s', 'left', 'top', 'right', 'bottom'])
print(detection_df)

# Perform light data manipulation
detection_df.sort_values(by=['start_s']) # Sort by Start time
fps = get_fps(video_path)
print(fps)
detection_df['start_s'] = detection_df['start_s'].multiply(fps) # Convert to frames
detection_df['end_s'] = detection_df['end_s'].multiply(fps) # Convert to frames 
detection_df.rename(columns={"start_s": "start_f", "end_s": "end_f"}, inplace=True) # Rename columns to describe fps
print(detection_df)

x = input('Proceed?')

# Display person tracking
draw_detections(video_path, output_path, detection_df, fps)
