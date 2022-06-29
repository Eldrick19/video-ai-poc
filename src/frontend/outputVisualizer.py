import numpy as np
import pandas as pd
import cv2
import json

def anonymize_detection_pixelate(pixelations, frame, rect, fc, blocks=3):
    # Definition of variables
    left, right, top, bottom = rect['left']-8, rect['right']+8, rect['top']-8, rect['bottom']-8
    bottom = round(top + (bottom-top)/3)
    region = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
    pixelation = frame[top:bottom, left:right]
    (h, w) = pixelation.shape[:2]
    xSteps = np.linspace(0, w, blocks + 1, dtype="int")
    ySteps = np.linspace(0, h, blocks + 1, dtype="int")
    # Loop over the blocks in both the x and y direction
    for i in range(1, len(ySteps)):
        for j in range(1, len(xSteps)):
            # Compute the starting and ending (x, y)-coordinates for the current block
            startX = xSteps[j - 1]
            startY = ySteps[i - 1]
            endX = xSteps[j]
            endY = ySteps[i]
            # Extract the ROI using NumPy array slicing, compute the mean of the ROI, and then draw a rectangle with the mean RGB values over the ROI in the original image
            roi = pixelation[startY:endY, startX:endX]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(pixelation, (startX, startY), (endX, endY),
                (B, G, R), -1)
    
    pixelations.append({'pixelation': pixelation, 'region': region, 'fc': fc})
    
    # return the pixelated blurred image
    return pixelations


def draw_rectangle(img, rect, dim, thickness = 8):
    # Definition of variables
    red, green, blue, white = (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 255)
    left, right, top, bottom = rect['left'], rect['right'], rect['top'], rect['bottom']
    # If there is a "distance_alert" tag, the check if the alert tag is 'on'
    color = green
    if 'distance_alert' in rect:
        # If tag = 1, then it is on. Draw it as a social distancing violation
        if rect['distance_alert'] == 1:
            color=red
            rect_center = json.loads(rect['center'])
            cv2.circle(img, (rect_center['x'],rect_center['y']), 2, color, thickness)
            if 'line' in rect and rect['line']:
                rect_line = json.loads(rect['line'])
                cv2.line(img, (rect_line['x1'], rect_line['y1']), (rect_line['x2'], rect_line['y2']), color, thickness)
    
    # Draw rectangle and ID
    cv2.rectangle(img, (left, top), (right, bottom), color, thickness)
    cv2.putText(img, 'ID: '+str(rect['d_id']), (left+15, top+20), cv2.FONT_HERSHEY_SIMPLEX,  0.5, color, 2)


# Draws detections analyzed by previously mentioned functions. Loops through each frame of video and leverages OpenCV. 
# Call draw_rectangle() and anonymize_detection_pixelate() which draw the detection boxes around people with ID’s and pixelate the face region, respectively.
# INPUTS:
# (1) video_path (list) - holds the video path in list format [FOLDER PATH, FILE_NAME]
# (2) output_path (list) - holds the video path of where the video will be output [FOLDER PATH, FILE_NAME]
# (3) detections (list of dictionaries) - list of dictionaries, where each dictionary describes a detection at a certain frame
# (4) fps (int) - frames per second of videos
# (5) dim (list 2 values) - holds video dimensions [WIDTH,HEIGHT]
# (6) detection_interval (int) - used to determine the interval between each detection in frames, useful variable for pixelation
# (7) blur_faces (Boolean) - Tag to determine if faces should be pixelized or not

def draw_detections(video_path, output_path, detections, fps, dim, detection_interval, blur_faces, log=False):
    # Definition of variables
    cap=cv2.VideoCapture(''.join(video_path))
    fc, dc = 0, 0 # Frame counter and detections counter
    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), 15, (int(dim[0]),int(dim[1])))
    pixelations = []

    # Loop through video capture and draw detections
    while(cap.isOpened()):
        ret,frame=cap.read() 

        if ret:
            df = 0
            while dc < len(detections) and fc == detections[dc]['frame']:
                if blur_faces: pixelations = anonymize_detection_pixelate(pixelations, frame, detections[dc], fc, 3)
                draw_rectangle(frame, detections[dc], dim)
                dc += 1
                df += 1
            if log: print('Show # of Rectangles: ', df)

            if blur_faces: 
                for p in pixelations:
                    if p['fc'] < fc-(detection_interval*2):
                        try: pixelations.remove(p)
                        except: 
                            if log: print('Some Pixelation Error')
                        continue
                    elif p['fc'] < fc-(detection_interval-1): 
                        continue
                    frame[p['region']['top']:p['region']['bottom'], p['region']['left']:p['region']['right']] = p['pixelation']
            
            cv2.imshow('feed',frame) ### COMMENT OUT THIS LINE TO NOT OUTPUT A VIDEO
            out.write(frame) 
            fc += 1       
            if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            
        else:
            break
    
    # End video streaming
    cap.release()
    out.release()
    cv2.destroyAllWindows()
