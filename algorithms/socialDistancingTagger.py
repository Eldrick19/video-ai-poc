import math


# This function will (for the first iteration), tag each box within each frame to determine if the detected individual
# is social distancing or not:
# 0 - Social Distancing
# 1 - Not Social Distancing
# Loops through manipulated detections and analyzes distance between detections at each frame. 
# Adds “Distancing violation” tag if detections are deemed too close. Also adds “lines” and “center” so that they can be drawn between detections if needed
# INPUTS: 
# (1) detections (Lists of dictionaries) - list of dictionaries, where each dictionary describes a detection at a certain frame
# (2) dim (list with 2 values) - list that holds video dimensions [width,height]
# OUTPUT: detections (Lists of dictionaries) - list of dictionaries, where each dictionary describes a detection at a certain frame

def tag_social_distancing(detections, dim, log=False):

    # Initialize Variables
    video_area = dim[0]*dim[1]

        # Note the following (see frameBoxesExtractor.py for more information):
        # detections[i][0] = frame of video (int)
        # detections[i][1] = list of rectangles (list) each rectangle in the list is a dictionary

    rectangle_index = 0
    while rectangle_index < len(detections): # Will loop through all detections in a frame and compare it with all other detections
        rectangle_to_compare_1 = detections[rectangle_index]
        comparison_index = rectangle_index+1
        person_1_area = (rectangle_to_compare_1["right"]-rectangle_to_compare_1["left"])*(rectangle_to_compare_1["bottom"]-rectangle_to_compare_1["top"])
        percent_of_video_area_1 = person_1_area/video_area
        person_1_height = abs(rectangle_to_compare_1["top"]-rectangle_to_compare_1["bottom"])
        person_1_center_x = rectangle_to_compare_1["left"] + abs(rectangle_to_compare_1["left"]-rectangle_to_compare_1["right"])/2
        person_1_center_y = rectangle_to_compare_1["top"] + abs(rectangle_to_compare_1["top"]-rectangle_to_compare_1["bottom"])/2
    
        while comparison_index < len(detections) and detections[comparison_index]['frame'] == detections[rectangle_index]['frame']: # Nested loop, compares all other detections in a frame to the 1st one. 
            rectangle_to_compare_2 = detections[comparison_index]
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

            person_1_height = rectangle_to_compare_1["bottom"]-rectangle_to_compare_1["top"]
            person_2_height = rectangle_to_compare_2["bottom"]-rectangle_to_compare_2["top"]
            heights = [person_1_height, person_2_height]
            if (min(heights)/max(heights)) <= 0.70:  # If video area percentage difference is too large
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
                rectangle_to_compare_1["center"], rectangle_to_compare_2["center"] = '{"x":' + str(int(person_1_center_x)) + ',"y":' + str(int(person_1_center_y)) + '}', '{"x":' + str(int(person_2_center_x)) + ',"y":' + str(int(person_2_center_y)) + '}'
                rectangle_to_compare_1["line"] = '{"x1":' + str(int(person_1_center_x)) + ',"y1":' + str(int(person_1_center_y)) + ',"x2":' + str(int(person_2_center_x)) + ',"y2":' + str(int(person_2_center_y)) + '}'
            else:
                if "distance_alert" not in rectangle_to_compare_1:
                    rectangle_to_compare_1["distance_alert"] = 0
                if "distance_alert" not in rectangle_to_compare_2:
                    rectangle_to_compare_2["distance_alert"] = 0 
            
            comparison_index+=1
        
        rectangle_index = comparison_index

    return detections