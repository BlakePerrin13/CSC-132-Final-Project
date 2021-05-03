import pygame as pyg
from time import sleep

GPIO = True

if GPIO:
    import RPi.GPIO as GPIO
    UP_ARROW = 18
    DOWN_ARROW = 19
    CONFIRM = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(UP_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(DOWN_ARROW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CONFIRM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    


def single_player():
    import GameProjectSinglePlayer
    
def multiplayer():
    import GameProjectOrganized

def cheats():
    pass

def settings():
    pass

def display_text(text, x, y):
    startScreen.blit(font.render(text, True, white), (x, y))

def setup():
    # fills background with green (can potentially be changed to image file later)
    startScreen.fill(green)
    # iterates through lists and draws appropriate objects
    
    display_text('Welcome to Py-Jack', 280, 75)
    display_text('SinglePlayer', 325, 175)
    display_text('Multiplayer', 335, 275)
    display_text('Cheats', 360, 375)
    pyg.draw.rect(startScreen, (255,255,255), (342, 363, 125, 50), 2)
    pyg.draw.rect(startScreen, (255,255,255), (320, 263, 167, 50), 2)
    pyg.draw.rect(startScreen, (255,255,255), (310, 162, 185, 50), 2)
    

def main():

    global mode
    global END
    while not END:
        if GPIO:
            if GPIO.input(CONFIRM) == GPIO.HIGH:
                if mode == 1:
                    import GameProjectSinglePlayer
                elif mode == 2:
                    import GameProjectOrganized
                elif mode == 3:
                    pass
                    
            if GPIO.input(UP_ARROW) == GPIO.HIGH:
                sleep(0.250)
                mode -= 1
                if mode == 0:
                    mode = 3
            elif GPIO.input(DOWN_ARROW) == GPIO.HIGH:
                sleep(0.250)
                mode += 1
                if mode == 4:
                    mode = 1

        if mode == 3:
            pyg.draw.rect(startScreen, (0, 0, 255), (342, 363, 125, 50), 2)   # singleplayer tab
            pyg.draw.rect(startScreen, (255,255,255), (320, 263, 167, 50), 2) # multiplayer tab
            pyg.draw.rect(startScreen, (255,255,255), (310, 162, 185, 50), 2) # cheats tab

        elif mode == 2:
            pyg.draw.rect(startScreen, (0, 0, 255), (320, 263, 167, 50), 2)   # multiplayer tab
            pyg.draw.rect(startScreen, (255,255,255), (342, 363, 125, 50), 2) # singleplayer tab
            pyg.draw.rect(startScreen, (255,255,255), (310, 162, 185, 50), 2) # cheats tab
            
        elif mode == 1:
            pyg.draw.rect(startScreen, (0, 0, 255), (310, 162, 185, 50), 2)    # cheats tab
            pyg.draw.rect(startScreen, (255,255,255), (342, 363, 125, 50), 2)  # singleplayer tab
            pyg.draw.rect(startScreen, (255,255,255), (320, 263, 167, 50), 2)  # multiplayer tab
                
        pyg.display.update()

        print(mode)
        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                END = True

            # detect if mouse button is pressed on buttons (and call appropriate functions)
            if event.type == pyg.MOUSEBUTTONDOWN:
                if (325) <= mouse[0] <= (325 + 100) and (175) <= mouse[1] <= (175 + 25):
                    import GameProjectSinglePlayer

                if (335) <= mouse[0] <= (335 + 100) and (275) <= mouse[1] <= (275 + 25):
                    import GameProjectOrganized

                if (360) <= mouse[0] <= (360 + 100) and (375) <= mouse[1] <= (375 + 25):
                    pass
 

        # call our setup function
        setup()

        # update display
        pyg.display.update()
        clock.tick(60)



pyg.init()

WIDTH = 800
HEIGHT = 480

startScreen = pyg.display.set_mode((WIDTH, HEIGHT))
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
mode = 1

main()
pyg.quit()
quit()
