import cv2
import numpy as np

# Game
NUM_PLAYERS = 4

# Path
PATH = "C:/Users/joaoc/Desktop/cardDetection/RVA/"
CARDS_PATH = PATH + "cards2/"

# Camera
VIDEO_CAPTURE = 1

# Checkerboard
CHECKERBOARD_PATH = "./board/joaorocha/"
CHECKERBOARD_SIZE = (9,6)

# Settings
SHOW_FPS = False
SHOW_WARP = False
SHOW_CARD_NAME = True
SHOW_CARD_BORDER = True
SHOW_UI = False

# Text
FONT = cv2.FONT_HERSHEY_COMPLEX
TEXT_SIZE = 0.8

# UI
UI_BACKGROUND_OPACITY = 0.8

# Colors
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_CYAN = (255, 255, 0)

# Card
CARD_TEXT_MARGIN = 20
CARD_COLOR_IDLE = COLOR_CYAN
CARD_COLOR_WINNER = COLOR_GREEN
CARD_COLOR_LOSER = COLOR_RED

# Card Detection
CARD_MIN_SIZE = 3000
CARD_MAX_SIZE = 60000

# Card Matching
MAX_DIFF = 100

# Fps Counter
FPS_COLOR = COLOR_WHITE
FPS_MARGIN = (5, 20)
FPS_SIZE = 1

# Keys
QUIT_KEY = 'q'
NEXT_KEY = 'n'

# OBJECT POINTS
objp = np.array([np.array([-3, -3, 0], np.float32),
                np.array([3, -3, 0], np.float32),
                np.array([-3, 3, 0], np.float32),
                np.array([3, 3, 0], np.float32),
                np.array([-3, -3, 6], np.float32),
                np.array([3, -3, 6], np.float32),
                np.array([-3, 3, 6], np.float32),
                np.array([3, 3, 6], np.float32)])
