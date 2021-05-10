import pygame as pyg
import importlib


def display_text(text, x, y):
    hostScreen.blit(font.render(text, True, white), (x, y))


# STUFF FOR PRINTING TEXT TO SCREEN
def print_text(text, diff):
    message = font.render(text, True, white)
    message_rect = message.get_rect(center=(WIDTH/2, (HEIGHT/2) - diff))
    hostScreen.blit(message, message_rect)



def setup():
    # fills background with green (can potentially be changed to image file later)
    hostScreen.fill(green)
    # iterates through lists and draws appropriate objects
    
    hostScreen.blit(font.render('Start the Game', True, SG_Color), (315, 190))
    pyg.draw.rect(hostScreen, SG_Rect_Color, (307, 177, 185, 50), 2)
    print_text("You Are Host", 150)
    print_text("Waiting for Players to Join...", 100)




def host():
    global imported
    run = True
    while run:
        clock.tick(60)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pygame.quit()
                run = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                run = False
        setup()
        # update display
        pyg.display.update()
        clock.tick(60)
    try:
        #n.send("start")
        import client
    except:
        if imported == True:
            importlib.reload(Multiplayer)
        elif imported == False:
            imported = True
            import Multiplayer



pyg.init()

WIDTH = 800
HEIGHT = 450

hostScreen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Py-Jack")

# set color values
green = (34, 99, 43)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Set Text Color Values
SG_Color = white

# Set Rect Color Values
SG_Rect_Color = white

# set font for pygame
font = pyg.font.Font('freesansbold.ttf', 25)

# initiates clock and end parameter
clock = pyg.time.Clock()
END = False
mode = 1
imported = False

while True:
    host()
pyg.quit()
quit()
