import numpy as np
import cv2

def show_comparison(video_name, calls):
    video_folder = 'videos/output/'
    output_path = ['videos/comparison/', video_name + '_' + calls[0] + '_' + calls[1] + '.avi']
    video1, video2 = video_folder + video_name + '_' + calls[0] + '.avi', video_folder + video_name + '_' + calls[1] + '.avi'
    cap = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)
    dim = [cap.get(cv2.CAP_PROP_FRAME_WIDTH)*2, cap.get(cv2.CAP_PROP_FRAME_HEIGHT)]
    out = cv2.VideoWriter(''.join(output_path), cv2.VideoWriter_fourcc(*"MJPG"), 15, (int(dim[0]),int(dim[1])))
    while(cap.isOpened()):
            ret,frame1=cap.read() 
            _,frame2=cap2.read() 
            if ret:
                both = np.hstack((frame1,frame2))
                cv2.imshow('frame',both)
                out.write(both)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            else:
                break

    cap.release()
    out.release
    cv2.destroyAllWindows()