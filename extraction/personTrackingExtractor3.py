import io
import math
import cv2


def detect_person(video_path, fps, dim, speed='FAST', log=False):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector())
    cap=cv2.VideoCapture(''.join(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    dim = [cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)]
    di = int(fps/2) # Detection interval, get detection every half a second
    fc = 0
    person_tracking_array = []
    while True:
        ret,frame=cap.read()
        if ret:
            if speed == 'FAST':
                detections,w=hog.detectMultiScale(frame, padding=(10,10), scale=1.02)
            if speed == 'SLOW':
                detections,w=hog.detectMultiScale(frame, winStride=(4,4), padding=(4,4), scale=1.02) 
            if len(detections) > 0:
                frame_s = fc/fps
                i = 0
                if log:
                    print(detections, w)
                    print(frame_s)
                for detection in detections:
                    if w[i] > 0.2:
                        left = detection[0]
                        top = detection[1]
                        right = detection[0]+detection[2]
                        bottom = detection[1]+detection[3]
                        person_tracking_array.append([0, frame_s, left, top, right, bottom])
                    i+=1
            fc+=1
            ch = 0xFF & cv2.waitKey(1)
            if ch == 27:
                break
        else:
            break
    cv2.destroyAllWindows()
        
    return person_tracking_array

def video_length_in_seconds(video_path):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    return clip.duration

def get_segments(video_length):
    import math
    time = 0.0
    segments = []
    while time <= video_length:
        start = time
        if time == math.floor(video_length): 
            end = video_length 
        else: 
            end = time + video_length/9
        start_s, start_n, end_s, end_n = int(start), int((start % 1) * 1e9), int(end), int((end % 1) * 1e9)
        print(start_s, start_n, end_s, end_n)
        segments.append([start_s, start_n, end_s, end_n])
        time+=video_length/9
    return segments

