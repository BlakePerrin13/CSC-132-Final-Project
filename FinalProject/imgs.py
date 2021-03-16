# file to save card files as images to open in game (de-clutters main loop)

import pygame as pyg

# cards
AC = pyg.transform.rotozoom(pyg.image.load('./card_images/AC.png'), 0, 0.2)
AD = pyg.transform.rotozoom(pyg.image.load('./card_images/AD.png'), 0, 0.2)

# buttons
deal = pyg.transform.rotozoom(pyg.image.load('./card_images/deal.png'), 0, 1)
hit = pyg.transform.rotozoom(pyg.image.load('./card_images/hit.png'), 0, 1.1)
stand = pyg.transform.rotozoom(pyg.image.load('./card_images/stand.png'), 0, 1.1)


