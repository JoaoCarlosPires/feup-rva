import cv2
import numpy as np

from Constants import *

class Ui:
    def draw(self, frame, number_of_cards):
        if number_of_cards == NUM_PLAYERS:
            return frame

        frame = self.drawBackground(frame)
        frame = self.drawIdle(frame)

        return frame

    def drawIdle(self, frame):
        (frame_height, frame_width) = frame.shape[:2]
        text = "Waiting for all cards to be placed"
        textsize = cv2.getTextSize(text, FONT, TEXT_SIZE, 2)
        textX = int((frame_width / 2 - textsize[0][0] / 2))
        textY = int((frame_height / 2 + textsize[0][1] / 2))
        cv2.putText(frame, text, (textX, textY), FONT, TEXT_SIZE, COLOR_WHITE, 2)

        return frame

    def drawBackground(self, frame):
        x, y = 0, 0
        h, w = frame.shape[:2]
        overlay = frame.copy()
        overlay = cv2.rectangle(overlay, (x, y), (x + w, y + h), COLOR_BLACK, -1)

        alpha = UI_BACKGROUND_OPACITY
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        return frame
