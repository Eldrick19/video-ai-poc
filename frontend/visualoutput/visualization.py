import numpy as np
import pandas as pd
import cv2

# Called to draw out detection box (rectangle) given image dimensions and box metrics
def draw_rectangle(img, rect, dim, thickness = 1):
    cv2.rectangle(img, (round(rect['left']*dim[0]), round(rect['top']*dim[1])), (round(rect['right']*dim[0]), round(rect['bottom']*dim[1])), (0, 255, 0), thickness)

# Gets FPS from video 
def get_fps(video_path):
    video = cv2.VideoCapture(''.join(video_path))
    fps = video.get(cv2.CAP_PROP_FPS)
    length = video.get(cv2.CAP_PROP_FRAME_COUNT)
    return fps

# Called to add a detection (in the form of a rectangle) to the list of detections that will be 'drawn' on a frame
def add_detections(rectangles, dc, fc, df):
    if round(df.loc[dc,'start_f']) == fc:
        rectangle = {
            "dc": dc,
            "left": df.loc[dc, 'left'],
            "top": df.loc[dc, 'top'],
            "right": df.loc[dc, 'right'],
            "bottom": df.loc[dc, 'bottom'],
            "end": df.loc[dc, 'end_f']
        }
        
        rectangles.append(rectangle)
        print('DC: ', dc)
        dc += 1

        rectangles, dc = add_detections(rectangles, dc, fc, df)

    return rectangles, dc

# Called to draw detections
def draw_detections(video_path, output_path, df, fps):
    # Defining of variables
    cap=cv2.VideoCapture(''.join(video_path))
    fc, dc = 0, 0 # Frame Counter and Detection Counter, respectively
    video_dimensions = [cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)]
    print(video_dimensions)
    rectangles = []

    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (int(video_dimensions[0]),int(video_dimensions[1])))

    # Loop through video capture and draw detections
    while(cap.isOpened()):
        ret,frame=cap.read() 

        if ret==True:
            # Add detections to list of detections to display
            if dc <= len(df.index):
                try:
                    rectangles, dc = add_detections(rectangles, dc, fc, df)
                except:
                    print('Arrived at last detection.')
            else:
                print('Arrived at last detection.')



            print('Show # of Rectangles: ', len(rectangles))

            # For each detection in list of detections to display do the following:
            # (1) Check if that detection has ended, if so remove it from list of detections to display
            # (2) Draw out the detections to display
            for rectangle in rectangles:
                if rectangle['dc'] <= dc and round(rectangle['end']) == fc:
                    rectangles.remove(rectangle)
                    continue
                draw_rectangle(frame, rectangle, video_dimensions)
            
            cv2.imshow('feed',frame)
            out.write(frame)
            fc += 1
            print('FC: ', fc)
        
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows() 
    print('Done')

