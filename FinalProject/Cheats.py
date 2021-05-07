import pygame as pyg
from time import sleep
import importlib

GPIO = False

if GPIO:
    import RPi.GPIO as GPIO
    UP_ARROW = 18
    DOWN_ARROW = 19
    CONFIRM = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(UP_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DOWN_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def display_text(text, x, y):
    cheatsScreen.blit(font.render(text, True, white), (x, y))

def getCheats():
    global BLACKJACK_CHEAT
    global DEALER_HINTS
    global PLACEHOLDER

    cheats = [BLACKJACK_CHEAT, DEALER_HINTS, PLACEHOLDER]

    return cheats

def setup():
    # fills background with green (can potentially be changed to image file later)
    cheatsScreen.fill(green)
    # iterates through lists and draws appropriate objects
    
    display_text('Cheats', 355, 75)
    display_text('INSANE BLACKJACK', 110, 175)
    display_text('DEALER HINTS', 140, 275)
    display_text('PLACEHOLDER', 137, 375)
    cheatsScreen.blit(font.render('Back', True, BACK_COLOR), (100, 75))
    cheatsScreen.blit(font.render('On', True, BLACKJACK_ON_COLOR), (500, 175))
    cheatsScreen.blit(font.render('Off', True, BLACKJACK_OFF_COLOR), (600, 175))
    cheatsScreen.blit(font.render('On', True, DEALER_HINTS_ON_COLOR), (500, 275))
    cheatsScreen.blit(font.render('Off', True, DEALER_HINTS_OFF_COLOR), (600, 275))
    cheatsScreen.blit(font.render('On', True, PLACEHOLDER_ON_COLOR), (500, 375))
    cheatsScreen.blit(font.render('Off', True, PLACEHOLDER_OFF_COLOR), (600, 375))
    pyg.draw.rect(cheatsScreen, INSANE_BLACKJACK_ON, (488, 161, 60, 50), 2)
    pyg.draw.rect(cheatsScreen, INSANE_BLACKJACK_OFF, (588, 161, 60, 50), 2)
    pyg.draw.rect(cheatsScreen, DEALER_HINTS_ON, (488, 261, 60, 50), 2)
    pyg.draw.rect(cheatsScreen, DEALER_HINTS_OFF, (588, 261, 60, 50), 2)
    pyg.draw.rect(cheatsScreen, PLACEHOLDER_ON, (488, 361, 60, 50), 2)
    pyg.draw.rect(cheatsScreen, PLACEHOLDER_OFF, (588, 361, 60, 50), 2)

def main():
    global file1
    global BLACKJACK_CHEAT
    global DEALER_HINTS 
    global PLACEHOLDER 
    global imported
    global INSANE_BLACKJACK_ON 
    global INSANE_BLACKJACK_OFF
    global DEALER_HINTS_ON 
    global DEALER_HINTS_OFF 
    global PLACEHOLDER_ON 
    global PLACEHOLDER_OFF
    global BLACKJACK_ON_COLOR 
    global BLACKJACK_OFF_COLOR
    global DEALER_HINTS_ON_COLOR 
    global DEALER_HINTS_OFF_COLOR 
    global PLACEHOLDER_ON_COLOR
    global PLACEHOLDER_OFF_COLOR
    global BACK_COLOR
    global selection
    global END
    while not END:
        if GPIO:
            if GPIO.input(CONFIRM) == GPIO.HIGH:
                sleep(0.250)
                if selection == 0:
                    if imported == True:
                        importlib.reload(StartScreen)
                    elif imported == False:
                        imported = True
                        import StartScreen
                elif selection == 1:
                    BLACKJACK_CHEAT = True
                    INSANE_BLACKJACK_ON = white
                    INSANE_BLACKJACK_OFF = green
                elif selection == 2:
                    BLACKJACK_CHEAT = False
                    INSANE_BLACKJACK_ON = green
                    INSANE_BLACKJACK_OFF = white
                elif selection == 3:
                    DEALER_HINTS = True
                    DEALER_HINTS_ON = white
                    DEALER_HINTS_OFF = green
                elif selection == 4:
                    DEALER_HINTS = False
                    DEALER_HINTS_ON = green
                    DEALER_HINTS_OFF = white
                elif selection == 5:
                    PLACEHOLDER = True
                    PLACEHOLDER_ON = white
                    PLACEHOLDER_OFF = green
                    
                elif selection == 6:
                    PLACEHOLDER = False
                    PLACEHOLDER_ON = green
                    PLACEHOLDER_OFF = white
                    
            if GPIO.input(UP_ARROW) == GPIO.HIGH:
                sleep(0.250)
                selection -= 1
                if selection == -1:
                    selection = 6
            elif GPIO.input(DOWN_ARROW) == GPIO.HIGH:
                sleep(0.250)
                selection += 1
                if selection == 7:
                    selection = 0
        if GPIO:
            if selection == 0:
                BACK_COLOR = blue
                BLACKJACK_ON_COLOR = white
                BLACKJACK_OFF_COLOR = white
                DEALER_HINTS_ON_COLOR = white
                DEALER_HINTS_OFF_COLOR = white
                PLACEHOLDER_ON_COLOR = white
                PLACEHOLDER_OFF_COLOR = white
            elif selection == 1:
                BACK_COLOR = white
                BLACKJACK_ON_COLOR = blue
                BLACKJACK_OFF_COLOR = white
                DEALER_HINTS_ON_COLOR = white
                DEALER_HINTS_OFF_COLOR = white
                PLACEHOLDER_ON_COLOR = white
                PLACEHOLDER_OFF_COLOR = white
            
            elif selection == 2:
                BACK_COLOR = white
                BLACKJACK_ON_COLOR = white
                BLACKJACK_OFF_COLOR = blue
                DEALER_HINTS_ON_COLOR = white
                DEALER_HINTS_OFF_COLOR = white
                PLACEHOLDER_ON_COLOR = white
                PLACEHOLDER_OFF_COLOR = white
            
            elif selection == 3:
                BACK_COLOR = white
                BLACKJACK_ON_COLOR = white
                BLACKJACK_OFF_COLOR = white
                DEALER_HINTS_ON_COLOR = blue
                DEALER_HINTS_OFF_COLOR = white
                PLACEHOLDER_ON_COLOR = white
                PLACEHOLDER_OFF_COLOR = white

            elif selection == 4:
                BACK_COLOR = white
                BLACKJACK_ON_COLOR = white
                BLACKJACK_OFF_COLOR = white
                DEALER_HINTS_ON_COLOR = white
                DEALER_HINTS_OFF_COLOR = blue
                PLACEHOLDER_ON_COLOR = white
                PLACEHOLDER_OFF_COLOR = white

            elif selection == 5:
                BACK_COLOR = white
                BLACKJACK_ON_COLOR = white
                BLACKJACK_OFF_COLOR = white
                DEALER_HINTS_ON_COLOR = white
                DEALER_HINTS_OFF_COLOR = white
                PLACEHOLDER_ON_COLOR = blue
                PLACEHOLDER_OFF_COLOR = white

            elif selection == 6:
                BACK_COLOR = white
                BLACKJACK_ON_COLOR = white
                BLACKJACK_OFF_COLOR = white
                DEALER_HINTS_ON_COLOR = white
                DEALER_HINTS_OFF_COLOR = white
                PLACEHOLDER_ON_COLOR = white
                PLACEHOLDER_OFF_COLOR = blue
                
        pyg.display.update()

        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                END = True

            # detect if mouse button is pressed on buttons (and call appropriate functions)
            if event.type == pyg.MOUSEBUTTONDOWN:
                if (500) <= mouse[0] <= (500 + 25) and (175) <= mouse[1] <= (175 + 25):
                    BLACKJACK_CHEAT = True
                    INSANE_BLACKJACK_ON = white
                    INSANE_BLACKJACK_OFF = green

                if (600) <= mouse[0] <= (600 + 25) and (175) <= mouse[1] <= (175 + 25):
                    BLACKJACK_CHEAT = False
                    INSANE_BLACKJACK_ON = green
                    INSANE_BLACKJACK_OFF = white

                if (500) <= mouse[0] <= (500 + 25) and (275) <= mouse[1] <= (275 + 25):
                    DEALER_HINTS = True
                    DEALER_HINTS_ON = white
                    DEALER_HINTS_OFF = green

                if (600) <= mouse[0] <= (600 + 25) and (275) <= mouse[1] <= (275 + 25):
                    DEALER_HINTS = False
                    DEALER_HINTS_ON = green
                    DEALER_HINTS_OFF = white

                if (500) <= mouse[0] <= (500 + 25) and (375) <= mouse[1] <= (375 + 25):
                    PLACEHOLDER = True
                    PLACEHOLDER_ON = white
                    PLACEHOLDER_OFF = green

                if (600) <= mouse[0] <= (600 + 25) and (375) <= mouse[1] <= (375 + 25):
                    PLACEHOLDER = False
                    PLACEHOLDER_ON = green
                    PLACEHOLDER_OFF = white

                if (100) <= mouse[0] <= (100 + 50) and (75) <= mouse[1] <= (75 + 25):
                    L = ["BLACKJACK_CHEAT = \n", "{} \n".format(BLACKJACK_CHEAT), "DEALER_HINTS = \n", "{} \n".format(DEALER_HINTS)]
                    file1.writelines(L)
                    file1.close()
                    if imported == True:
                        importlib.reload(StartScreen)
                    elif imported == False:
                        imported = True
                        import StartScreen

        # call our setup function
        setup()

        # update display
        pyg.display.update()
        clock.tick(60)

pyg.init()

WIDTH = 800
HEIGHT = 450

cheatsScreen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Py-Jack")

# set color values
green = (34, 99, 43)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# RECTANGLES
INSANE_BLACKJACK_ON = green
INSANE_BLACKJACK_OFF = white
DEALER_HINTS_ON = green
DEALER_HINTS_OFF = white
PLACEHOLDER_ON = green
PLACEHOLDER_OFF = white

# TEXT COLORS
BLACKJACK_ON_COLOR = white
BLACKJACK_OFF_COLOR = white
DEALER_HINTS_ON_COLOR = white
DEALER_HINTS_OFF_COLOR = white
PLACEHOLDER_ON_COLOR = white
PLACEHOLDER_OFF_COLOR = white
BACK_COLOR = white

# CHEATS
BLACKJACK_CHEAT = False
DEALER_HINTS = False
PLACEHOLDER = False

# set font for pygame
font = pyg.font.Font('freesansbold.ttf', 25)

# initiates clock and end parameter
clock = pyg.time.Clock()
END = False
selection = 0
imported = False

file1 = open("Cheats.txt", "w")

main()
pyg.quit()
quit()
