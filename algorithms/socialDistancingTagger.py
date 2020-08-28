import math


# This function will (for the first iteration), tag each box within each frame to determine if the detected individual
# is social distancing or not:
# 0 - Social Distancing
# 1 - Not Social Distancing
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
                    print('\nComparing rectangle 1 ', rectangles[rectangle_index]["dc"], ' with 2 ', rectangles[comparison_index]["dc"])
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