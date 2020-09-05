import numpy as np
import cv2
import sys
import math
import time


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def tag_social_distancing(detections, dim):

    # Initialize Variables
    frame_detections = {} # Will hold each frame detection data
    rectangles = [] # Will hold list of detections (rectangle) at each frame
    current_frame = detections[0][0] # Initialize this as starting frame
    print('First frame: ', current_frame)
    video_area = dim[0]*dim[1]

    for i in range(len(detections)):
        # Note the following (see frameBoxesExtractor.py for more information):
        # detections[i][0] = frame of video (int)
        # detections[i][1] = rectangle data dictionary (dictionary)

        current_frame = detections[i][0]
        print('Current Detection: ', detections[i])
        if (i+1) == len(detections) or detections[i+1][0] > current_frame: # If next detection is on the next frame, perform calculations of distance before moving onto next frame
            rectangles.append(detections[i][1])
            print('Appending ', rectangles)
            print('End of frame ', current_frame, ' reached')
            rectangle_index = 0

            while rectangle_index < len(rectangles): # Will loop through all detections in a frame and compare it with all other detections
                rectangle_to_compare_1 = rectangles[rectangle_index]
                comparison_index = rectangle_index+1
                percent_of_video_area_1 = (rectangle_to_compare_1["left"]*rectangle_to_compare_1["bottom"])/video_area
                person_1_height = abs(rectangle_to_compare_1["top"]-rectangle_to_compare_1["bottom"])
                person_1_center_x = rectangle_to_compare_1["left"] + abs(rectangle_to_compare_1["left"]-rectangle_to_compare_1["right"])/2
                person_1_center_y = rectangle_to_compare_1["top"] + abs(rectangle_to_compare_1["top"]-rectangle_to_compare_1["bottom"])/2
                
                while comparison_index < len(rectangles): # Nested loop, compares all other detections in a frame to the 1st one. 
                    rectangle_to_compare_2 = rectangles[comparison_index]
                    percent_of_video_area_2 = (rectangle_to_compare_2["left"]*rectangle_to_compare_2["bottom"])/video_area
                    person_2_center_x = rectangle_to_compare_2["left"] + abs(rectangle_to_compare_2["left"]-rectangle_to_compare_2["right"])/2
                    person_2_center_y = rectangle_to_compare_2["top"] + abs(rectangle_to_compare_2["top"]-rectangle_to_compare_2["bottom"])/2
                    print('\nPercent of Video 1 ', percent_of_video_area_1, ' with 2 ', percent_of_video_area_2)
                    print('\nPercent Center 1 ', person_1_center_x, ' ', person_1_center_y, ' with 2 ', person_2_center_x, ' ', person_2_center_y)
                    
                    if abs(percent_of_video_area_1 - percent_of_video_area_2) >= 5: # If video area percentage difference is too large
                        print('Difference between boxes too large')
                        print('Person 1 area: ', percent_of_video_area_1)
                        print('Person 2 area: ', percent_of_video_area_2)
                        continue

                    # If video area percentage is not too large, find distance between points
                    distance_between_points = math.sqrt(pow((person_1_center_x-person_2_center_x),2)+pow((person_1_center_y-person_2_center_y),2))
                    if distance_between_points <= person_1_height:
                        rectangle_to_compare_1["distance_alert"], rectangle_to_compare_2["distance_alert"] = 1, 1
                        rectangle_to_compare_1["center"], rectangle_to_compare_2["center"] = {"x":int(person_1_center_x),"y":int(person_1_center_y)}, {"x":int(person_2_center_x),"y":int(person_2_center_y)}
                        rectangle_to_compare_1["line"] = {"x1":int(person_1_center_x),"y1":int(person_1_center_y),"x2":int(person_2_center_x),"y2":int(person_2_center_y)}
                    else:
                        if "distance_alert" not in rectangle_to_compare_1:
                            rectangle_to_compare_1["distance_alert"] = 0
                        if "distance_alert" not in rectangle_to_compare_2:
                            rectangle_to_compare_2["distance_alert"] = 0 
                    
                    print()
                    comparison_index+=1
                
                rectangle_index+=1
            
            frame_detections[current_frame] = rectangles
            rectangles = []
            
        else: # Else you are still on the same frame, add rectangle to list of rectangles for i frame
            rectangles.append(detections[i][1])
            print('Appending ', rectangles)

    return frame_detections

