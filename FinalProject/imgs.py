# file to save card files as images to open in game (de-clutters main loop)

import pygame as pyg
import os


# function to load cards as images given name
def card_load(name):
    card = pyg.transform.rotozoom(pyg.image.load('./card_images/{}.png'.format(name)), 0, 0.2)
    return card


# separate lists to store card images and names (same index in both lists is same card)
# it's gross but dictionaries don't work with loaded images oh well
cards = []
card_names = []

# iterate through folder and load all card images
for entry in os.listdir('./card_images/'):
    if len(entry) <= 7 and entry != 'hit.png':
        card_name = os.path.splitext(entry)[0]
        cards.append(card_load(card_name))
        card_names.append(card_name)

# buttons
deal = pyg.transform.rotozoom(pyg.image.load('./card_images/deal.png'), 0, 1)
hit = pyg.transform.rotozoom(pyg.image.load('./card_images/hit.png'), 0, 1.1)
stand = pyg.transform.rotozoom(pyg.image.load('./card_images/stand.png'), 0, 1.1)


