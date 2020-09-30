import numpy as np
import pandas as pd
import cv2

# Gets FPS from video 
def get_video_data(video_path):
    video = cv2.VideoCapture(''.join(video_path))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video_dimensions = [video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT)]
    return fps, frame_count, video_dimensions

# Called to add a detection (in the form of a rectangle) to the list of detections that will be 'drawn' on a frame
def add_detection(rect_data, dim):
    rectangle = {
        "d_id": int(rect_data['d_id']),
        "left": round(rect_data['left']*dim[0]),
        "top": round(rect_data['top']*dim[1]),
        "right": round(rect_data['right']*dim[0]),
        "bottom": round(rect_data['bottom']*dim[1]),
    }
    
    return rectangle

def detection_frame_interval(detections_per_frame):
    interval = detections_per_frame[1][0] - detections_per_frame[0][0]
    return interval

def detections_at_each_frame(df, frame_count, dim, log=False):
    # Defining of variables
    fc, dc = 0, 0 # Frame Counter, Detection Counter Min, Detection Counter Max, and Unique ID, respectively
    detections_per_frame = []
    while(fc <= frame_count):   
        if log: print('\nOn Frame: ', fc, '| On Detection: ', dc,)
        if dc <= max(df.index) and round(df.loc[dc, 'start_f']) == fc:
            rectangles=[]
            while dc <= max(df.index) and round(df.loc[dc, 'start_f']) == fc:
                rect_data = df.iloc[dc]
                rectangles.append(add_detection(rect_data, dim))
                dc+=1
            detections_per_frame.append([fc, rectangles])
        else:
            fc+=1

    return detections_per_frame