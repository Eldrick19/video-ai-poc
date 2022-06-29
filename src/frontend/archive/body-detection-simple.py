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
        #print('X = ', x, '| ', 'Y = ', y, '| ', 'W = ', w, '| ', 'H = ', h)
        #print('DETECTION[0] = ', rects[0])
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (255, 0, 0), thickness)

video_name = sys.argv[1]
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
cap=cv2.VideoCapture('C:/Users/eldri/Documents/GitHub/video-ai-poc/videos/input/'+video_name+'.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
dim = [cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)]
# Draw every X seconds
x, i, fc = 0.5, 0, 0
frame_wait = None
print('\nGetting Boxes at each Frame...\n')
while True:
    ret,frame=cap.read()
    if ret:
        if round(x*fps*i) == fc:
            print('Drawing for frame ', fc)
            found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
            draw_detections(frame,found)
            i+=1
            frame_wait = fc+1
        cv2.imshow('feed',frame)
        if fc == frame_wait:
            print('WAIT AT FRAME', frame_wait)
            time.sleep(1)
        fc+=1
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    else:
        break
cv2.destroyAllWindows()
print('\nGetting Done.\n')
