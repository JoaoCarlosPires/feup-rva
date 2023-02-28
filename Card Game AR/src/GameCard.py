class GameCard:
    suits = ["Clubs", "Diamonds", "Spades", "Hearts"]
    ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

    def __init__(self, trump=None, curr_hand=None, suit=0, rank=0):
        self.trump = trump
        self.curr_hand = curr_hand
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return '%s %s' % (GameCard.suits[self.suit], GameCard.ranks[self.rank])

    def __lt__(self, other):
        if self is None:
            return True
        elif other is None:
            return False
        elif self.suit == self.trump and other.suit == self.trump:
            t1 = self.rank
            t2 = other.rank
            return t1 < t2
        elif self.suit == self.trump:
            return False
        elif other.suit == self.trump:
            return True
        elif self.suit == self.curr_hand and other.suit == self.curr_hand:
            t1 = self.rank
            t2 = other.rank
            return t1 < t2
        elif self.suit == self.curr_hand:
            return False
        elif other.suit == self.curr_hand:
            return True
        else:
            t1 = self.rank, self.suit
            t2 = other.rank, other.suit
            return t1 < t2

    def getSuitRankNr(self, suit_nr, rank_nr):
        return self.suits.index(suit_nr), self.ranks.index(rank_nr)
