import numpy as np
import pandas as pd
import cv2

# Called to draw out detection box (rectangle) given image dimensions and box metrics
def draw_rectangle(img, rect, dim, thickness = 1):
    
    red, green, blue = (0, 0, 255), (0, 255, 0), (255, 0, 0)

    if 'distance_alert' in rect:
        if rect['distance_alert'] == 1:
            color=red
            cv2.circle(img, (rect['center']['x'],rect['center']['y']), 2, color, thickness)
            if 'line' in rect:
                cv2.line(img, (rect['line']['x1'], rect['line']['y1']), (rect['line']['x2'], rect['line']['y2']), color, thickness)
        else:
            color=green
            cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), color, thickness)
    else:
        color=green
    
    cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), color, thickness)
    cv2.putText(img, 'ID: '+str(rect['d_id']), (rect['left'], rect['top']+15), cv2.FONT_HERSHEY_SIMPLEX,  0.5, color, 2)

# Called to draw detections
def draw_detections(video_path, output_path, detections, fps, dim, log=False):
    # Defining of variables
    cap=cv2.VideoCapture(''.join(video_path))
    fc= 0 # Frame Counter and Detection Counter, respectively

    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (int(dim[0]),int(dim[1])))

    # Loop through video capture and draw detections
    while(cap.isOpened()):
        ret,frame=cap.read() 

        if ret:

            if fc in detections:
                if log: print('Show # of Rectangles: ', len(detections[fc]))
                for rectangle in detections[fc]:
                    draw_rectangle(frame, rectangle, dim)
            else:
                if log: print('Show # of Rectangles: ', 0)
            
            cv2.imshow('feed',frame)
            out.write(frame)
            fc += 1       
            if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

