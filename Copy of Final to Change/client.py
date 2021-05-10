import pygame as pyg
from network import Network
import pickle
import ObjClasses as obj
import imgs
from time import sleep


GPIO = False
if GPIO:
    import RPi.GPIO as GPIO
    # Setup GPIO Blackjack Buttons
    RESET = 6
    HIT = 17
    STAND = 16
    UP_ARROW = 19
    DOWN_ARROW = 18
    CONFIRM = 4
    # Setup the GPIO pins 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RESET, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HIT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(STAND, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(UP_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DOWN_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def display_text(text, x, y):
    gameDisplay.blit(font.render(text, True, white), (x, y))


# STUFF FOR PRINTING TEXT TO SCREEN
def print_text(text):
    message = font.render(text, True, black)
    message_rect = message.get_rect(center=(display_width/2, display_height/2))
    gameDisplay.blit(message, message_rect)


MESSAGE = ""


# define function to draw objects
def drawObjs(object):
    if object.__class__ == obj.Card:
        gameDisplay.blit(imgs.cards[object.ind], (object.x, object.y))
    else:
        gameDisplay.blit(getattr(imgs, object.name), (object.x, object.y))


# defines setup function to be run at start of loop
def setup(self, dealer, p, players):
    #print(self.name)
    # fills background with green (can potentially be changed to image file later)
    gameDisplay.fill(green)
    # iterates through lists and draws appropriate objects
    for obj in objs:
        drawObjs(obj)
    for card in self.cards:
        drawObjs(card)
    for card in self.splitCards:
        drawObjs(card)
        
    for card in dealer.cards:
        drawObjs(card)
    for card in dealer.splitCards:
        drawObjs(card)
        
    if self.split is True:
        gameDisplay.blit(font.render('Hand 2 Total: {}'.format(self.splitScore), True, white), (20, 100))
        gameDisplay.blit(font.render('Hand 1 Total: {}'.format(self.score), True, white), (20, 60))
    gameDisplay.blit(font.render('Dealer Total: {}'.format(dealer.score), True, white), (20, 20))
    gameDisplay.blit(font.render('Chips: {}'.format(self.chips), True, white), (600, 20))
    gameDisplay.blit(font.render('Bet: {}'.format(self.bet), True, white), (600, 60))
    count = 1
    for i in range(len(players) - 1):
        j = i + 1
        if j == p:
            if self.split is False:
                gameDisplay.blit(font.render('Your Total: {}'.format(self.score), True, white), (20, 60))
        else:
            if p == 1:
                gameDisplay.blit(font.render('Host Total: {}'.format(players[j].score), True, white), (20, 60 + (count * 30)))
                count += 1
            else:
                gameDisplay.blit(font.render('Player{} Total: {}'.format(j, players[j].score), True, white), (20, 60 + (count * 30)))
                count += 1
    print_text(MESSAGE)


# button check functions:
def deal_button_check(mouse):
    if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 70) and (display_height * 0.87) <= mouse[1] <= ((display_height * 0.87) + 70):
        return 1
    return 0


def hit_button_check(mouse):
    if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        return 1
    return 0


