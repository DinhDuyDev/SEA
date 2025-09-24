import pygame as pg
from pygame.locals import *
from settings import *
import pygame.time


class Game:
    FULLSCREEN = True
    screen = None
    draw_dest = None
    PAUSED = False
    level_editor = True
    giving_names = True

class NameQueue:
    names_queue = []

def set_full_screen():
    Game.screen = pg.display.set_mode((0, 0), pygame.FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
def set_not_full_screen():
    Game.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)

#class Button:
#    def __init__(self):

class TextBox:
    curr_name_string = ""

def get_name(event):
    if event.key == pygame.K_RETURN:
        NameQueue.names_queue.append(TextBox.curr_name_string)
    elif event.key == pygame.K_TAB:
        Game.giving_names = False
    elif event.key == pygame.K_BACKSPACE:
        TextBox.curr_name_string = TextBox.curr_name_string[:-1]
    else:
        TextBox.curr_name_string += event.key.unicode
def add_all_fighters_in_queue():
    for fn in NameQueue.names_queue:
        add_fighter(random.randrange(0, 640), random.randrange(0, 640), name=fn)

pg.init()
pg.font.init()

my_font = pygame.font.SysFont('./Kranky/Kranky-Regular.ttf', 15)

# All surfaces
Game.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
Game.draw_dest = Game.screen.copy()

pygame.display.set_caption('METALPOCALYPSE')

FIGHTER_SPRITE = pygame.image.load('sprites/fighter.png').convert_alpha()
BULLET_SPRITES = {
    "Bullet" : pygame.transform.scale_by(pygame.image.load('sprites/white_bullet.png').convert_alpha(), (1,0.5)),
    "Yellow Bullet" : pygame.transform.scale_by(pygame.image.load('sprites/bullet.png').convert_alpha(), (1,0.5)),
    "Splitter" : pygame.image.load('sprites/splitter_bullet.png').convert_alpha(),
    "Rocket" : pygame.image.load('sprites/rocket.png').convert_alpha()
}

WEAPONS = {
    "KATANA" : pygame.image.load('sprites/katana.png').convert_alpha(),
    "SHOTGUN" : pygame.image.load('sprites/shotgun.png').convert_alpha(),
    "MACHINEGUN": pygame.image.load('sprites/machinegun.png').convert_alpha(),
    "SPLITTER" : pygame.image.load('sprites/splitter.png').convert_alpha(),
    "MINIGUN" : pygame.image.load('sprites/minigun.png').convert_alpha(),
    "ROCKETLAUNCHER" : pygame.image.load('sprites/rocketlauncher.png').convert_alpha()
}