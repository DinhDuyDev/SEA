import pygame as pg
from pygame.locals import *
import pygame.time
from Fighter import *

## Initializing pygame
pg.init()
pg.font.init()

my_font = pygame.font.SysFont("Verdana", 10)
first_run = True
# Defining functions

class Button:
    list_of_buttons = []
    def __init__(self, x, y, w, h, text, room, color=(180, 0, 0), special_effects="None"):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.scene = room

        self.special_effects = special_effects

        self.hor_bounds = (x - w / 2, x + w / 2)
        self.ver_bounds = (y - h / 2, y + h / 2)

        self.color = color
        self.og_color = color
        self.text_surf = my_font.render(self.text, False, color)
        self.button_rect = pygame.Rect(x, y, w, h)

        self.button_rect.center = x, y

        Button.list_of_buttons.append(self)

    def action(self):
        oc = self.og_color
        self.text_surf = my_font.render(self.text, False, self.color)
        if self.button_rect.collidepoint(mouse_coords()[0], mouse_coords()[1]):
            self.color = (min(oc[0]*2, 255), min(oc[1]*2, 255), min(oc[2]*2, 255))
        else:
            self.color = (oc[0], oc[1], oc[2])


class NameQueue:
    names_queue = []

class TextBox:
    curr_name_string = ""

class OnDemandText:
    list_of_text = []
    def __init__(self, x, y, text, countdown=60, scale=1, color=(255, 0, 0), alignment="center"):
        self.x = x
        self.y = y
        self.text = text
        self.og_c = countdown
        self.countdown = countdown
        self.text_surf = pygame.transform.scale_by(my_font.render(text, False, color), scale)
        self.text_rect = self.text_surf.get_rect(center=(self.x, self.y))

        if alignment == "left":
            self.text_rect = self.text_surf.get_rect(left=(self.x, self.y))
        elif alignment == "right":
            self.text_rect = self.text_surf.get_rect(right=(self.x, self.y))

        OnDemandText.list_of_text.append(self)

    def action(self):
        self.countdown -= 1
        if self.countdown <= 0:
            OnDemandText.list_of_text.remove(self)
        if self.countdown <= self.og_c:
            self.text_surf.set_alpha(255 * (self.countdown / self.og_c))


