# main game plays here

# import pygame and image files
import pygame as pyg
import imgs


# initiate pygame
pyg.init()

# set display dimensions
display_width = 800
display_height = 600

# initiate display and caption
gameDisplay = pyg.display.set_mode((display_width, display_height))
pyg.display.set_caption('Blackjack')

# set color values
green = (34, 99, 43)

# initiates clock and end parameter
clock = pyg.time.Clock()
end = False

# how much the cards should be offset in x and y directions when new card is dealt
card_offset = 40


# defines function to display images (might be redundant whoops)
def display_img(img, x, y):
    gameDisplay.blit(img, (x, y))


# defines setup function to be run at start of loop
def setup():
    gameDisplay.fill(green)
    display_img(imgs.AC, card1_x, card1_y)
    display_img(imgs.deal, display_width * 0.9, display_height * 0.87)
    display_img(imgs.hit, display_width * 0.01, display_height * 0.86)
    display_img(imgs.stand, display_width * 0.12, display_height * 0.86)


# set x and y for first card dealt
card1_x = (display_width * 0.35)
card1_y = (display_height * 0.56)

# begin main game loop
while not end:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            end = True

    setup()

    pyg.display.update()
    clock.tick(60)

pyg.quit()
quit()
