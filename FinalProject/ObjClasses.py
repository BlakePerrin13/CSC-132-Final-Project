# a module for the object classes to be called in main

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# order specifies when card is played
# name is the name of the card i.e. AS (Ace of Spades)
# val specifies value of card i.e. King is 10
# ind tells the index in list of cards
class Card(Object):
    def __init__(self, x, y, name, val, ind):
        super().__init__(x, y)
        self.name = name
        self.val = val
        self.ind = ind

# basic class for buttons, pressed parameter might be useless right now idk
class Button(Object):
    def __init__(self, x, y, name, pressed=False):
        super().__init__(x, y)
        self.name = name
        self.pressed = pressed


# class to store player data, will be useful for if we add more players, also cleans up code
# cards refers to a list of cards (the hand)
class Player:
    def __init__(self, name, cards, aces, score, chips, bet, stand = False, bust=False, splitCards = [], splitAces = 0, splitScore = 0, splitBet = 0,  splitStand = False, splitBust = False, split = False, win = False):
        self.name = name
        self.cards = cards
        self.aces = aces
        self.score = score
        self.chips = chips
        self.bet = bet
        self.stand = stand
        self.bust = bust
        self.splitCards = splitCards
        self.splitAces = splitAces
        self.splitScore = splitScore
        self.splitBet = splitBet
        self.splitStand = splitStand
        self.splitBust = splitBust
        self.split = split
        self.win = win
