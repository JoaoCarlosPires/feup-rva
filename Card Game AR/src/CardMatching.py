import cv2
import numpy as np
import os
import glob
import json

from Card import *
from Constants import *

class CardMatching:

    def __init__(self):
        self.loadCards() # Load cards information from our database

    def loadCards(self): # Load cards information from our database
        with open('cards.json') as json_file:
            data = json.load(json_file)
            for i, c in enumerate(data['cards']): # For each card in our database
                image = cv2.imread(CARDS_PATH + c['image']) # Read the card's image
                image = self.preprocessImage(image) # Preprocess the card's image to have a thresh image
                data['cards'][i]['preprocessedImage'] = image # Save this prepocessed image in our database
                imageRotated = cv2.rotate(image, cv2.ROTATE_180) # Rotate the prepocessed image by 180 degrees
                data['cards'][i]['preprocessedImageRotated'] = imageRotated # Also save the rotated prepocessed image

            self.data = data

    def preprocessImage(self, image): # Preprocesses a frame and returns a thresh image of it
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Get black and white frame image
        imblur =  cv2.GaussianBlur(imgray, (5, 5), 0) # Apply a Gaussian Blur to the gray image
        ret, thresh = cv2.threshold(imblur, 127, 255, 0) # Get a thresh image from the blured image

        return thresh

    def match(self, card): # Get the best match of a card detected in the frame with a card in our database. Return True if there is a match
        best_diff = MAX_DIFF # Define a max difference
        bestMatch = None

        cardImage = self.preprocessImage(card.getWarp()) # Preprocess the card's warped image to have a thresh image

        for c in self.data['cards']: # For each card in our database

            diff_img = cv2.absdiff(cardImage, c['preprocessedImage']) # Get the difference between the card's warped image and one from our database
            diff = np.sum(diff_img) / (len(diff_img) + 1) / 255

            if (diff < best_diff): # If this difference is better than what we have set it to be the best difference yet and do the same to the best match
                best_diff = diff
                bestMatch = c

            diff_img = cv2.absdiff(cardImage, c['preprocessedImageRotated']) # Get the difference between the card's warped image and one rotated image from our database
            diff = np.sum(diff_img) / (len(diff_img) + 1) / 255

            if (diff < best_diff): # If this difference is better than what we have set it to be the best difference yet and do the same to the best match
                best_diff = diff
                bestMatch = c

        if bestMatch == None: # If there is no good match return false
            return False

        card.setInfo(bestMatch['name'], bestMatch['rank'], bestMatch['suit'], bestMatch['value']) # If there is a good match set card's info and return true
        return True

    def reorderCards(self, cards):
        xs = []
        ys = []

        for card in cards:
            x, y = card.getCenter()
            xs.append(x)
            ys.append(y)

        leftCardIndex = xs.index(min(xs))
        rightCardIndex = xs.index(max(xs))
        topCardIndex = ys.index(max(ys))
        bottomCardIndex = ys.index(min(ys))

        cards = [cards[leftCardIndex], cards[topCardIndex], cards[rightCardIndex], cards[bottomCardIndex]]

        return cards
