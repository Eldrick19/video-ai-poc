import io
import math
from google.cloud import videointelligence_v1p3beta1 as videointelligence
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration


def detect_person(video_path, storage_online, do_segments=False):
    """Detects people in a video."""

    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.OBJECT_TRACKING]

    # Grab video - choose from Cloud Storage or Local Storage
    if storage_online:
        input_content = video_path
    else:
        with io.open(''.join(video_path), "rb") as f:
            input_content = f.read()

    if do_segments:
        # Pass all segments to analyze (currently per second)
        segments = get_segments(video_length_in_seconds(''.join(video_path)))
        segment_config = []
        for segment in segments:
            start = Duration(seconds=segment[0],nanos=segment[1])
            print("Start: ", start, " | Type: ", type(start))
            end = Duration(seconds=segment[2],nanos=segment[3])
            print("End:", end, " | Type: ", type(end))
            segment_config.append(videointelligence.types.VideoSegment(
                start_time_offset=start,
                end_time_offset=end,
            ))

    # Configure the request
    config = videointelligence.types.LabelDetectionConfig(
        label_detection_mode='FRAME_MODE',
    )    

    #Specify Video Context
    if do_segments:
        context = videointelligence.types.VideoContext(
            segments=segment_config,
            label_detection_config=config,
        )
    else:
        context = videointelligence.types.VideoContext(
            label_detection_config=config,
        )

    # Start the asynchronous request - choose from Cloud Storage or Local Storage
    if storage_online:
        operation = client.annotate_video(
            input_uri=input_content, 
            features=features,
            video_context=context,
        )
    else:
        operation = client.annotate_video(
            input_content=input_content,
            features=features,
            video_context=context,
        )

    print("\nProcessing video for person detection annotations.")
    result = operation.result(timeout=300)

    print("\nFinished processing.\n")

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations
    person_tracking_array = []
    # Get only the first annotation for demo purposes.
    for object_annotation in object_annotations:
        if object_annotation.entity.description == 'person' and object_annotation.entity.entity_id:
            print("Entity description: {}".format(object_annotation.entity.description))
            print("Entity id: {}".format(object_annotation.entity.entity_id))
            # Obtain segment start and end times
            start = object_annotation.segment.start_time_offset.seconds + object_annotation.segment.start_time_offset.nanos / 1e9
            end = object_annotation.segment.end_time_offset.seconds + object_annotation.segment.end_time_offset.nanos / 1e9
            print(
                "Segment: {}s to {}s".format(
                    start,
                    end,
                )
            )

            print("Confidence: {}".format(object_annotation.confidence))

            # Here we print only the bounding box of the first frame in this segment
            frame = object_annotation.frames[0]
            box = frame.normalized_bounding_box
            print(
                "Time offset of the first frame: {}s".format(
                    frame.time_offset.seconds + frame.time_offset.nanos / 1e9
                )
            )
            print("Bounding box position:")
            print("\tleft  : {}".format(box.left))
            print("\ttop   : {}".format(box.top))
            print("\tright : {}".format(box.right))
            print("\tbottom: {}".format(box.bottom))
            print("\n")

            person_tracking_array.append([start, end, box.left, box.top, box.right, box.bottom])

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

