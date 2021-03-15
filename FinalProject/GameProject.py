# main game plays here

import pygame as pyg
import imgs


pyg.init()

display_width = 800
display_height = 600

gameDisplay = pyg.display.set_mode((display_width, display_height))
pyg.display.set_caption('Blackjack')

black = (0, 0, 0)
white = (255, 255, 255)
green = (34, 99, 43)

clock = pyg.time.Clock()
end = False


def display_img(img, x, y):
    gameDisplay.blit(img, (x, y))


x = (display_width * 0.35)
y = (display_height * 0.56)

while not end:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            end = True

    gameDisplay.fill(green)
    display_img(imgs.Four_H, x, y)

    pyg.display.update()
    clock.tick(60)

pyg.quit()
quit()
