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


# randomly gen cards but do not repeat cards
def random_card():
    try:
        card = choice([i for i in range(0, 51) if i not in used_cards])
        used_cards.append(card)
        return card

    # error to return if try to draw from empty deck (should never happen in real game)
    except:
        raise IndexError("No cards left in deck; nothing to return")


# function to deal card to given player
def deal_card(player):
    # generates random card number
    rand_index = random_card()
    # checks if this is first card and who is receiving it (first cards have a specific x,y pair to use)
    if len(player.cards) == 0 and player.name == "player1":
        player.cards.append(obj.Card(card1_x, card1_y, imgs.card_names[rand_index], card_value(imgs.card_names[rand_index], player), rand_index))
    elif len(player.cards) == 0 and player.name == "dealer":
        player.cards.append(obj.Card(card2_x, card2_y, imgs.card_names[rand_index], card_value(imgs.card_names[rand_index], player), rand_index))
    # if not first card, just add it on top of last placed card
    else:
        player.cards.append(obj.Card((player.cards[len(player.cards) - 1].x + 40), (player.cards[len(player.cards) - 1].y - 20), imgs.card_names[rand_index], card_value(imgs.card_names[rand_index], player), rand_index))
    # print statement to debug dealing (not seen by player)
    print("Card dealt to {}!".format(player.name))


# use card name to determine value (removes last character and returns number, prints 10 if face card or 1 if Ace)
def card_value(name, player):
    simplified = name[:-1]
    if simplified in ["K", "Q", "J"]:
        return 10
    elif simplified == "A":
        player.aces += 1
        return 1
    else:
        return int(simplified)


# determine total point value of cards
def score(player):
    total_player = 0
    for card in player.cards:
        total_player += card.val
    return gameDisplay.blit(font.render('Player Total: {}'.format(total_player), True, white), (20, 20))


# initialize objects
objs = [
    obj.Button(display_width * 0.9, display_height * 0.87, 'deal'),
    obj.Button(display_width * 0.01, display_height * 0.86, 'hit'),
    obj.Button(display_width * 0.12, display_height * 0.86, 'stand')
]

# initialize players and deal first cards
# should add a players list to call players from (will be necessary when there are more players)
# possibly turn this into an 'initialization' function to call whenever needed? idk if that would be more efficient
player1 = obj.Player("player1", [], 0, 0)
dealer = obj.Player("dealer", [], 0, 0)
deal_card(player1)
deal_card(dealer)


# define function to draw objects
def drawObjs(object):
    if object.__class__ == obj.Card:
        gameDisplay.blit(imgs.cards[object.ind], (object.x, object.y))
    else:
        gameDisplay.blit(getattr(imgs, object.name), (object.x, object.y))


# defines setup function to be run at start of loop
def setup():
    # fills background with green (can potentially be changed to image file later)
    gameDisplay.fill(green)
    # iterates through lists and draws appropriate objects
    for obj in objs:
        drawObjs(obj)
    for card in player1.cards:
        drawObjs(card)
    for card in dealer.cards:
        drawObjs(card)
    # displays score for main player
    score(player1)


# define reset function
def reset():
    global player1
    global dealer
    global used_cards
    player1 = obj.Player("player1", [], 0, 0)
    dealer = obj.Player("dealer", [], 0, 0)
    used_cards = []
    deal_card(player1)
    deal_card(dealer)
    # FIXME: after running the reset function the deal_card function is broken (idk why yet)


# begin main game loop
def main(player, dealer):
    global END
    while not END:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                END = True

            # detect if mouse button is pressed on buttons (and call appropriate functions)
            if event.type == pyg.MOUSEBUTTONDOWN:
                # deal button
                if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 70) and (display_height * 0.87) <= mouse[1] <= ((display_height * 0.87) + 70):
                    reset()
                # hit button, generates new card and adds to card objects list
                if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
                    deal_card(player)
                    deal_card(dealer)
                # stand button
                if (display_width * 0.12) <= mouse[0] <= ((display_width * 0.12) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
                    deal_card(dealer)

        # call our setup function
        setup()

        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

        # update display
        pyg.display.update()
        clock.tick(60)


main(player1, dealer)
pyg.quit()
quit()
