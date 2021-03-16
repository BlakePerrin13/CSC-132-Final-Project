# a module for the object classes to be called in main

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Card(Object):
    def __init__(self, x, y, order, name, val):
        super().__init__(x, y)
        self.order = order
        self.name = name
        self.val = val


class Button(Object):
    def __init__(self, x, y, name, pressed=False):
        super().__init__(x, y)
        self.name = name
        self.pressed = pressed
