# This class is meant to save and edit the parameters for tracking a person
# Note that tracking components currently include the following:
# SEGMENT : the time segment during which a tracked person appears at a specific location. More details below
# BOX : the bounding box of a person being detected during a specific segment. More details below
# More components may be added as deemed necessary

class PersonTracker:

    def saveID(self, ID):
        self.id = ID

    # A segment will be defined by its start and end time. Originally in seconds.
    def saveSegmentInSeconds(self, start, end):
        self.segment = {}
        self.segment['start'] = start
        self.segment['end'] = end
    
    # A box is defined by the bounding elemnts. left and right are units on the X axis. top and bottom are units on the Y axis
    # The units are a decimal of the screnn (0-1)
    # More information found: https://googleapis.dev/python/videointelligence/latest/gapic/v1p3beta1/types.html
    def saveBox(self, left, top, right, bottom):
        self.box = {}
        self.box['left'] = left
        self.box['top'] = top
        self.box['right'] = right
        self.box['bottom'] = bottom


    def convertSegmentsToFrameUnits(self, fps):
        self.segment_frames = {}
        self.segment_frames['start'] = self.segment['start']*fps
        self.segment_frames['end'] = self.segment['end']*fps
    