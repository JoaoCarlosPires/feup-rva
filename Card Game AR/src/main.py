import cv2

from Calibration import *
from CardDetection import *
from CardMatching import *
from Card import *
from FpsCounter import *
from Ui import *
from Constants import *
from Markers import *
from Deck import *
from GameCard import *

# Calibrate the camera
calibration = Calibration(CHECKERBOARD_SIZE, CHECKERBOARD_PATH)
ret, matrix, distortion, r_vecs, t_vecs = calibration.calibrate()

vid = cv2.VideoCapture(VIDEO_CAPTURE) # Define a video capture object

cardDetection = CardDetection()

cardMatching = CardMatching()

fpsCounter = FpsCounter()

ui = Ui()

markers = Markers()

deck = Deck()

num_plays = 0
wins = [0, 0, 0, 0]

Trump = random.randrange(4)  # random trump
trump_suit = GameCard.suits[Trump]
Curr_hand = 0


wins[0] = []
wins[1] = []
wins[2] = []
wins[3] = []

print("The Trump suit is: ", trump_suit)

while(num_plays < 5):
    print(num_plays)
    ret, frame = vid.read() # Read frame from camera

    if num_plays == 4:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        arucoFound = markers.findArucoMarkers(frame)


        wins_len = [len(i) for i in wins]
        filename = 'player' + str(wins_len.index(max(wins_len))+1) +  '.jpg'
        augmentedImage = markers.loadAugImage('markers', filename)

        if len(arucoFound[0])!=0:
            for bbox in arucoFound[0]:
                # Find the rotation and translation vectors.
                rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(bbox, 6, matrix, distortion)
                # project 3D points to image plane
                imgpts, jac = cv2.projectPoints(objp, rvecs, tvecs, matrix, distortion)
                # draw the trohpy
                frame = markers.draw(frame,imgpts,augmentedImage)
    else:
        if SHOW_UI:
            frame = ui.draw(frame, number_of_cards)

        thresh = cardDetection.preprocessFrame(frame) # Obtain the thresh image by preprocessing the frame
        contours, hierarchy = cardDetection.findContours(thresh) # Get the contours of the thresh image

        possible_cards = cardDetection.findCards(frame, contours) # Detect possible cards from the contours

        cards = [] # Cards list

        for card in possible_cards: # For each possible card
            if cardMatching.match(card): # Try to match to card in our database
                cards.append(card) # If it is successfull then append it to the cards list

        number_of_cards = len(cards) # Save the number of matched cards

        if (number_of_cards == NUM_PLAYERS): # If the number of matched cards is equal to the number of players (finished play)
            cards = cardMatching.reorderCards(cards)

            aux_cards = []

            for i, card in enumerate(cards):
                cardName = card.getName()
                cardSuit = cardName.split(" of ")[1]
                cardRank = cardName.split(" of ")[0]
                currCard = GameCard()
                cardSuitNr, cardRankNr = currCard.getSuitRankNr(cardSuit, cardRank)
                if i == 0:
                    Curr_hand = cardSuitNr
                currCard = GameCard(Trump, Curr_hand, cardSuitNr, cardRankNr)
                aux_cards.append(currCard)

            winner_card = deck.wincard(aux_cards)  # check for winner card
            winner_player = aux_cards.index(winner_card)

            winner_card = cards[winner_player] #[ace of ..., seven ..., ... , ...]

            if num_plays in wins[winner_player]:
                wins[winner_player].append(num_plays)
            for i, card in enumerate(cards):
                if winner_card == card:
                    card.setWinner() # Change card's color
                else:
                    card.setLoser() # Change card's color

        for i, card in enumerate(cards): # For each card
            frame = card.draw(frame) # Draw card info

            if SHOW_WARP:
                card.drawWarp('cardWarped' + str(i)) # Draw card warp in a new window

    if SHOW_FPS:
        fpsCounter.draw(frame) # Draw an FPS counter

    cv2.imshow('frame', frame) # Display the resulting frame

    if cv2.waitKey(1) & 0xFF == ord(NEXT_KEY): # If user moves to next play
        num_plays += 1

    if cv2.waitKey(2) & 0xFF == ord(QUIT_KEY): # If user clicks in the QUIT_KEY the program will close
        break


vid.release() # Release the cap object
cv2.destroyAllWindows() # Destroy all the windows
