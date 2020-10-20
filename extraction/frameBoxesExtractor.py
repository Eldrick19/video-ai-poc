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
def add_detection(rect_data, fc, dim):
    rectangle = {
        "frame": round(fc),
        "d_id": int(rect_data['d_id']),
        "left": round(rect_data['left']*dim[0]),
        "top": round(rect_data['top']*dim[1]),
        "right": round(rect_data['right']*dim[0]),
        "bottom": round(rect_data['bottom']*dim[1]),
    }
    
    return rectangle

def add_detection_opencv(rect_data, fc):
    rectangle = {
        "frame": round(fc),
        "d_id": int(rect_data['d_id']),
        "left": round(rect_data['left']),
        "top": round(rect_data['top']),
        "right": round(rect_data['right']),
        "bottom": round(rect_data['bottom']),
    }
    
    return rectangle

def detection_frame_interval(detections, call):
    if call == 'HOG_OPENCV':
        interval = 0
    else:
        i=0
        while detections[i]['frame'] == detections[0]['frame']:
            i+=1
        interval = detections[i]['frame'] - detections[0]['frame']
    
    return interval

def detections_at_each_frame(df, frame_count, dim, fps, log=False):
    # Defining of variables
    fc, dc = 0, 0 # Frame Counter, Detection Counter Min, Detection Counter Max, and Unique ID, respectively
    frame_detections = []
    while(fc <= frame_count): 
        if log: print('\nOn Frame: ', fc, '| On Detection: ', dc)
        if dc <= max(df.index) and round(df.loc[dc, 'start_f']) == fc:
            while dc <= max(df.index) and round(df.loc[dc, 'start_f']) == fc:
                rect_data = df.iloc[dc]
                frame_detections.append(add_detection_opencv(rect_data, fc))
                dc+=1
        else:
            fc+=1
    return frame_detections