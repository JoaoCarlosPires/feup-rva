import cv2
import numpy as np
import os
import glob

from Card import *
from Orientation import *
from Constants import *

class CardDetection:

    def preprocessFrame(self, frame): # Preprocesses a frame and returns a thresh image of it
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Get black and white frame image
        imblur =  cv2.GaussianBlur(imgray, (5, 5), 0) # Apply a Gaussian Blur to the gray image
        ret, thresh = cv2.threshold(imblur, 127, 255, 0) # Get a thresh image from the blured image

        return thresh

    def findContours(self, thresh): # Find the and return the contours in a thresh image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Find the contours

        return contours, hierarchy

    def findCards(self, frame, contours): # Find all possible cards and return them
        cards = []
        counter = 0
        for c in contours: # For each contour found
            size = cv2.contourArea(c) # Calculate it's size
            peri = cv2.arcLength(c, True) # Calculate it's perimether
            approx = cv2.approxPolyDP(c, 0.01 * peri, True) # Get an approximation of a shape of the contour

            if self.isCard(size, peri, approx): # If it has 4 sides and is not too big neither too small it is a card

                cardCorners = np.array(approx) # Get the corners of the card

                x,y,w,h = cv2.boundingRect(c) # Get the x, y, width and height from the bounding rectangle of the countour

                orderedCardCorners, orientation = self.reorderCardCorners(cardCorners, w, h) # Order the corners in accordance to the cards rotation and get card's orientation

                cardFrameWarped = self.warpCard(frame, orderedCardCorners) # Warp the card to get a frontal view

                cardCenter = self.findCenterOfCard(cardCorners) # Calculate the center of the card

                card = Card(c, orderedCardCorners, cardCenter, size, peri, approx, cardFrameWarped, orientation) # Create new card with all the info we need

                cards.append(card) # Append it to the cards list

        return cards

    def isCard(self, size, peri, approx): # Check if a contour is a card
        if size > CARD_MIN_SIZE and size < CARD_MAX_SIZE and len(approx) == 4: # If it has 4 sides and is not too big neither too small it is a card
            return True
        else:
            return False

    def reorderCardCorners(self, corners, w, h): # Order the corners in accordance to the card's rotation
        s = np.sum(corners, axis = 2)
        tl = corners[np.argmin(s)]
        br = corners[np.argmax(s)]

        diff = np.diff(corners, axis = -1)
        tr = corners[np.argmin(diff)]
        bl = corners[np.argmax(diff)]

        orderedCardCorners = np.array([tl, tr, br, bl]) # Default value
        orientation = Orientation.VERTICAL # Default value

        if w <= 0.7*h: # Card is vertical
            orderedCardCorners = np.array([tl, tr, br, bl]) # Reorder corners
            orientation = Orientation.VERTICAL # Set orientation
        elif w >= 1.1*h: # Card is horizontal
            orderedCardCorners = np.array([bl, tl, tr, br]) # Reorder corners
            orientation = Orientation.HORIZONTAL # Set orientation
        else:
            if corners[1][0][1] <= corners[3][0][1]: # Card is tilted left
                orderedCardCorners = np.array([corners[1][0], corners[0][0], corners[3][0], corners[2][0]]) # Reorder corners
                orientation = Orientation.TILTED_LEFT # Set orientation
            else: # Card is tilted right
                orderedCardCorners = np.array([corners[0][0], corners[3][0], corners[2][0], corners[1][0]]) # Reorder corners
                orientation = Orientation.TILTED_RIGHT # Set orientation

        return orderedCardCorners, orientation

    def findCenterOfCard(self, corners): # Find the center point of the card
        average = np.sum(corners, axis=0)/len(corners)
        cent_x = int(average[0][0])
        cent_y = int(average[0][1])
        center = [cent_x, cent_y]

        return center

    def warpCard(self, frame, corners): # Warp the card to get a frontal view
        destCorners = np.array([[0, 0], [500, 0], [500, 726], [0, 726]]) # Define destination corners (a rectangle)
        homography, status = cv2.findHomography(corners, destCorners) # Find a Homography from the card's corners to the destination corners

        cardFrameWarped = cv2.warpPerspective(frame, homography, (500, 726)) # Apply the Homography

        return cardFrameWarped