def stand_button_check(mouse):
    if (display_width * 0.12) <= mouse[0] <= ((display_width * 0.12) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        return 1
    return 0


def split_button_check(mouse):
    if (display_width * 0.8) <= mouse[0] <= ((display_width * 0.8) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        return 1
    return 0


def increase_bet_check(mouse, p):
    if (display_width * 0.8) <= mouse[0] <= ((display_width * 0.8) + 77) and (display_height * 0.64) <= mouse[1] <= \
            ((display_height * 0.64) + 77):
        bets = [25, 50, 100, 500, 750, 1000, p.chips]
        if p.bet_value == 6:
            p.bet_value = 0
        else:
            p.bet_value += 1

        if p.chips < bets[p.bet_value]:
            p.bet = p.chips
        else:
            p.bet = bets[p.bet_value]
        print("Increase")


def decrease_bet_check(mouse, p):
    if (display_width * 0.9) <= mouse[0] <= ((display_width * 0.9) + 77) and (display_height * 0.64) <= mouse[1] <= \
            ((display_height * 0.64) + 77):
        bets = [25, 50, 100, 500, 750, 1000, p.chips]
        if p.bet_value == 0:
            p.bet_value = 6
        else:
            p.bet_value -= 1

        if p.chips < bets[p.bet_value]:
            p.bet = p.chips
        else:
            p.bet = bets[p.bet_value]
        print("Decrease")


def set_bet_check(mouse, player):
    if (display_width * 0.01) <= mouse[0] <= ((display_width * 0.01) + 77) and (display_height * 0.64) <= mouse[1] <= \
            ((display_height * 0.64) + 77):
        player.chips -= player.bet
        print("Bets placed")
        return True


def bet(player, p):
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
        
        setup(player, obj.players[0], p, obj.players)

        pyg.display.update()
        clock.tick(30)

    MESSAGE = ""




def update(p):
    global n
    reply = pickle.loads(n.send("players"))

    for i in range(len(reply)):
        obj.players[i] = reply[i]

    reply = pickle.loads(n.send("cards"))
    obj.players[p].cards = reply
    

def waiting(info):
    global n
    global MESSAGE
    run = True
    while run:
        try:  
            reply = pickle.loads(n.send(info))
            if reply == "done":
                MESSAGE = ""
                run = False
        except:
            break
    
    
    
    

def main():
    # initiates clock and end parameter
    clock = pyg.time.Clock()
    global n
    global MESSAGE
    
    try:
        reply = pickle.loads(n.send("initial"))
    except:
        MESSAGE = "Oops, it looks like an error has occured."
        setup(obj.players[p], obj.players[0], p, obj.players)
        menu_screen()
    for i in range(len(reply)):
        obj.players.append(reply[i])
    p = int(n.getP())
    try:
        update(p)
    except:
        MESSAGE = "Oops, it looks like an error has occured."
        setup(obj.players[p], obj.players[0], p, obj.players)
        menu_screen()
    #print("Score out of update: " + str(obj.players[p].score))
    setup(obj.players[p], obj.players[0], p, obj.players)
    # update display
    pyg.display.update()

    game_run = True
    while game_run:
        bet(obj.players[p], p)
        n.send(str(obj.players[p].chips))
        #initialization(player, p)
        try:
            update(p)
        except:
            MESSAGE = "Oops, it looks like an error has occured."
            setup(obj.players[p], obj.players[0], p, obj.players)
            sleep(5)
            menu_screen()
        setup(obj.players[p], obj.players[0], p, obj.players)
        pyg.display.update()
        run = True
        while run:
            clock.tick(20)
##            start_time = time()
            try:
                game = n.send("get")
            except:
                print("Couldn't get game")
                menu_screen()
            

    ##        if game.allStand():
    ##            pass
           # if GPIO.input(18) == GPIO.HIGH:
           #     reset()
           # if GPIO.input(19) == GPIO.HIGH:
           #     hit()
           #     sleep(0.5)
           # elif GPIO.input(20) == GPIO.HIGH:
           #     stand()
           

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    run = True

                # detect if mouse button is pressed on buttons (and call appropriate functions)
                if event.type == pyg.MOUSEBUTTONDOWN:
                    # get mouse x and y coordinates
                    mouse = pyg.mouse.get_pos()
                    # deal button
                    if deal_button_check(mouse) == 1:
                        if p == 1:
                            n.send("reset")
                            try:
                                update(p)
                            except:
                                MESSAGE = "Oops, it looks like an error has occured."
                                setup(obj.players[p], obj.players[0], p)
                                sleep(5)
                                menu_screen()
                            setup(obj.players[p], obj.players[0], p, obj.players)
                            pyg.display.update()
                            run = False
                        else:
                            MESSAGE = "Only the Host can begin a new round."
                            print_text(MESSAGE)
                    # hit button, generates new card and adds to card objects list
                    elif hit_button_check(mouse) == 1 and obj.players[p].stand is False:
                        n.send("hit")
                        try:
                            update(p)
                        except:
                            MESSAGE = "Oops, it looks like an error has occured."
                            setup(obj.players[p], obj.players[0], p, obj.players)
                            menu_screen()
                        setup(obj.players[p], obj.players[0], p, obj.players)
                        pyg.display.update()
                        if obj.players[p].bust is True:
                            MESSAGE = "You Busted! Waiting for other players..."
                            setup(obj.players[p], obj.players[0], p, obj.players)
                            waiting("bust")
                    # stand button
                    elif stand_button_check(mouse) == 1 and obj.players[p].stand is False:
                        MESSAGE = "Waiting for other players to finish..."
                        setup(obj.players[p], obj.players[0], p, obj.players)
                        waiting("stand")
                    # split button
                    elif split_button_check(mouse) == 1 and obj.players[p].stand is False:
                        n.send("split")
                        try:
                            update(p)
                        except:
                            MESSAGE = "Oops, it looks like an error has occured."
                            setup(obj.players[p], obj.players[0], p, obj.players)
                            sleep(5)
                            menu_screen()

            # call our setup function
            #n.send("player")
            try:
                update(p)
            except:
                MESSAGE = "Oops, it looks like an error has occured."
                setup(obj.players[p], obj.players[0], p, obj.players)
                sleep(5)
                menu_screen()
            #print("Score out of update: " + str(obj.players[p].score))
            setup(obj.players[p], obj.players[0], p, obj.players)

            # update display
            pyg.display.update()
##            end_time = time()
##            total = end_time - start_time
##            print(total)
            




def menu_screen():
    run = True
    clock = pyg.time.Clock()
    global n
    try:
        n.send("add")
    except:
        MESSAGE = "Oops, it looks like an error has occured."
        print_text(MESSAGE)
        # update display
        pyg.display.update()
        sleep(5)
        menu_screen()
    p = int(n.getP())
    if p == 1:
        while run:
            # fills background with green (can potentially be changed to image file later)
            gameDisplay.fill(green)
            clock.tick(60)
            reply = pickle.loads(n.send("players"))
            count = 0
            print(len(reply))
            for i in range(len(reply) - 1):
                j = i + 1
                if j == p:
                    print("j = p")
                else:
                    print("print Plyaer")
                    gameDisplay.blit(font.render('Player{} has connected'.format(j), True, white), (20, 60 - (count * 10)))
                    count += 1

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pyg.MOUSEBUTTONDOWN:
                    run = False
            MESSAGE = "Click to Play!"
            print_text(MESSAGE)
            # update display
            pyg.display.update()
        try:
            n.send("start")
        except:
            MESSAGE = "Oops, it looks like an error has occured."
            print_text(MESSAGE)
            # update display
            pyg.display.update()
            sleep(5)
            menu_screen()
        main()
    else:
        while run:
            # fills background with green (can potentially be changed to image file later)
            gameDisplay.fill(green)
            clock.tick(60)
            MESSAGE = "Waiting for Host to start..."
            print_text(MESSAGE)
            # update display
            pyg.display.update()
            try:
                reply = pickle.loads(n.send("isStart"))
                if reply is True:
                    run = False
            except:
                menu_screen()

        main()



        


n = Network()

# initiate pygame
pyg.init()

# set display dimensions
display_width = 800
display_height = 450

# initiate display and caption
gameDisplay = pyg.display.set_mode((display_width, display_height))
pyg.display.set_caption("Py-Jack")

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
card1_x = (display_width * 0.38)
card1_y = (display_height * 0.61)

# set x and y for first card dealt to dealer
card2_x = (display_width * 0.38)
card2_y = (display_height * 0.15)

# create list for used cards and counters for cards dealt to player/dealer
used_cards = []

# initialize objects
objs = [
    obj.Button(display_width * 0.9, display_height * 0.82, 'deal'),
    obj.Button(display_width * 0.01, display_height * 0.82, 'hit'),
    obj.Button(display_width * 0.12, display_height * 0.82, 'stand'),
    obj.Button(display_width * 0.8, display_height * 0.82, 'split'),
    obj.Button(display_width * 0.8, display_height * 0.64, 'raise_bet'),
    obj.Button(display_width * 0.9, display_height * 0.64, 'lower_bet'),
    obj.Button(display_width * 0.01, display_height * 0.64, 'set_bet')
]


menu_screen()
if GPIO:
    GPIO.cleanup()
pyg.quit()
quit()
