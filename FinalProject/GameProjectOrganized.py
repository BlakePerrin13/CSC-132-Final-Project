# main game plays here

# import pygame and image files
import pygame as pyg
from random import choice
import ObjClasses as obj
import imgs
from time import sleep

GPIO = False
if GPIO:
    import RPi.GPIO as GPIO
    #Setup GPIO Blackjack Buttons
    RESET = 18
    HIT = 19
    STAND = 20
    UP_ARROW = 12
    DOWN_ARROW = 6
    CONFIRM = 5
    # Setup the GPIO pins 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RESET, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HIT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(STAND, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(UP_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DOWN_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
# defines function to display images (might be redundant whoops)
def display_img(img, x, y):
    gameDisplay.blit(img, (x, y))


def display_text(text, x, y):
    gameDisplay.blit(font.render(text, True, white), (x, y))


# STUFF FOR PRINTING TEXT TO SCREEN
def print_text(text):
    message = font.render(text, True, black)
    message_rect = message.get_rect(center=(display_width/2, display_height/2))
    gameDisplay.blit(message, message_rect)


MESSAGE = ""


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
        player.cards.append(obj.Card(card1_x, card1_y, imgs.card_names[rand_index],
                                     card_value(imgs.card_names[rand_index], player), rand_index))
    elif len(player.cards) == 0 and player.name == "dealer":
        player.cards.append(obj.Card(card2_x, card2_y, imgs.card_names[rand_index],
                                     card_value(imgs.card_names[rand_index], player), rand_index))
    elif len(player.cards) == 1 and player.name == "dealer":
        player.cards.append(obj.Card((player.cards[len(player.cards) - 1].x + 40),
                                     (player.cards[len(player.cards) - 1].y - 20), "purple_back", 0, 52))
    elif len(player.cards) == 2 and player.name == "dealer" and player.cards[1].name == "purple_back":
        player.cards.remove(player.cards[1])
        player.cards.append(obj.Card((player.cards[len(player.cards) - 1].x + 40),
                                     (player.cards[len(player.cards) - 1].y - 20), imgs.card_names[rand_index],
                                     card_value(imgs.card_names[rand_index], player), rand_index))
    # if not first card, just add it on top of last placed card
    else:
        player.cards.append(obj.Card((player.cards[len(player.cards) - 1].x + 40),
                                     (player.cards[len(player.cards) - 1].y - 20), imgs.card_names[rand_index],
                                     card_value(imgs.card_names[rand_index], player), rand_index))
    # print statement to debug dealing (not seen by player)
    print("Card dealt to {}! (if not busted)".format(player.name))


def split_deal(player):
    rand_index = random_card()
    # check if player is busted, if so don't deal them
    if player.splitBust is True:
        pass
    else:
        player.splitCards.append(obj.Card((player.splitCards[len(player.splitCards) - 1].x + 40),
                                          (player.splitCards[len(player.splitCards) - 1].y - 20),
                                          imgs.card_names[rand_index], card_value(imgs.card_names[rand_index],
                                                                                  player), rand_index))
    # print statement to debug dealing (not seen by player)
    print("Card dealt to {} Split Hand! (if not busted)".format(player.name))


# use card name to determine value (removes last character and returns number, prints 10 if face card or 1 if Ace)
def card_value(name, player):
    simplified = name[:-1]
    if simplified in ["K", "Q", "J"]:
        return 10
    elif simplified == "A":
        if player.split is not True:
            if player.score > 10:
                return 1
            else:
                player.aces += 1
                return 11
        else:
            if player.splitScore > 10:
                return 1
            else:
                player.splitAces += 1
                return 11
    else:
        return int(simplified)


# determine total point value of cards for player
def player_score(player):
    global counter
    if player.bust is False:
        if counter == 0:
            n = len(player.cards)
            player.score += player.cards[n - 1].val
        if counter == 1:
            player.score = player.cards[0].val
            counter = 0
        if player.score > 21 and player.aces > 0:
            player.score -= 10
            player.aces -= 1
    bust_check(player)