video_name = sys.argv[1]
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
cap=cv2.VideoCapture('C:/Users/eldri/Documents/GitHub/video-ai-poc/videos/input/'+video_name+'.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
dim = [cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)]
fc = 0
detections = []
# Draw every X seconds
x, i, fc = 1, 0, 0
print('\nGetting Boxes at each Frame...\n')
while True:
    ret,frame=cap.read()
    #print('\nFC: \n', fc)
    if ret:
        if round(x*fps*i) == fc:
            rectangles = []
            print('Drawing for frame ', fc)
            found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
            draw_detections(frame,found)
            i+=1
            if len(found) > 0:
                for detection in found:
                    rectangle = {
                        "left": detection[0],
                        "top": detection[1],
                        "right": detection[0]+detection[2],
                        "bottom": detection[1]+detection[3],
                    }
                    print(rectangle["left"], rectangle["top"], rectangle["right"], rectangle["bottom"])
                    detections.append([fc, rectangle])
        fc+=1
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    else:
        break
cv2.destroyAllWindows()
print('\nGetting Done.\n')
print(detections)

print('\nTagging Social Distancing...\n')
frame_detections = tag_social_distancing(detections, dim)
print('\nTagging Done.\n')


# Called to draw out detection box (rectangle) given image dimensions and box metrics
def draw_rectangle(img, rect, dim, thickness = 1):
    if 'distance_alert' in rect:
        if rect['distance_alert'] == 1:
            cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (0, 0, 255), thickness)
            cv2.circle(img, (rect['center']['x'],rect['center']['y']), 2, (0, 0, 255), thickness)
            if 'line' in rect:
                cv2.line(img, (rect['line']['x1'], rect['line']['y1']), (rect['line']['x2'], rect['line']['y2']), (0, 0, 255), thickness)
        else:
            cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (255, 0, 0), thickness)
    else:
        cv2.rectangle(img, (rect['left'], rect['top']), (rect['right'], rect['bottom']), (255, 0, 0), thickness)

# Called to draw detections
def draw_detections_2(video_path, output_path, detections, fps, dim):
    # Defining of variables
    cap=cv2.VideoCapture(''.join(video_path))
    fc= 0 # Frame Counter and Detection Counter, respectively

    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (int(dim[0]),int(dim[1])))

    # Loop through video capture and draw detections
    # Draw every X seconds
    x, i, fc = 1, 0, 0  
    frame_wait = None
    while(cap.isOpened()):
        ret,frame=cap.read() 

        if ret:
            if round(x*fps*i) == fc:
                frame_wait = fc+1
                if fc in detections:
                    print('Drawing for frame ', fc)
                    print('Show # of Rectangles: ', len(detections[fc]))
                    for rectangle in detections[fc]:
                        draw_rectangle(frame, rectangle, dim)
                i+=1
            
            if fc == frame_wait:
                j=0
                while j < 200:
                    cv2.imshow('feed',frame)
                    out.write(frame)
                    j+=1 
            cv2.imshow('feed',frame)
            out.write(frame)
            fc += 1       
            if cv2.waitKey(50) & 0xFF == ord('q'):
                    break
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows() 
    print('Done')

video_path = ['C:/Users/eldri/Documents/GitHub/video-ai-poc/videos/input/', video_name + '.mp4']
output_path = ['C:/Users/eldri/Documents/GitHub/video-ai-poc/videos/output/', video_name + '-HOG.avi']

input('Start video?\n')
draw_detections_2(video_path,output_path, frame_detections, fps, dim)

#draw_detections(frame,found)
#cv2.imshow('feed',frame)