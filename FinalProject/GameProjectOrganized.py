# main game plays here

# import pygame and image files
import pygame as pyg
from random import choice
import ObjClasses as obj
import imgs
##import RPi.GPIO as GPIO
from time import sleep

# Setup GPIO Blackjack Buttons
# Setup the GPIO pins 
##GPIO.setmode(GPIO.BCM)
##GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# defines function to display images (might be redundant whoops)
def display_img(img, x, y):
    gameDisplay.blit(img, (x, y))


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
    # check if player is busted, if so don't deal them
    if player.bust is True:
        pass
    # checks if this is first card and who is receiving it (first cards have a specific x,y pair to use)
    elif len(player.cards) == 0 and player.name == "player1":
        player.cards.append(obj.Card(card1_x, card1_y, imgs.card_names[rand_index], card_value(imgs.card_names[rand_index], player), rand_index))
    elif len(player.cards) == 0 and player.name == "dealer":
        player.cards.append(obj.Card(card2_x, card2_y, imgs.card_names[rand_index], card_value(imgs.card_names[rand_index], player), rand_index))
    # if not first card, just add it on top of last placed card
    else:
        player.cards.append(obj.Card((player.cards[len(player.cards) - 1].x + 40), (player.cards[len(player.cards) - 1].y - 20), imgs.card_names[rand_index], card_value(imgs.card_names[rand_index], player), rand_index))
    # print statement to debug dealing (not seen by player)
    print("Card dealt to {}! (if not busted)".format(player.name))


# use card name to determine value (removes last character and returns number, prints 10 if face card or 1 if Ace)
def card_value(name, player):
    simplified = name[:-1]
    if simplified in ["K", "Q", "J"]:
        return 10
    elif simplified == "A":
        if player.score > 10:
            return 1
        else:
            player.aces += 1
            return 11
    else:
        return int(simplified)


# determine total point value of cards for player
def player_score(player):
    global players
    if player.bust is False:
        n = len(player.cards)
        player.score += player.cards[n - 1].val
        if player.score > 21 and player.aces > 0:
            player.score -= 10
            player.aces -= 1
    bust_check(player)


# define function to draw objects
def drawObjs(object):
    if object.__class__ == obj.Card:
        gameDisplay.blit(imgs.cards[object.ind], (object.x, object.y))
    else:
        gameDisplay.blit(getattr(imgs, object.name), (object.x, object.y))


# defines setup function to be run at start of loop
def setup(players):
    # fills background with green (can potentially be changed to image file later)
    gameDisplay.fill(green)
    # iterates through lists and draws appropriate objects
    for obj in objs:
        drawObjs(obj)
    for p in players:
        for card in p.cards:
            drawObjs(card)
    gameDisplay.blit(font.render('Player Total: {}'.format(players[1].score), True, white), (20, 60))
    gameDisplay.blit(font.render('Dealer Total: {}'.format(players[0].score), True, white), (20, 20))


# define reset function
def reset():
    global used_cards
    global players
    used_cards = []
    for p in players:
        p.cards = []
        p.score = 0
        p.bet = 0
        p.aces = 0
        p.bust = False
        p.win = False
    initialization(players)
    main(players)


# button check functions:
def deal_button_check(mouse):
    if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 70) and (display_height * 0.87) <= mouse[1] <= ((display_height * 0.87) + 70):
        reset()


def hit_button_check(mouse):
    if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        hit()


def stand_button_check(mouse):
    if (display_width * 0.12) <= mouse[0] <= ((display_width * 0.12) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        # While dealers score is less than 18, dealer will keep hitting
        stand()

def split_button_check(mouse):
    if (display_width * 0.8) <= mouse[0] <= ((display_width * 0.8) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        print("Split")

# begin main game loop
def main(players):
    global END
    while not END:
##        if GPIO.input(18) == GPIO.HIGH:
##            reset()
##        if GPIO.input(19) == GPIO.HIGH:
##            hit()
##            sleep(0.5)
##        elif GPIO.input(20) == GPIO.HIGH:
##            stand()
##            
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                END = True

            # detect if mouse button is pressed on buttons (and call appropriate functions)
            if event.type == pyg.MOUSEBUTTONDOWN:
                # deal button
                deal_button_check(mouse)
                # hit button, generates new card and adds to card objects list
                hit_button_check(mouse)
                # stand button
                stand_button_check(mouse)
                # split button
                split_button_check(mouse)

        # call our setup function
        setup(players)

        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

        # update display
        pyg.display.update()
        clock.tick(60)


# initialize players and deal first cards
# TODO: later add way to generate a new player for every player in num_players
def initialization(players):
    setup(players)
    pyg.display.update()
    sleep(0.5)
    for p in players:
        if p.name == "dealer":
            continue
        bet(p)
    for i in range(2):
        for p in players:
            if p.name == "dealer":
                continue
            deal_card(p)
            player_score(p)
            sleep(0.5)
            setup(players)
            pyg.display.update()
        deal_card(players[0])
        player_score(players[0])
        sleep(0.5)
        setup(players)
        pyg.display.update()


def bust_check(player):
    if player.score > 21:
        player.bust = True


# TODO: Add win function that can end game and print winner (give option to play again)
def win_condition():
    for p in players:
        if p.name == "dealer":
            continue
        if p.bust is True:
            if p.chips == 0:
                p.chips = 100
            winner = players[0]
        elif players[0].bust == True:
            winner = p
        elif p.score > players[0].score and p.bust != True:
            winner = p
        else:
            winner = players[0]
        win(winner)


def win(player):
    if player.name == "dealer":
        print("Better Luck Next Time")
    else:
        print("Congratulations {}, you've won {} chips!".format(player.name, player.bet*2))
        player.chips = player.chips + player.bet*2
        print(player.chips)


def hit():
    deal_card(players[1])
    player_score(players[1])
    setup(players)
    pyg.display.update()
    sleep(0.5)
    if players[1].bust == True:
        stand()
    


def stand():
    sleep(0.5)
    if players[0].score < 17:
        deal_card(players[0])
        player_score(players[0])
        sleep(0.5)
        setup(players)
        pyg.display.update()
        stand()
    else:
        win_condition()

def bet(player):
    amount = int(input("How much would you like to bet. (Must be Less than or Equal to {}: ".format(player.chips)))
    if amount > player.chips:
        print("Invalid Bet. Must be Less than or Equal to {}".format(player.chips))
        bet(player)
    else:
        if amount == player.chips:
            player.chips = 0
        else:
            player.chips -= amount
        player.bet = amount
    print(player.bet)


################################################
################# Main Game ####################
################################################

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

# set x and y for first card dealt to player
card1_x = (display_width * 0.35)
card1_y = (display_height * 0.56)

# set x and y for first card dealt to dealer
card2_x = (display_width * 0.35)
card2_y = (display_height * 0.1)

# create list for used cards and counters for cards dealt to player/dealer
used_cards = []

# keep track of number of players (total players adds dealer)
num_players = 1
total_players = num_players + 1

# initialize objects
objs = [
    obj.Button(display_width * 0.9, display_height * 0.87, 'deal'),
    obj.Button(display_width * 0.01, display_height * 0.86, 'hit'),
    obj.Button(display_width * 0.12, display_height * 0.86, 'stand'),
    obj.Button(display_width * 0.8, display_height * 0.86, 'split')
]

# initialize players as a list
players = [
        obj.Player("dealer", [], 0, 0, 0, 0),
        obj.Player("player1", [], 0, 0, 1000, 0)
    ]
initialization(players)
main(players)
GPIO.cleanup()
pyg.quit()
quit()