def split_score(player):
    if player.splitBust is False:
        n = len(player.splitCards)
        if player.splitCards[0].name[:-1] == "A":
            player.splitCards[0].val = 11
            player.splitAces += 1
        player.splitScore += player.splitCards[n - 1].val
        if player.splitScore > 21 and player.splitAces > 0:
            player.splitScore -= 10
            player.splitAces -= 1
    split_bust_check(player)


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
        for card in p.splitCards:
            drawObjs(card)
    if players[1].split is False:
        display_text('Player Total: {}'.format(players[1].score), 20, 60)
    if players[1].split is True:
        display_text('Hand 2 Total: {}'.format(players[1].splitScore), 20, 100)
        display_text('Hand 1 Total: {}'.format(players[1].score), 20, 60)
    display_text('Bet: {}'.format(players[1].bet), 600, 60)
    display_text('Dealer Total: {}'.format(players[0].score), 20, 20)
    display_text('Chips: {}'.format(players[1].chips), 600, 20)
    print_text(MESSAGE)


# define reset function
def reset():
    global used_cards
    global players
    used_cards = []
    for p in players:
        p.cards = []
        p.aces = 0
        p.score = 0
        p.bet = 0
        p.stand = 0
        p.bust = False
        p.splitCards = []
        p.splitAces = 0
        p.splitScore = 0
        p.splitBet = 0
        p.splitStand = False
        p.splitBust = False
        p.split = False
        p.win = False
    initialization(players)
    main(players)


# button check functions:
def deal_button_check(mouse):
    if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 70) and (display_height * 0.87) <= mouse[1] <= \
            ((display_height * 0.87) + 70):
        reset()


def hit_button_check(mouse):
    if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.86) <= mouse[1] <= \
            ((display_height * 0.86) + 77):
        hit(players[1])


def stand_button_check(mouse):
    if (display_width * 0.12) <= mouse[0] <= ((display_width * 0.12) + 77) and (display_height * 0.86) <= mouse[1] <= \
            ((display_height * 0.86) + 77):
        # While dealers score is less than 18, dealer will keep hitting
        stand(players[1])


def split_button_check(mouse):
    if (display_width * 0.8) <= mouse[0] <= ((display_width * 0.8) + 77) and (display_height * 0.86) <= mouse[1] <= \
            ((display_height * 0.86) + 77):
        split(players[1])


# TODO ##########################################################################################
def increase_bet_check(mouse, p):
    if (display_width * 0.8) <= mouse[0] <= ((display_width * 0.8) + 77) and (display_height * 0.76) <= mouse[1] <= \
            ((display_height * 0.76) + 77):
        if p.bet_value == 5:
            p.bet_value = 0
        else:
            p.bet_value += 1
        p.bet = bets[p.bet_value]
        print("Increase")


def decrease_bet_check(mouse, p):
    if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 77) and (display_height * 0.76) <= mouse[1] <= \
            ((display_height * 0.76) + 77):
        if p.bet_value == 0:
            p.bet_value = 5
        else:
            p.bet_value -= 1
        p.bet = bets[p.bet_value]
        print("Decrease")


def set_bet_check(mouse, player):
    if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.76) <= mouse[1] <= \
            ((display_height * 0.76) + 77):
        player.chips -= player.bet
        print("Bets placed")
        return True


# begin main game loop ############################################################################################
def main(players):
    global END
    while not END:
        if GPIO:
            if GPIO.input(RESET) == GPIO.HIGH:
                reset()
            if GPIO.input(HIT) == GPIO.HIGH:
                hit(players[1])
                sleep(0.5)
            elif GPIO.input(STAND) == GPIO.HIGH:
                stand(players[1])

        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

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

        # update display
        pyg.display.update()
        clock.tick(60)


# initialize players and deal first cards
# TODO: later add way to generate a new player for every player in num_players
def initialization(players):
    global MESSAGE
    MESSAGE = ""
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
        if i < 1:
            deal_card(players[0])
            player_score(players[0])
            sleep(0.5)
            setup(players)
            pyg.display.update()
    deal_card(players[0])


# TODO ######################################################################################################
def bust_check(player):
    if player.score > 21:
        player.bust = True


