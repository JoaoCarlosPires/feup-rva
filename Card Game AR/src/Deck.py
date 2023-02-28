import random
from GameCard import *

class Deck:
    def __init__(self):
        ...

    def wincard(self, cards):
        winner = cards[0]
        for card in cards:
            if winner < card:
                winner = card
        return winner
