import pygame as pyg
from network import Network
import pickle
import ObjClasses as obj
#from GameProjectOrganized import Game
import imgs
from time import time


def Display(info):
    text = font.render(info, 1, (255,0,0))
    gameDisplay.blit(text, (100,200))
    pyg.display.update()

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
        # While dealers score is less than 18, dealer will keep hitting
        return 1
    return 0


def split_button_check(mouse):
    if (display_width * 0.8) <= mouse[0] <= ((display_width * 0.8) + 77) and (display_height * 0.86) <= mouse[1] <= ((display_height * 0.86) + 77):
        return 1
    return 0



# define function to draw objects
def drawObjs(object):
    if object.__class__ == obj.Card:
        gameDisplay.blit(imgs.cards[object.ind], (object.x, object.y))
    else:
        gameDisplay.blit(getattr(imgs, object.name), (object.x, object.y))


# defines setup function to be run at start of loop
def setup(self, dealer):
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
        
    if self.split is False:
        gameDisplay.blit(font.render('Player Total: {}'.format(self.score), True, white), (20, 60))
    if self.split is True:
        gameDisplay.blit(font.render('Hand 2 Total: {}'.format(self.splitScore), True, white), (20, 100))
        gameDisplay.blit(font.render('Hand 1 Total: {}'.format(self.score), True, white), (20, 60))
    gameDisplay.blit(font.render('Dealer Total: {}'.format(dealer.score), True, white), (20, 20))
    gameDisplay.blit(font.render('Chips: {}'.format(self.chips), True, white), (600, 20))
    gameDisplay.blit(font.render('Bet: {}'.format(self.bet), True, white), (600, 60))



# initialize players and deal first cards
# TODO: later add way to generate a new player for every player in num_players
##def initialization(self, p):
##    global n
##    Game.bet(self)
##    for i in range(2):
##        Game.deal_card(self)
##        Game.player_score(self)
##        #sleep(0.1)
##        #setup(self)
##        pyg.display.update()
##        
####        Game.deal_card(dealer)
####        Game.player_score(dealer)
####        sleep(0.1)
####        #setup(self)
####        pyg.display.update()
##    n.send(obj.players[p])
##    pyg.display.update()

def bet(self):
    amount = input("How much would you like to bet. (Must be Less than or Equal to {}): ".format(self.chips))
    dataType = check_user_input(amount)
    #print("Amount: " + str(amount) + " Chips: " + str(self.chips))
    if dataType == "int":
        amount = int(amount)
        if amount < 0:
            print("Invalid bet. Bet must be a positive whole number")
            bet(self)
        elif amount < self.chips:
            #print("Less than chips")
            self.chips -= amount
            self.bet = amount
        elif amount == self.chips:
            #print("Equal to chips")
            self.chips = 0
            self.bet = amount
        elif amount > self.chips:
            print("Invalid bet. Must be Less than or Equal to {}".format(self.chips))
            bet(self)
    else:
        print("Invalid bet. Bet must be a positive whole number")
        bet(self)


def check_user_input(input):
    try:
        # convert input to integer
        val = int(input)
        return "int"
    except ValueError:
        return "other"


def update(p):
    global n
    reply = pickle.loads(n.send("players"))

    for i in range(len(reply)):
        obj.players[i] = reply[i]

    reply = pickle.loads(n.send("cards"))
    obj.players[p].cards = reply
    

def waiting(info):
    global n
    run = True
    while run:
        try:  
            reply = pickle.loads(n.send(info))
            if reply == "done":
                run = False
        except:
            break
    
    
    
    

def main():
    # initiates clock and end parameter
    clock = pyg.time.Clock()
    global n
    try:
        reply = pickle.loads(n.send("initial"))
    except:
        print("Oops, it looks like an error has occured.")
        menu_screen()
    for i in range(len(reply)):
        obj.players.append(reply[i])
    p = int(n.getP())
    try:
        update(p)
    except:
        print("Oops, it looks like an error has occured.")
        menu_screen()
    #print("Score out of update: " + str(obj.players[p].score))
    setup(obj.players[p], obj.players[0])
    # update display
    pyg.display.update()

    game_run = True
    while game_run:
        bet(obj.players[p])
        n.send(str(obj.players[p].chips))
        #initialization(player, p)
        try:
            update(p)
        except:
            print("Oops, it looks like an error has occured.")
            menu_screen()
        setup(obj.players[p], obj.players[0])
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
                        n.send("reset")
                        try:
                            update(p)
                        except:
                            print("Oops, it looks like an error has occured.")
                            menu_screen()
                        setup(obj.players[p], obj.players[0])
                        pyg.display.update()
                        run = False
                    # hit button, generates new card and adds to card objects list
                    elif hit_button_check(mouse) == 1 and obj.players[p].stand is False:
                        n.send("hit")
                        try:
                            update(p)
                        except:
                            print("Oops, it looks like an error has occured.")
                            menu_screen()
                        setup(obj.players[p], obj.players[0])
                        pyg.display.update()
                        if obj.players[p].bust is True:
                            waiting("bust")
                    # stand button
                    elif stand_button_check(mouse) == 1 and obj.players[p].stand is False:
                        waiting("stand")
                    # split button
                    elif split_button_check(mouse) == 1 and obj.players[p].stand is False:
                        n.send("split")
                        try:
                            update(p)
                        except:
                            print("Oops, it looks like an error has occured.")
                            menu_screen()

            # call our setup function
            #n.send("player")
            try:
                update(p)
            except:
                print("Oops, it looks like an error has occured.")
                menu_screen()
            #print("Score out of update: " + str(obj.players[p].score))
            setup(obj.players[p], obj.players[0])

            # update display
            pyg.display.update()
##            end_time = time()
##            total = end_time - start_time
##            print(total)
            

def menu_screen():
    run = True
    clock = pyg.time.Clock()
    global n
    p = int(n.getP())
    if p == 1:
        while run:
            clock.tick(60)
            gameDisplay.fill((128, 128, 128))
            Display("Click to Play!")

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pyg.MOUSEBUTTONDOWN:
                    run = False
        try:
            n.send("start")
        except:
            print("Oops, it looks like an error has occured.")
            menu_screen()
        main()
    else:
        while run:
            clock.tick(60)
            gameDisplay.fill((128, 128, 128))
            Display("Waiting for Host to start!")
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
display_height = 480

# initiate display and caption
gameDisplay = pyg.display.set_mode((display_width, display_height))
pyg.display.set_caption('Blackjack')

# set color values
green = (34, 99, 43)
white = (255, 255, 255)

# set font for pygame
font = pyg.font.Font('freesansbold.ttf', 25)

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


# initialize objects
objs = [
    obj.Button(display_width * 0.9, display_height * 0.87, 'deal'),
    obj.Button(display_width * 0.01, display_height * 0.86, 'hit'),
    obj.Button(display_width * 0.12, display_height * 0.86, 'stand'),
    obj.Button(display_width * 0.8, display_height * 0.86, 'split')
]

while True:
    menu_screen()


### initialize players as a list
#players = []
##        obj.Player("dealer", [], 0, 0, 0, 0),
##        obj.Player("player1", [], 0, 0, 1000, 0)
##    ]

##GPIO.cleanup()
##pyg.quit()
##quit()