def split_bust_check(player):
    if player.splitScore > 21:
        player.splitBust = True


def win_condition():
    global MESSAGE
    for p in players:
        if p.name == "dealer":
            continue
        if p.score == 21:
            MESSAGE = "You hit Blackjack! You have recieved {} chips.".format(int(p.bet*2.5))
            p.chips += int(p.bet*2.5)
            print(p.chips)
            if p.split is False:
                continue
        elif players[0].bust is True:
            if p.bust is True:
                if p.chips == 0:
                    p.chips = 100
                MESSAGE = "Better luck next time!"
            elif p.bust is not True:
                MESSAGE = "Congratulations {}, you've won {} chips!".format(p.name, int(p.bet*2))
                p.chips += int(p.bet*2)
                print(p.chips)
        else:
            if p.bust != True:
                if p.score == players[0].score:
                    MESSAGE = "Push! You have recieved {} chips.".format(int(p.bet))
                    p.chips += p.bet
                    print(p.chips)
                elif p.score > players[0].score:
                    MESSAGE = "Congratulations {}, you've won {} chips!".format(p.name, int(p.bet*2))
                    p.chips += int(p.bet*2)
                    print(p.chips)
                elif p.score < players[0].score:
                    if p.chips == 0:
                        p.chips = 100
                    MESSAGE = "Better luck next time!"
            elif p.bust == True:
                if p.chips == 0:
                    p.chips = 100
                MESSAGE = "Better luck next time!"
                
                
        if p.split is True:
            if p.splitScore == 21:
                MESSAGE = "You hit Blackjack! You have recieved {} chips.".format(int(p.bet*2.5))
                p.chips += int(p.bet*2.5)
                print(p.chips)
                continue
            elif players[0].bust is True:
                if p.splitBust is True:
                    if p.chips == 0:
                        p.chips = 100
                    MESSAGE = "Better luck next time!"
                elif p.splitBust is not True:
                    MESSAGE = "Congratulations {}, you've won {} chips!".format(p.name, int(p.bet*2))
                    p.chips += int(p.bet*2)
                    print(p.chips)
            else:
                if p.splitBust != True:
                    if p.splitScore == players[0].score:
                        MESSAGE = "Push! You have recieved {} chips.".format(int(p.bet))
                        p.chips += p.bet
                        print(p.chips)
                    elif p.splitScore > players[0].score:
                        MESSAGE = "Congratulations {}, you've won {} chips!".format(p.name, int(p.splitbet*2))
                        p.chips += int(p.bet*2)
                        print(p.chips)
                    elif p.splitScore < players[0].score:
                        if p.chips == 0:
                            p.chips = 100
                        MESSAGE = "Better luck next time!"
                elif p.splitBust == True:
                    if p.chips == 0:
                        p.chips = 100
                    MESSAGE = "Better luck next time!"
                    

def win(player):
    global MESSAGE
    if player.name == "dealer":
        MESSAGE = "Better luck next time!"
    elif player.score == players[0].score:
        if player.score == 21:
            MESSAGE = "You hit Blackjack! You have recieved {} chips.".format(player.bet*1.5)
            player.chips += player.bet*1.5
            print(player.chips)
        else:
            MESSAGE = "Push, you have recieved {} chips.".format(player.bet)
            player.chips += player.bet
            print(player.chips)
    else:
        if player.score == 21:
            MESSAGE = "You hit Blackjack! You have recieved {} chips.".format(player.bet*1.5 + player.bet)
            player.chips += player.bet*1.5
            print(player.chips)
        else: 
            MESSAGE = "Congratulations {}, you've won {} chips!".format(player.name, player.bet*2)
            player.chips += player.bet*2
            print(player.chips)


def hit(player):
    if player.stand is True and player.split is True:
        split_deal(player)
        split_score(player)
        setup(players)
        pyg.display.update()
        sleep(0.5)
        if player.splitBust is True:
            stand(player)
    else:   
        deal_card(player)
        player_score(player)
        setup(players)
        pyg.display.update()
        sleep(0.5)
        if players[1].bust is True and players[1].split is not True:
            stand(players[0])


