import cv2
import numpy as np
import os
import glob

CARD_MIN_SIZE = 3000
CARD_MAX_SIZE = 60000

def reorderCardCorners(corners, w, h):
    s = np.sum(corners, axis = 2)
    tl = corners[np.argmin(s)]
    br = corners[np.argmax(s)]

    diff = np.diff(corners, axis = -1)
    tr = corners[np.argmin(diff)]
    bl = corners[np.argmax(diff)]

    orderedCardCorners = np.array([tl, tr, br, bl])
    if w <= 0.8*h:
        orderedCardCorners = np.array([tl, tr, br, bl])
        #print('Card vertical')
    elif w >= 1.2*h:
        orderedCardCorners = np.array([bl, tl, tr, br])
        #print('Card horizontal')
    else:
        if corners[1][0][1] <= corners[3][0][1]:
            orderedCardCorners = np.array([corners[1][0], corners[0][0], corners[3][0], corners[2][0]])
            #print('Card tilted left')
        else:
            orderedCardCorners = np.array([corners[0][0], corners[3][0], corners[2][0], corners[1][0]])
            #print('Card tilted right')

    return orderedCardCorners

img = cv2.imread("C:/Users/joaos/Desktop/RVA/proj/cards2/cards6.jpg")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imblur =  cv2.GaussianBlur(imgray, (5, 5), 0)
ret, thresh = cv2.threshold(imblur, 127, 255, 0)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cards = []
for c in contours:
    size = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)

    if size > CARD_MIN_SIZE and len(approx) == 4:
        cards.append(c)

#cv2.drawContours(img, cards, -1, (255,255,0), 3)

destCorners = np.array([[0, 0], [500, 0], [500, 726], [0, 726]])

cardsWarped = []
for i,card in enumerate(cards):
    size = cv2.contourArea(card)
    peri = cv2.arcLength(card, True)
    approx = cv2.approxPolyDP(card, 0.01 * peri, True)

    corners = np.array(approx)
    x,y,w,h = cv2.boundingRect(card)
    reorderedCorners = reorderCardCorners(corners, w, h)

    homography, status = cv2.findHomography(reorderedCorners, destCorners)
    cardWarped = cv2.warpPerspective(img, homography, (500, 726))
    cardsWarped.append(cardWarped)

    cv2.imwrite("C:/Users/joaos/Desktop/RVA/proj/cards3/" + str(i+1+9+9+9+9+9+9) + ".png", cardWarped)

while (True):

    cv2.imshow('img', img)

    for i, card in enumerate(cardsWarped):
        cv2.imshow('card-'+str(i), card)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
