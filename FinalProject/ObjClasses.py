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