def stand(player):
    sleep(0.5)
    if player.stand is True:
        player.splitStand = True
        finalStand()
    elif player.split is True:
        player.stand = True
    elif player.stand is True and player.splitStand is True:
        finalStand()
    else:
        finalStand()


def finalStand():
    if players[0].score < 17:
        deal_card(players[0])
        player_score(players[0])
        sleep(0.5)
        setup(players)
        pyg.display.update()
        finalStand()
    else:
        win_condition()


# TODO ##########################################################################################
def bet(player):
    global MESSAGE
    player.bet_value = 0
    player.bets_placed = False
    while not player.bets_placed:
        mouse = pyg.mouse.get_pos()
        MESSAGE = "Use buttons to place your bets."

        if GPIO:
            if GPIO.input(UP_ARROW) == GPIO.HIGH:
                sleep(0.250)
                if player.bet_value == 5:
                    player.bet_value = 0
                else:
                    player.bet_value += 1
                player.bet = bets[player.bet_value]
                print("Increase")
            elif GPIO.input(DOWN_ARROW) == GPIO.HIGH:
                sleep(0.250)
                if player.bet_value == 0:
                    player.bet_value = 5
                else:
                    player.bet_value -= 1
                player.bet = bets[player.bet_value]
                print("Decrease")
            elif GPIO.input(CONFIRM) == GPIO.HIGH:
                player.chips -= player.bet
                print("Bets placed")
                return True
            
        for event in pyg.event.get():
            if event.type == pyg.MOUSEBUTTONDOWN:
                increase_bet_check(mouse, player)
                decrease_bet_check(mouse, player)
                player.bets_placed = set_bet_check(mouse, player)
        
        setup(players)

        pyg.display.update()
        clock.tick(30)

    MESSAGE = ""


def check_user_input(input):
    try:
        # convert input to integer
        val = int(input)
        return "int"
    except ValueError:
        return "other"


def split(player):
    global counter
    if len(player.cards) < 2:
        pass
    elif player.cards[0].name[0] == player.cards[1].name[0] and len(player.cards) == 2 and \
            player.chips - player.bet >= 0:
        player.split = True
        counter = 1
        player.chips -= player.bet
        player.splitBet += player.bet 
        card1_x = (display_width * 0.25)
        card1_y = (display_height * 0.56)
        card2_x = (display_width * 0.60)
        card2_y = (display_height * 0.56)
        player.cards[0].x = card1_x
        player.cards[0].y = card1_y
        player.cards[1].x = card2_x
        player.cards[1].y = card2_y
        for card in player.cards:
            drawObjs(card)
        player.splitCards.append(player.cards[1])
        player.cards.remove(player.cards[1])
        player_score(player)
        split_score(player)
    else:
        print("cards do not match")

################################################
################# Main Game ####################
################################################


# initiate pygame
pyg.init()

# set display dimensions
display_width = 800
display_height = 480

# initiate display and caption
gameDisplay = pyg.display.set_mode((display_width, display_height))
pyg.display.set_caption('Blackjack')

# set color values
green = (34, 99, 43)
white = (255, 255, 255)
black = (0, 0, 0)

# set font for pygame
font = pyg.font.Font('freesansbold.ttf', 25)

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

# bet values list
bets = [25, 50, 100, 500, 750, 1000]

# keep track of number of players (total players adds dealer)
num_players = 1
total_players = num_players + 1
counter = 0

# initialize objects
objs = [
    obj.Button(display_width * 0.9, display_height * 0.83, 'deal'),
    obj.Button(display_width * 0.01, display_height * 0.83, 'hit'),
    obj.Button(display_width * 0.12, display_height * 0.83, 'stand'),
    obj.Button(display_width * 0.8, display_height * 0.83, 'split')
]

# initialize players as a list
players = [
        obj.Player("dealer", [], 0, 0, 0, 0),
        obj.Player("player1", [], 0, 0, 1000, 0)
]

initialization(players)
main(players)
# GPIO.cleanup()
pyg.quit()
quit()
