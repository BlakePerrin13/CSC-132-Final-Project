# main game plays here

# import pygame and image files
import pygame as pyg
from random import choice
import ObjClasses as obj
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
white = (255, 255, 255)

# set font for pygame
font = pyg.font.Font('freesansbold.ttf', 32)

# initiates clock and end parameter
clock = pyg.time.Clock()
END = False

# how much the cards should be offset in x and y directions when new card is dealt
card_offset = 40


# defines function to display images (might be redundant whoops)
def display_img(img, x, y):
    gameDisplay.blit(img, (x, y))


# set x and y for first card dealt to player
card1_x = (display_width * 0.35)
card1_y = (display_height * 0.56)

# set x and y for first card dealt to dealer
card2_x = (display_width * 0.35)
card2_y = (display_height * 0.1)

# create list for used cards and counters for cards dealt to player/dealer
used_cards = []
cards_dealt_player = 0
cards_dealt_dealer = 0


# randomly gen cards but do not repeat cards
def random_card():
    try:
        card = choice([i for i in range(0, 51) if i not in used_cards])
        used_cards.append(card)
        return card
    
    # error to return if try to draw from empty deck (should never happen in real game)
    except:
        raise IndexError("No cards left in deck; nothing to return")


# use card name to determine value (removes last character and returns number, prints 10 if face card or 1 if Ace)
def card_value(name):
    simplified = name[:-1]
    if simplified in ["K", "Q", "J"]:
        return 10
    elif simplified == "A":
        return 1
    else:
        return int(simplified)


# determine total point value of cards
def score():
    total_player = 0
    for card in objs_cards_player:
        total_player += card.val
    return gameDisplay.blit(font.render('Player Total: {}'.format(total_player), True, white), (20, 20))


# initialize objects
objs = [
    obj.Button(display_width * 0.9, display_height * 0.87, 'deal'),
    obj.Button(display_width * 0.01, display_height * 0.86, 'hit'),
    obj.Button(display_width * 0.12, display_height * 0.86, 'stand')
]


# for player and dealer: gen random first card and initialize it
rand_index = random_card()
objs_cards_player = [
    obj.Card(card1_x, card1_y, imgs.card_names[rand_index], card_value(imgs.card_names[rand_index]), rand_index)
]

rand_index = random_card()
objs_cards_dealer = [
    obj.Card(card2_x, card2_y, imgs.card_names[rand_index], card_value(imgs.card_names[rand_index]), rand_index)
]


# define function to draw objects
def drawObjs(object):
    if object.__class__ == obj.Card:
        gameDisplay.blit(imgs.cards[object.ind], (object.x, object.y))
    else:
        gameDisplay.blit(getattr(imgs, object.name), (object.x, object.y))


# defines setup function to be run at start of loop
def setup():
    gameDisplay.fill(green)
    for obj in objs:
        drawObjs(obj)
    for card in objs_cards_player:
        drawObjs(card)
    for card in objs_cards_dealer:
        drawObjs(card)
    score()


# define reset function
def reset():
    global objs_cards_dealer
    global objs_cards_player
    global used_cards
    objs_cards_dealer = []
    objs_cards_player = []
    used_cards = []
    # TODO: MAKE DEAL CARD FUNCTION WITH "PERSON" PARAMETER -- takes list and deals card to it


# begin main game loop
def main(cards_dealt_player):
    global END
    while not END:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                END = True

            # detect if mouse button is pressed on buttons (and call appropriate functions)
            if event.type == pyg.MOUSEBUTTONDOWN:
                # deal button
                if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 70) and (display_height * 0.87) <= mouse[1] <= ((display_height * 0.87) + 70):
                    print("You pressed \'deal\'!")
                    reset()
                # hit button, generates new card and adds to card objects list
                if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
                    rand_index = random_card()
                    objs_cards_player.append(obj.Card((objs_cards_player[cards_dealt_player].x + 40), (objs_cards_player[cards_dealt_player].y - 20), imgs.card_names[rand_index], card_value(imgs.card_names[rand_index]), rand_index))
                    cards_dealt_player += 1
                # stand button
                if (display_width * 0.12) <= mouse[0] <= ((display_width * 0.12) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
                    print("You pressed \'stand\'!")

        # call our setup function
        setup()

        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

        # update display
        pyg.display.update()
        clock.tick(60)


main(cards_dealt_player)
pyg.quit()
quit()
