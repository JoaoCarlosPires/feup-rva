import cv2

from Constants import *

class Card:
    def __init__(self, contour, corners, center, size, peri, approx, warp, orientation):
        self.contour = contour
        self.corners = corners
        self.center = center
        self.size = size
        self.peri = peri
        self.approx = approx
        self.warp = warp
        self.orientation = orientation

        self.name = "Not Found"
        self.rank = "Not Found"
        self.suit = "Not Found"
        self.value = None
        self.color = CARD_COLOR_IDLE

        _, _, width, height = cv2.boundingRect(contour)
        self.width = width
        self.height = height

    def draw(self, frame):
        # Draw the card's border
        if SHOW_CARD_BORDER:
            cv2.drawContours(frame, [self.contour], -1, self.color, 2)

        # Draw the card name on top of the card
        if SHOW_CARD_NAME:
            text = str(self.name)
            textsize = cv2.getTextSize(text, FONT, TEXT_SIZE, 2)
            textX = int((self.center[0] - textsize[0][0] / 2))
            textY = int((self.center[1] + textsize[0][1] / 2) - self.height / 2 - CARD_TEXT_MARGIN)
            cv2.putText(frame, text, (textX, textY), FONT, TEXT_SIZE, self.color, 2)

        # Draw Winner or Loser in the center point of the card
        statusText = ""
        if self.color == CARD_COLOR_WINNER:
            statusText = "Winner"
        elif self.color == CARD_COLOR_LOSER:
            statusText = "Loser"
        textsize = cv2.getTextSize(statusText, FONT, TEXT_SIZE, 2)
        textX = int((self.center[0] - textsize[0][0] / 2))
        textY = int((self.center[1] + textsize[0][1] / 2))
        cv2.putText(frame, statusText, (textX, textY), FONT, TEXT_SIZE, self.color, 2)

        return frame


    def drawWarp(self, window): # Draw card warp in a new window
        # Resize image to 25%
        scale_percent = 25
        cardWarp = self.warp
        width = int(cardWarp.shape[1] * scale_percent / 100)
        height = int(cardWarp.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized = cv2.resize(cardWarp, dim)

        cv2.imshow(window, resized) # Show warp

    def getContour(self): # Get contour of Card
        return self.contour

    def getCorners(self): # Get corners of Card
        return self.corners

    def getCenter(self): # Get center point of Card
        return self.center

    def getSize(self): # Get size of Card
        return self.size

    def getPeri(self): # Get perimether of Card
        return self.peri

    def getApprox(self): # Get approx of Card
        return self.approx

    def getWarp(self): # Get warp of Card
        return self.warp

    def getOrientation(self): # Get orientation of Card
        return self.orientation

    def getValue(self): # Get value of Card
        return self.value

    def setValue(self, value): # Set color of Card
        self.value = value

    def setColor(self, color): # Set color of Card
        self.color = color

    def setInfo(self, name, rank, suit, value): # Set name, rank, suit and value of Card
        self.name = name
        self.rank = rank
        self.suit = suit
        self.value = value

    def setWinner(self): # Set card as Winner
        self.setColor(CARD_COLOR_WINNER) # Changes card's color to the winner color

    def setLoser(self): # Set card as Loser
        self.setColor(CARD_COLOR_LOSER) # Changes card's color to the loser color

    def getName(self): # Get name of Card
        return self.name
