import pygame as pg
from pygame.locals import *
from settings import *
import pygame.time
from Smoke_And_Explosions import *
from Camera import *
from Fighter import *

## Initializing pygame
pg.init()
pg.font.init()

my_font = pygame.font.SysFont('./Kranky/Kranky-Regular.ttf', 15)

# Defining functions

def adding_names():
    for event in pg.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.running = False
            get_keys(event)

    names_surf = my_font.render(f"> {TextBox.curr_name_string} ", False, (255, 0, 0))
    names_rect = names_surf.get_rect(topleft=(64, 64))
    Game.draw_dest.blit(names_surf, names_rect)

    for i, v in enumerate(NameQueue.names_queue):
        names_surf_list = my_font.render(f"{i + 1} : {v}", False, (255, 0, 0))
        names_rect_list = names_surf.get_rect(topleft=(WINDOW_WIDTH / 2 + 64, i * 16 + 64))
        Game.draw_dest.blit(names_surf_list, names_rect_list)



def fighting():
    for event in pg.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.curr_state = "ADDING_NAMES"

            ######### Spawning players
            elif event.key == pygame.K_e:
                if len(Fighter.list_of_fighters) == 0 or len(Fighter.list_of_fighters) == 1:
                    Fighter.list_of_fighters.clear()
                    add_all_fighters_in_queue()
            elif event.key == pygame.K_p:
                Game.PAUSED = not Game.PAUSED

    ######### Logic block #########
    c = cxy()
    if not Game.PAUSED:
        Camera.update(None)
    ######### Moving fighters

    # While you are playing
    if not Game.giving_names:
        for f in Fighter.list_of_fighters:
            if not Game.PAUSED:
                f.action()
        for b in Bullet.list_of_bullets:
            if not Game.PAUSED:
                b.action()
                for f in Fighter.list_of_fighters:
                    if point_distance(b.x, b.y, f.x, f.y) < b.hit_radius and b.spawner is not f:
                        f.take_damage(b.get_damage())

        # print(len(Bullet.list_of_bullets))

        for b in Bullet.list_of_bullets:
            b_spr = pygame.transform.rotate(BULLET_SPRITES[b.get_type()], b.dir)
            Game.draw_dest.blit(b_spr, b_spr.get_rect(center=(b.x - c[0], b.y - c[1])))
            # pygame.draw.rect(Game.draw_dest, (255, 255, 255), (b.x - 2, b.y - 2, 2, 2))

        ######## Drawing block (cont) ########
        for f in Fighter.list_of_fighters:
            if f.hp > 0:
                col = f.color
                unique_tint = pygame.Surface((13, 13))
                unique_tint.fill(col)
                unique_tint.set_alpha(128)
                Game.draw_dest.blit(FIGHTER_SPRITE, FIGHTER_SPRITE.get_rect(center=(f.x - c[0], f.y - c[1])))
                Game.draw_dest.blit(unique_tint, unique_tint.get_rect(center=(f.x - c[0], f.y - c[1])))

                w = pygame.transform.rotate(WEAPONS[f.get_weapon_sprite()], f.get_weapon_direction())
                Game.draw_dest.blit(w, w.get_rect(center=(f.x - c[0], f.y + 5 - c[1])))

                text_surf = my_font.render(f.get_name(), False, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(f.x, f.y - 16))
                Game.draw_dest.blit(text_surf, text_rect)

                pygame.draw.rect(Game.draw_dest, (255, 0, 0), (f.x - 16 - c[0], f.y + 8 - c[1], 32, 6))
                pygame.draw.rect(Game.draw_dest, (82, 14, 125),
                                 (f.x - 16 - c[0], f.y + 8 - c[1], (f.get_recovery_health() / Fighter.full_health) * 32,
                                  6))
                pygame.draw.rect(Game.draw_dest, (0, 255, 0),
                                 (f.x - 16 - c[0], f.y + 8 - c[1], (f.get_health() / Fighter.full_health) * 32, 6))

        for s in Smoke.list_of_smoke:
            if not Game.PAUSED:
                s.action()
            pygame.draw.circle(Game.draw_dest, s.get_color(), (s.x - c[0], s.y - c[1]), s.radius)

        for st in SmokeTrail.list_of_smoke_trails:
            if not Game.PAUSED:
                st.action()

        for e in Explosion.list_of_explosion:
            if not Game.PAUSED:
                for fi in Fighter.list_of_fighters:
                    dist = point_distance(fi.x, fi.y, e.x, e.y)
                    if dist < e.radius:
                        fi.take_damage(e.radius - dist)
                        dir_to_player = point_direction(e.x, e.y, fi.x, fi.y)
                        fi.take_knockback(random.randrange(3, 6), dir_to_player)
                e.explode()


class Game:
    FULLSCREEN = True
    screen = None
    draw_dest = None
    PAUSED = False
    level_editor = True
    giving_names = True
    running = True
    curr_state = "ADDING_NAMES"

    states = {
        "MENU" : None,
        "ADDING_NAMES" : adding_names,
        "FIGHTING" : fighting
    }

Game.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
Game.draw_dest = Game.screen.copy()


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

def get_keys(event):
    if event.key == pygame.K_RETURN:
        NameQueue.names_queue.append(TextBox.curr_name_string)
        TextBox.curr_name_string = ""
    elif event.key == pygame.K_TAB:
        Game.giving_names = False # Move into play mode!
        Game.curr_state = "FIGHTING"
    elif event.key == pygame.K_BACKSPACE:
        TextBox.curr_name_string = TextBox.curr_name_string[:-1]
    elif event.key == pygame.K_g:
        if len(NameQueue.names_queue) != 0:
            NameQueue.names_queue.pop()
    else:
        if event.key != pygame.K_ESCAPE: #and Game.giving_names:
            TextBox.curr_name_string += event.unicode

def add_all_fighters_in_queue():
    for fn in NameQueue.names_queue:
        add_fighter(random.randrange(0, 640), random.randrange(0, 640), name=fn)


pygame.display.set_caption('AI SUPER SHOWDOWN')

FIGHTER_SPRITE = pygame.image.load('sprites/fighter.png').convert_alpha()
BULLET_SPRITES = {
    "Bullet" : pygame.transform.scale_by(pygame.image.load('sprites/white_bullet.png').convert_alpha(), (1,0.5)),
    "Yellow Bullet" : pygame.transform.scale_by(pygame.image.load('sprites/bullet.png').convert_alpha(), (1,0.5)),
    "Splitter" : pygame.image.load('sprites/splitter_bullet.png').convert_alpha(),
    "Rocket" : pygame.image.load('sprites/rocket.png').convert_alpha()
}

WEAPONS = {
    "KATANA" : pygame.transform.scale_by(pygame.image.load('sprites/katana.png').convert_alpha(), (2, 1)),
    "SHOTGUN" : pygame.image.load('sprites/shotgun.png').convert_alpha(),
    "MACHINEGUN": pygame.image.load('sprites/machinegun.png').convert_alpha(),
    "SPLITTER" : pygame.image.load('sprites/splitter.png').convert_alpha(),
    "MINIGUN" : pygame.image.load('sprites/minigun.png').convert_alpha(),
    "ROCKETLAUNCHER" : pygame.image.load('sprites/rocketlauncher.png').convert_alpha()
}