class Text:
    list_of_text = []
    def __init__(self, x, y, text, room, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.text = text

        self.text_surf = pygame.transform.scale_by(my_font.render(text, False, color), 2)
        self.text_rect = self.text_surf.get_rect(center=(self.x, self.y))

        self.scene = room
        Text.list_of_text.append(self)

    #def action(self):


def menu_room():
    mx, my = mouse_coords()
    start_game = [b for b in Button.list_of_buttons if b.text == "START GAME"][0]
    end_game = [b for b in Button.list_of_buttons if b.text == "EXIT GAME"][0]

    for event in pg.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_game.button_rect.collidepoint(mx, my):
                Game.curr_state = "ADDING_NAMES"
                Sounds.button_click_sound.play(0)
            elif end_game.button_rect.collidepoint(mx, my):
                Game.running = False

def adding_names():
    add_name_button = [b for b in Button.list_of_buttons if b.text == "Add Name"][0]
    delete_name_button = [b for b in Button.list_of_buttons if b.text == "Delete Name"][0]
    proceed_button = [b for b in Button.list_of_buttons if b.text == "Proceed to fight!"][0]

    def get_keys(e):
        if e.key == pygame.K_BACKSPACE:
            Sounds.delete_sound.play(0)
            TextBox.curr_name_string = TextBox.curr_name_string[:-1]
        elif e.key == pygame.K_RETURN:
            if len(NameQueue.names_queue) < PLAYER_LIMIT:
                Sounds.added_names_sound.play(0)
                NameQueue.names_queue.append(TextBox.curr_name_string)
                TextBox.curr_name_string = ""
            else:
                OnDemandText(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, f"Maximum: {PLAYER_LIMIT} names.")
        else:
            if event.unicode.isalpha() or event.unicode == " ":  # and Game.giving_names:
                if len(TextBox.curr_name_string) < 20:
                    Sounds.keyboard_sound.play(0)
                    TextBox.curr_name_string += event.unicode
                else:
                    OnDemandText(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, "Names must be fewer than 20 letters",
                                 countdown=60, scale=2)

    for event in pg.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Sounds.button_click_sound.play(0)
                Game.curr_state = "MENU"
            get_keys(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = mouse_coords()[0], mouse_coords()[1]
            if add_name_button.button_rect.collidepoint(mx, my):
                if len(NameQueue.names_queue) < PLAYER_LIMIT:
                    Sounds.added_names_sound.play(0)
                    NameQueue.names_queue.append(TextBox.curr_name_string)
                    TextBox.curr_name_string = ""
                else:
                    OnDemandText(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, f"Maximum: {PLAYER_LIMIT} names.")
            elif delete_name_button.button_rect.collidepoint(mx, my):
                if len(NameQueue.names_queue) != 0:
                    NameQueue.names_queue.pop()
                    Sounds.deleted_name.play(0)
            elif proceed_button.button_rect.collidepoint(mx, my):
                Sounds.button_click_sound.play(0)
                if len(NameQueue.names_queue) >= PLAYER_MINIMUM:
                    Game.giving_names = False  # Move into play mode!
                    Game.curr_state = "FIGHTING"
                else:
                    OnDemandText(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, f"Minimum: {PLAYER_MINIMUM} names.")

    names_surf = my_font.render(f"> {TextBox.curr_name_string}|", False, (255, 0, 0))
    names_rect = names_surf.get_rect(topleft=(128, 64))
    Game.draw_dest.blit(names_surf, names_rect)

    for i, v in enumerate(NameQueue.names_queue):
        names_surf_list = my_font.render(f"{i + 1} : {v}", False, (255, 0, 0))
        names_rect_list = names_surf.get_rect(topleft=(WINDOW_WIDTH / 2 + 128, i * 16 + 64))
        Game.draw_dest.blit(names_surf_list, names_rect_list)



def fighting():
    for event in pg.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.curr_state = "ADDING_NAMES"
                Sounds.button_click_sound.play(0)

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
    for f in Fighter.list_of_fighters:
        if not Game.PAUSED:
            f.action()

    for b in Bullet.list_of_bullets:
        if not Game.PAUSED:
            b.action()
            for f in Fighter.list_of_fighters:
                if point_distance(b.x, b.y, f.x, f.y) < b.hit_radius and b.spawner is not f:
                    f.take_damage(b.get_damage())
                    f.killer = b.spawner
                    f.kill_type = b.kill_weapon


    for b in Bullet.list_of_bullets:
        b_spr = pygame.transform.rotate(BULLET_SPRITES[b.get_type()], b.dir)
        Game.draw_dest.blit(b_spr, b_spr.get_rect(center=(b.x - c[0], b.y - c[1])))

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
            dx = math.cos(math.radians(f.get_weapon_direction())) * 8
            dy = -math.sin(math.radians(f.get_weapon_direction())) * 8
            Game.draw_dest.blit(w, w.get_rect(center=(f.x - c[0]+dx, f.y + 5 - c[1]+dy)))

            text_surf = my_font.render(f.get_name(), False, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(f.x, f.y - 16))
            Game.draw_dest.blit(text_surf, text_rect)


    for s in Smoke.list_of_smoke:
        if not Game.PAUSED:
            s.action()
        pygame.draw.circle(Game.draw_dest, s.get_color(), (s.x - c[0], s.y - c[1]), s.radius)

    for st in SmokeTrail.list_of_smoke_trails:
        if not Game.PAUSED:
            st.action()

    for h in Hitscan.list_of_hitscan:
        h.action()
        x, y, end_x, end_y = h.get_pos()
        damage = h.get_damage()
        rad = h.get_hit_radius()
        spawner = h.get_spawner()
        h.destroy()

        for f in Fighter.list_of_fighters:
            if point_distance_perpendicular(f.x, f.y, x, y, end_x, end_y) < rad:
                if spawner is not f:
                    f.take_damage(damage)

    for e in Explosion.list_of_explosion:
        if not Game.PAUSED:
            for fi in Fighter.list_of_fighters:
                dist = point_distance(fi.x, fi.y, e.x, e.y)
                if dist < e.radius:
                    fi.take_damage(e.radius - dist)
                    dir_to_player = point_direction(e.x, e.y, fi.x, fi.y)
                    fi.take_knockback(random.randrange(3, 6), dir_to_player)
            e.explode()

    for f in Fighter.list_of_fighters:
        if f.get_health() > 0:
            pygame.draw.rect(Game.draw_dest, (255, 0, 0), (f.x - 16 - c[0], f.y + 8 - c[1], 32, 6))
            pygame.draw.rect(Game.draw_dest, (82, 14, 125),
                             (f.x - 16 - c[0], f.y + 8 - c[1], (f.get_recovery_health() / Fighter.full_health) * 32,
                              6))
            pygame.draw.rect(Game.draw_dest, (0, 255, 0),
                             (f.x - 16 - c[0], f.y + 8 - c[1], (f.get_health() / Fighter.full_health) * 32, 6))

    # if Fighter.kill_feed != "":
    #     OnDemandText.list_of_text.clear()
    #     OnDemandText(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 128, Fighter.kill_feed, 180, 2)
    #     Fighter.kill_feed = ""

    if len(Fighter.list_of_fighters) == 1:
        OnDemandText(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, f"{Fighter.list_of_fighters[0].name} won!", 30, 2)


class Game:
    FULLSCREEN = True
    screen = None
    draw_dest = None
    PAUSED = False
    level_editor = True
    giving_names = True
    running = True
    curr_state = "MENU"

    states = {
        "MENU" : menu_room,
        "ADDING_NAMES" : adding_names,
        "FIGHTING" : fighting
    }

Game.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
Game.draw_dest = Game.screen.copy()


def add_all_fighters_in_queue():
    for fn in NameQueue.names_queue:
        add_fighter(random.randrange(64, WINDOW_WIDTH-64), random.randrange(64, WINDOW_HEIGHT-64), name=fn)

def mouse_coords():
    x = pygame.mouse.get_pos()[0] / (Game.screen.get_rect().width / Game.draw_dest.get_width())
    y = pygame.mouse.get_pos()[1] / (Game.screen.get_rect().height / Game.draw_dest.get_height())
    return x, y

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
    "ROCKETLAUNCHER" : pygame.image.load('sprites/rocketlauncher.png').convert_alpha(),
    "SNIPER" : pygame.image.load('sprites/sniper.png').convert_alpha()
}