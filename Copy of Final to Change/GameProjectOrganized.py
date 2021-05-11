# main game plays here

# import pygame and image files
import pygame as pyg
from random import choice
import ObjClasses as obj
import imgs
from time import sleep


class Game():
    def __init__(self, id):
        self.id = id
        self.ready = False

    
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
    def deal_card(self):
        # generates random card number
        rand_index = Game.random_card()
        # check if player is busted, if so don't deal them
        if self.bust is True:
            pass
        # checks if this is first card and who is receiving it (first cards have a specific x,y pair to use)
        elif len(self.cards) == 0 and self.name != "dealer":
            self.cards.append(obj.Card(card1_x, card1_y, imgs.card_names[rand_index],
                                       Game.card_value(self, imgs.card_names[rand_index]), rand_index))
        elif len(self.cards) == 0 and self.name == "dealer":
            self.cards.append(obj.Card(card2_x, card2_y, imgs.card_names[rand_index],
                                       Game.card_value(self, imgs.card_names[rand_index]), rand_index))
        elif len(self.cards) == 1 and self.name == "dealer":
            self.cards.append(obj.Card((self.cards[len(self.cards) - 1].x + 40),
                                       (self.cards[len(self.cards) - 1].y), "purple_back", 0, 52))
        elif len(self.cards) == 2 and self.name == "dealer" and self.cards[1].name == "purple_back":
            self.cards.remove(self.cards[1])
            self.cards.append(obj.Card((self.cards[len(self.cards) - 1].x + 40),
                                       (self.cards[len(self.cards) - 1].y), imgs.card_names[rand_index],
                                       Game.card_value(self, imgs.card_names[rand_index]), rand_index))
        # if not first card, just add it on top of last placed card
        else:
            self.cards.append(obj.Card((self.cards[len(self.cards) - 1].x + 40),
                                       (self.cards[len(self.cards) - 1].y), imgs.card_names[rand_index],
                                       Game.card_value(self, imgs.card_names[rand_index]), rand_index))
        # print statement to debug dealing (not seen by player)
        #print("Card dealt to {}! (if not busted)".format(self.name))


    def split_deal(self):
        rand_index = Game.random_card()
        # check if player is busted, if so don't deal them
        if self.splitBust is True:
            pass
        else:
            self.splitCards.append(obj.Card((self.splitCards[len(self.splitCards) - 1].x + 40),
                                            (self.splitCards[len(self.splitCards) - 1].y - 20),
                                            imgs.card_names[rand_index], card_value(imgs.card_names[rand_index],
                                                                                    self), rand_index))
        # print statement to debug dealing (not seen by player)
        #print("Card dealt to {} Split Hand! (if not busted)".format(self.name))


    # use card name to determine value (removes last character and returns number, prints 10 if face card or 1 if Ace)
    def card_value(self, name):
        simplified = name[:-1]
        if simplified in ["K", "Q", "J"]:
            return 10
        elif simplified == "A":
            if self.split is not True:
                if self.score > 10:
                    return 1
                else:
                    self.aces += 1
                    return 11
            else:
                if self.splitScore > 10:
                    return 1
                else:
                    self.splitAces += 1
                    return 11
        else:
            return int(simplified)


    # determine total point value of cards for player
    def player_score(self):
        global counter
        if self.bust is False:
            if counter == 0:
                n = len(self.cards)
                self.score += self.cards[n - 1].val
            if counter == 1:
                self.score = self.cards[0].val
                counter = 0
            if self.score > 21 and self.aces > 0:
                self.score -= 10
                self.aces -= 1
        Game.bust_check(self)


    def split_score(self):
        if self.splitBust is False:
            n = len(self.splitCards)
            if self.splitCards[0].name[:-1] == "A":
                self.splitCards[0].val = 11
                self.splitAces += 1
            self.splitScore += self.splitCards[n - 1].val
            if self.splitScore > 21 and self.splitAces > 0:
                self.splitScore -= 10
                self.splitAces -= 1
        Game.split_bust_check(self)


    

    # define reset function
    def reset(self):
        p = self
        global used_cards
        used_cards = []
        p.cards = []
        p.aces = 0
        p.score = 0
        p.bet = 0
        p.stand = False
        p.bust = False
        p.splitCards = []
        p.splitAces = 0
        p.splitScore = 0
        p.splitBet = 0
        p.splitStand = False
        p.splitBust = False
        p.split = False
        p.win = False


    # initialize players and deal first cards
    # TODO: later add way to generate a new player for every player in num_players
    def initialization(self):
        if self.name == "dealer":
            for i in range(2):
                Game.deal_card(self)
                Game.player_score(self)
        else:
            #global n
            #Game.setup(self)
            sleep(0.1)
            #Game.bet(self)
            for i in range(2):
                Game.deal_card(self)
                Game.player_score(self)
                sleep(0.1)
                #setup(self)
                #pyg.display.update()
                
        ##        Game.deal_card(dealer)
        ##        Game.player_score(dealer)
        ##        sleep(0.1)
        ##        #setup(self)
        ##        pyg.display.update()
            #pyg.display.update()

    def bust_check(self):
        if self.score > 21:
            self.bust = True


    def split_bust_check(self):
        if self.splitScore > 21:
            self.splitBust = True


    def win_condition(dealer, p):
        if p.score == 21:
            print("You hit Blackjack! You have recieved {} chips.".format(p.bet*1.5))
            p.chips += p.bet*1.5
            print(p.chips)
        if p.split is True:
            if p.splitScore == 21:
                print("You hit Blackjack! You have recieved {} chips.".format(p.bet*1.5))
                p.chips += int(p.bet*1.5)
                print(p.chips)
        elif dealer.bust is True:
            if p.bust is True:
                if p.chips == 0:
                    p.chips = 100
                print("Better Luck Next Time")
            elif p.bust is not True:
                print("Congratulations {}, you've won {} chips!".format(p.name, p.bet*2))
                p.chips += p.bet*2
                print(p.chips)
            if p.split is True:
                if p.splitBust is True:
                    print("Better Luck Next Time")
                elif p.splitBust is not True:
                    print("Congratulations {}, you've won {} chips!".format(p.name, p.bet*2))
                    p.chips += p.bet*2
                    print(p.chips)      
        elif p.bust is True:
            if p.chips == 0:
                p.chips = 100
            print("Better Luck Next Time")
            if p.split is True:
                if p.splitBust is True:
                    print("Better Luck Next Time")
                elif p.splitBust is not True:
                    if p.splitBet == dealer.score:
                        print("Push! You have recieved {} chips.".format(p.bet))
                        p.chips += p.bet
                        print(p.chips)
                    elif p.splitBet > dealer.score:
                        print("Congratulations {}, you've won {} chips!".format(p.name, p.bet*2))
                        p.chips += p.bet*2
                        print(p.chips)
                    elif p.splitBet < dealer.score:
                         print("Better Luck Next Time")
        elif p.splitBust is True:
            if p.score == dealer.score:
                print("Push! You have recieved {} chips.".format(p.bet))
                p.chips += p.bet
                print(p.chips)
            elif p.score > dealer.score:
                print("Congratulations {}, you've won {} chips!".format(p.name, p.bet*2))
                p.chips += p.bet*2
                print(p.chips)
            elif p.score < dealer.score:
                if p.chips == 0:
                    p.chips = 100
                print("Better Luck Next Time") 
            print("Better Luck Next Time")
        else:
            if p.score == dealer.score:
                print("Push! You have recieved {} chips.".format(p.bet))
                p.chips += p.bet
                print(p.chips)
            elif p.score > dealer.score:
                print("Congratulations {}, you've won {} chips!".format(p.name, p.bet*2))
                p.chips += p.bet*2
                print(p.chips)
            elif p.score < dealer.score:
                if p.chips == 0:
                    p.chips = 100
                print("Better Luck Next Time")
            if p.split is True:
                if p.splitScore == dealer.score:
                    print("Push, you have recieved {} chips.".format(p.bet))
                    p.chips += p.bet
                    print(p.chips)
                elif p.splitScore > dealer.score:
                    print("Congratulations {}, you've won {} chips!".format(p.name, p.bet*2))
                    p.chips += p.bet*2
                    print(p.chips)
                elif p.splitScore < dealer.score:
                    if p.chips == 0:
                        p.chips = 100
                    print("Better Luck Next Time")


    def win(self):
        if self.name == "dealer":
            print("Better Luck Next Time")
        elif self.score == dealer.score:
            if self.score == 21:
                print("You hit Blackjack! You have recieved {} chips.".format(self.bet*1.5))
                self.chips += self.bet*1.5
                print(self.chips)
            else:
                print("Push, you have recieved {} chips.".format(self.bet))
                self.chips += self.bet
                print(self.chips)
        else:
            if self.score == 21:
                print("You hit Blackjack! You have recieved {} chips.".format(self.bet*1.5))
                self.chips += self.bet*1.5
                print(self.chips)
            else: 
                print("Congratulations {}, you've won {} chips!".format(self.name, self.bet*2))
                self.chips += self.bet*2
                print(self.chips)


    def hit(self):
        if self.stand == True and self.split == True:
            Game.split_deal(self)
            Game.split_score(self)
            #setup(selfs)
            pyg.display.update()
            sleep(0.5)
            
        else:   
            Game.deal_card(self)
            Game.player_score(self)
            #setup(self)
            pyg.display.update()
            sleep(0.5)


            
    def allStand(players):
        for i in range(len(players) - 1):
            if players[i + 1].stand is False or players[i + 1] is False:
                return False
        return True


    
    def stand(self):
        if self.split is True:
            self.splitStand = True
        else:
            self.stand = True


    def finalStand(dealer, player):
        if dealer.score < 17:
            Game.deal_card(dealer)
            Game.player_score(dealer)
            Game.finalStand(dealer, player)
        else:
            Game.win_condition(dealer, player)



    def split(self):
        global counter
        if len(self.cards) < 2:
            pass
        elif self.cards[0].name[0] == self.cards[1].name[0] and len(self.cards) == 2 and \
                self.chips - self.bet >= 0:
            self.split = True
            counter = 1
            self.chips -= self.bet
            self.splitBet += self.bet 
            card1_x = (display_width * 0.25)
            card1_y = (display_height * 0.56)
            card2_x = (display_width * 0.60)
            card2_y = (display_height * 0.56)
            self.cards[0].x = card1_x
            self.cards[0].y = card1_y
            self.cards[1].x = card2_x
            self.cards[1].y = card2_y
            for card in self.cards:
                Game.drawObjs(card)
            self.splitCards.append(self.cards[1])
            self.cards.remove(self.cards[1])
            Game.player_score(self)
            Game.split_score(self)
        else:
            print("cards do not match")


# initiate pygame
pyg.init()

# set display dimensions
display_width = 800
display_height = 450

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
card1_x = (display_width * 0.38)
card1_y = (display_height * 0.61)

# set x and y for first card dealt to dealer
card2_x = (display_width * 0.38)
card2_y = (display_height * 0.15)

# create list for used cards and counters for cards dealt to player/dealer
used_cards = []

# keep track of number of players (total players adds dealer)
num_players = 1
total_players = num_players + 1
counter = 0

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
