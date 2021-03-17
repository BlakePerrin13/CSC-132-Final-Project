# file to store all functions for the project
# helps to clean things up and make main loop easier to understand

import imgs
import GameProject as loop


def drawObjs(object):
    if object.__class__ == loop.obj.Card:
        loop.gameDisplay.blit(imgs.cards[object.ind], (object.x, object.y))
    else:
        loop.gameDisplay.blit(getattr(imgs, object.name), (object.x, object.y))


def setup():
    loop.gameDisplay.fill(loop.green)
    for obj in loop.objs:
        drawObjs(obj)
    for card in loop.objs_cards_player:
        drawObjs(card)
    loop.score()
