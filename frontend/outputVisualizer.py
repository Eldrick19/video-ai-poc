import numpy as np
import pandas as pd
import cv2

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
    if 'distance_alert' in rect:
        # If tag = 1, then it is on. Draw it as a social distancing violation
        if rect['distance_alert'] == 1:
            color=red
            cv2.circle(img, (rect['center']['x'],rect['center']['y']), 2, color, thickness)
            if 'line' in rect:
                cv2.line(img, (rect['line']['x1'], rect['line']['y1']), (rect['line']['x2'], rect['line']['y2']), color, thickness)
        # If tag NOT 1, then it is off. Draw it as a normal detection
        else:
            color=green
    # If no "distance_alert" tag, then draw as normal detection
    else:
        color=green
    
    # Draw rectangle and ID
    cv2.rectangle(img, (left, top), (right, bottom), color, thickness)
    cv2.putText(img, 'ID: '+str(rect['d_id']), (left+15, top+20), cv2.FONT_HERSHEY_SIMPLEX,  0.5, color, 2)


def draw_detections(video_path, output_path, detections, fps, dim, detection_interval, blur_faces, log=False):
    # Definition of variables
    cap=cv2.VideoCapture(''.join(video_path))
    fc= 0 # Frame counter
    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), 15, (int(dim[0]),int(dim[1])))
    pixelations = []

    # Loop through video capture and draw detections
    while(cap.isOpened()):
        ret,frame=cap.read() 

        if ret:

            if fc in detections:
                if log: print('Show # of Rectangles: ', len(detections[fc]))
                for rectangle in detections[fc]:
                    if blur_faces: pixelations = anonymize_detection_pixelate(pixelations, frame, rectangle, fc, 3)
                    draw_rectangle(frame, rectangle, dim)
            else:
                if log: print('Show # of Rectangles: ', 0)

            if blur_faces: 
                for p in pixelations:
                    if p['fc'] < fc-(detection_interval*2):
                        try: pixelations.remove(p)
                        except: print('Some Pixelation Error')
                        continue
                    elif p['fc'] < fc-(detection_interval-1): 
                        continue
                    frame[p['region']['top']:p['region']['bottom'], p['region']['left']:p['region']['right']] = p['pixelation']

            cv2.imshow('feed',frame)
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
