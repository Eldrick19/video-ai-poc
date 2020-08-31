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
def add_detections(rectangles, dc, fc, df, dim):
    if round(df.loc[dc,'start_f']) == fc:
        rectangle = {
            "dc": dc,
            "left": round(df.loc[dc, 'left']*dim[0]),
            "top": round(df.loc[dc, 'top']*dim[1]),
            "right": round(df.loc[dc, 'right']*dim[0]),
            "bottom": round(df.loc[dc, 'bottom']*dim[1]),
            "end": df.loc[dc, 'end_f']
        }
        
        rectangles.append(rectangle)
        dc += 1

        rectangles, dc = add_detections(rectangles, dc, fc, df, dim)

    return rectangles, dc


def detections_at_each_frame(video_path, df, fps, frame_count, dim):
    # Defining of variables
    fc, dc = 0, 0 # Frame Counter and Detection Counter, respectively
    rectangles = []
    detections_per_frame = []

    print(frame_count)
    while(fc <= frame_count):
        # Add detections to list of detections to display
        if dc <= len(df.index):
            try:
                rectangles, dc = add_detections(rectangles, dc, fc, df, dim)
            except:
                print('Arrived at last detection.')
        else:
            print('Arrived at last detection.')

        # For each detection in list of detections to display do the following:
        # (1) Check if that detection has ended, if so remove it from list of detections to display
        # (2) Add detections to the detection_pr_frame list
        for rectangle in rectangles:
            if rectangle['dc'] <= dc and round(rectangle['end']) == fc:
                rectangles.remove(rectangle)
                continue
            detections_per_frame.append([fc, rectangle]) # Note that the 0 is to initialize the social distancing variable. See socialDistancingTagger.py in the algorithms folder for more information
        
        fc += 1
    print(detections_per_frame)
    return detections_per_frame