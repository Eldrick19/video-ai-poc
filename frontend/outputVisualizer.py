import numpy as np
import pandas as pd
import cv2

# Called to draw out detection box (rectangle) given image dimensions and box metrics
def draw_rectangle(img, rect, dim, thickness = 1):
    if 'distance_alert' in rect:
        if rect['distance_alert'] == 1:
            cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (255, 0, 0), thickness)
        else:
            cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (0, 255, 0), thickness)
    else:
        cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (0, 255, 0), thickness)

# Called to draw detections
def draw_detections(video_path, output_path, detections, fps, dim):
    # Defining of variables
    cap=cv2.VideoCapture(''.join(video_path))
    fc= 0 # Frame Counter and Detection Counter, respectively

    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (int(dim[0]),int(dim[1])))

    # Loop through video capture and draw detections
    while(cap.isOpened()):
        ret,frame=cap.read() 

        if ret==True:

            if fc in detections:
                print('Show # of Rectangles: ', len(detections[fc]))
                for rectangle in detections[fc]:
                    draw_rectangle(frame, rectangle, dim)
            else:
                print('Show # of Rectangles: ', 0)
            
            cv2.imshow('feed',frame)
            out.write(frame)
            print('FC: ', fc) 
            fc += 1       
            if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows() 
    print('Done')

