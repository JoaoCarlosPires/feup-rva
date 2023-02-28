import cv2
import time

from Constants import *

class FpsCounter():
    def __init__(self):
        self.prev_frame_time = 0 # used to record the time when we processed last frame
        self.new_frame_time = 0 # used to record the time at which we processed current frame

    def draw(self, frame): # Draw FPS counter (Only call after processing frame)
        self.new_frame_time = time.time() # time when we finish processing for this frame

        # Calculating the fps
        fps = 1/(self.new_frame_time-self.prev_frame_time)
        self.prev_frame_time = self.new_frame_time
        fps = str(int(fps))

        cv2.putText(frame, fps, FPS_MARGIN, FONT, FPS_SIZE, FPS_COLOR, 3, cv2.LINE_AA) # Display the FPS in the frame
