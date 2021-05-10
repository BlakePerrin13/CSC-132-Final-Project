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
    multiplayerScreen.blit(font.render(text, True, white), (x, y))

def setup():
    # fills background with green (can potentially be changed to image file later)
    multiplayerScreen.fill(green)
    # iterates through lists and draws appropriate objects
    
    multiplayerScreen.blit(font.render('Multiplayer', True, white), (330, 75))
    multiplayerScreen.blit(font.render('Back', True, Back_Color), (100, 75))
    multiplayerScreen.blit(font.render('Start a Server', True, SS_Color), (315, 190))
    multiplayerScreen.blit(font.render('Join a Server', True, JS_Color), (320, 300))
    pyg.draw.rect(multiplayerScreen, JS_Rect_Color, (310, 285, 180, 50), 2)
    pyg.draw.rect(multiplayerScreen, SS_Rect_Color, (307, 177, 185, 50), 2)
    pyg.draw.rect(multiplayerScreen, Back_Rect_Color, (90, 67, 80, 40), 2)
    

def main():

    global imported
    global mode
    global white
    global blue
    global JS_Color
    global SS_Color
    global END
    while not END:
        if GPIO:
            if GPIO.input(CONFIRM) == GPIO.HIGH:
                sleep(0.250)
                if mode == 1:
                    if imported == True:
                        importlib.reload(StartScreen)
                    elif imported == False:
                        imported = True
                        import StartScreen
                elif mode == 2:
                    import host
                elif mode == 3:
                    import client
                    
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
        if GPIO:
            if mode == 3:
                Back_Rect_Color = white
                SS_Rect_Color = white
                JS_Rect_Color = blue
            
            elif mode == 2:
                Back_Rect_Color = white
                SS_Rect_Color = blue
                JS_Rect_Color = white
            
            elif mode == 1:
                SS_Rect_Color = white
                JS_Rect_Color = white
                Back_Rect_Color = Blue
                
        pyg.display.update()

        # get mouse x and y coordinates
        mouse = pyg.mouse.get_pos()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                END = True

            # detect if mouse button is pressed on buttons (and call appropriate functions)
            if event.type == pyg.MOUSEBUTTONDOWN:
                if (315) <= mouse[0] <= (315 + 200) and (190) <= mouse[1] <= (190 + 25):
                    import client

                if (320) <= mouse[0] <= (320 + 200) and (300) <= mouse[1] <= (300 + 25):
                    import client

                if (100) <= mouse[0] <= (100 + 75) and (75) <= mouse[1] <= (75 + 25):
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

multiplayerScreen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Py-Jack")

# set color values
green = (34, 99, 43)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Set Text Color Values
SS_Color = white
JS_Color = white
Back_Color = white

# Set Rect Color Values
SS_Rect_Color = white
JS_Rect_Color = white
Back_Rect_Color = white

# set font for pygame
font = pyg.font.Font('freesansbold.ttf', 25)

# initiates clock and end parameter
clock = pyg.time.Clock()
END = False
mode = 1
imported = False

main()
pyg.quit()
quit()
