import math


# This function will (for the first iteration), tag each box within each frame to determine if the detected individual
# is social distancing or not:
# 0 - Social Distancing
# 1 - Not Social Distancing
def tag_social_distancing(detections, dim, log=False):

    # Initialize Variables
    frame_detections = {} # Will hold each frame detection data
    video_area = dim[0]*dim[1]

    for i in range(len(detections)):
        # Note the following (see frameBoxesExtractor.py for more information):
        # detections[i][0] = frame of video (int)
        # detections[i][1] = list of rectangles (list) each rectangle in the list is a dictionary

        current_frame = detections[i][0]
        rectangles = detections[i][1]
        rectangle_index = 0

        while rectangle_index < len(rectangles): # Will loop through all detections in a frame and compare it with all other detections
            rectangle_to_compare_1 = rectangles[rectangle_index]
            comparison_index = rectangle_index+1
            person_1_area = (rectangle_to_compare_1["right"]-rectangle_to_compare_1["left"])*(rectangle_to_compare_1["bottom"]-rectangle_to_compare_1["top"])
            percent_of_video_area_1 = person_1_area/video_area
            person_1_height = abs(rectangle_to_compare_1["top"]-rectangle_to_compare_1["bottom"])
            person_1_center_x = rectangle_to_compare_1["left"] + abs(rectangle_to_compare_1["left"]-rectangle_to_compare_1["right"])/2
            person_1_center_y = rectangle_to_compare_1["top"] + abs(rectangle_to_compare_1["top"]-rectangle_to_compare_1["bottom"])/2
        
            while comparison_index < len(rectangles): # Nested loop, compares all other detections in a frame to the 1st one. 
                rectangle_to_compare_2 = rectangles[comparison_index]
                person_2_area = (rectangle_to_compare_2["right"]-rectangle_to_compare_2["left"])*(rectangle_to_compare_2["bottom"]-rectangle_to_compare_2["top"])
                percent_of_video_area_2 = person_2_area/video_area
                person_2_center_x = rectangle_to_compare_2["left"] + abs(rectangle_to_compare_2["left"]-rectangle_to_compare_2["right"])/2
                person_2_center_y = rectangle_to_compare_2["top"] + abs(rectangle_to_compare_2["top"]-rectangle_to_compare_2["bottom"])/2
                if log:
                    print('Compare Rectangle 1: ', rectangle_to_compare_1, ' | Rectangle 2: ', rectangle_to_compare_2)
                    print('\nPercent of Video 1 ', percent_of_video_area_1, ' with 2 ', percent_of_video_area_2)
                    print('\nPercent Center 1 ', person_1_center_x, ' ', person_1_center_y, ' with 2 ', person_2_center_x, ' ', person_2_center_y)
                    print('\nPerson 1 area: ', ((rectangle_to_compare_1["right"]-rectangle_to_compare_1["left"])*(rectangle_to_compare_1["bottom"]-rectangle_to_compare_1["top"])), ' | Percent: ', percent_of_video_area_1)
                    print('Person 2 area: ', ((rectangle_to_compare_2["right"]-rectangle_to_compare_2["left"])*(rectangle_to_compare_2["bottom"]-rectangle_to_compare_2["top"])), ' | Percent: ', percent_of_video_area_2)
                    print('Video Area: ', video_area)

                #person_1_height = rectangle_to_compare_1["bottom"]-rectangle_to_compare_1["top"]
                #person_2_height = rectangle_to_compare_2["bottom"]-rectangle_to_compare_2["top"]
                if (person_1_area/person_2_area) >= 66.67 or (person_1_area/person_2_area) <= 0.6667: # If video area percentage difference is too large
                    comparison_index+=1
                    if log:
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
                
                comparison_index+=1
            
            rectangle_index+=1
        
        frame_detections[current_frame] = rectangles

    return frame_detections