import pygame
import math
import random
from functions import *
from settings import *
from Bullet import *
from Camera import *

class Fighter:
    fighter_id = 0
    full_health = 1_000
    list_of_fighters = []
    kill_feed = ""

    kill_message = {
        "MACHINEGUN" : [
            "{k} Killed {v} With A Machine Gun",
            "{k} Riddled {v} With Bullets",
            "{v} Was Shot Up By {k}",
            "{k} Pointed The Funny Pipe At {v}",
        ],

        "SHOTGUN" : [
            "{k} Killed {v} With A shotgun",
            "{k} Blasted Away {v} With a 12 gauge",
            "{v} Was Perforated By {k}",
            "{k} Shotgunned {v} (Painfully)",
            "{k} Pointed The Funny Stick At {v}"
        ],
        "MINIGUN" : [
            "{k} Killed {v} With A Minigun",
            "{v} Ate A Risotto Of Lead From {k}",
            "{v} Tasted {k} 's Bullets",
            "{v} Stood Too Still And {k} Was Too Trigger Happy"
        ],

        "SPLITTER" : [
            "{k} Killed {v} With The Splitter",
            "{v} Ate A Bomb From {k}",
            "{k} Gave {v} Some Nails To Eat",
        ],
        'ROCKETLAUNCHER' : [
            "{k} Killed {v} With A Rocket Launcher",
            "{v} Rode {k} 's Rocket Into Heaven",
            "{k} Was Blown Apart By {v}",
        ],
        "KATANA" : [
            "{k} TENNO HEIKA BANZAI!!!!!!! {v}",
            "{k} Slashed {v} Open",
            "{k} Turned Anime And {v} Turned Corpse"
        ]
    }

    def destroy(self):
        screen_shake(3, 30)
        for i in range(12):
            create_smoke_trail(self.x, self.y, random.randrange(0, 360), (random.randrange(0, 255)
                                                                              , random.randrange(0, 255)
                                                                              , random.randrange(0, 255)))
        for i in range(4):
            create_smoke(self.x + random.randrange(-12, 12), self.y + random.randrange(-12, 12)
                         , random.randrange(12, 16), (random.randrange(0, 255)
                                                                        , random.randrange(0, 255)
                                                                        , random.randrange(0, 255)))
        if self.killer is not None:
            kill = ""
            if self.killer is not self:
                ls = random.choice(Fighter.kill_message[self.kill_type]).split(" ")
                for i in range(len(ls)):
                    if ls[i] == "{k}":
                        ls[i] = self.killer.get_name()
                    elif ls[i] == "{v}":
                        ls[i] = self.name
                kill = " ".join(ls)
            else:
                kill = random.choice(
                    [
                        f"{self.name} no longer has that dog in them :(",
                        f"{self.name} sees no point in life anymore :(",
                        f"{self.name}, I feel bad for :("
                    ]
                )
            Fighter.kill_feed = kill
        Fighter.list_of_fighters.remove(self)

    def route_enemy_left(self):
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) + 90
        self.x += math.cos(math.radians(direction_to_target)) * 2.0
        self.y -= math.sin(math.radians(direction_to_target)) * 2.0

    def route_enemy_right(self):
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) - 90
        self.x += math.cos(math.radians(direction_to_target)) * 2.0
        self.y -= math.sin(math.radians(direction_to_target)) * 2.0

    def tackle_enemy(self):
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1])

        self.x += math.cos(math.radians(direction_to_target)) * 7.0
        self.y -= math.sin(math.radians(direction_to_target)) * 7.0

        self.x += math.cos(math.radians(random.randrange(0, 360))) * 2
        self.y -= math.sin(math.radians(random.randrange(0, 360))) * 2

    def back_away_enemy(self):
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) + 180
        self.x += math.cos(math.radians(direction_to_target)) * 3.25
        self.y -= math.sin(math.radians(direction_to_target)) * 3.25

    def move_random(self):
        self.x += math.cos(math.radians(self.movement_direction)) * 3.0
        self.y -= math.cos(math.radians(self.movement_direction)) * 3.0

    def change_direction(self):
        self.movement_direction = random.randrange(0, 360)


    def shotgun_enemy(self):
        rof_end = 30
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1])
        self.weapon_direction = direction_to_target
        if self.ROF > rof_end:
            for i in range(7):
                #create_bullet(self.x, self.y, direction_to_target, 15, self)
                direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) + random.randrange(-7, 7)
                create_bullet(self.x, self.y, direction_to_target, self, damage=3, kill_weapon=self.weapon_sprites[self.attack])
            self.ROF = 0
        self.ROF += 1

    def machine_gun_enemy(self):
        rof_end = 5
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) + random.randrange(-5, 5)
        self.weapon_direction = direction_to_target
        if self.ROF > rof_end:
            create_bullet(self.x, self.y, direction_to_target, self, 2, kill_weapon=self.weapon_sprites[self.attack])
            self.ROF = 0
        self.ROF += 1

    def minigun_enemy(self):
        rof_end = 1
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) + random.randrange(-4, 4)
        self.weapon_direction = direction_to_target
        if self.ROF > rof_end:
            screen_shake(1, 15)
            create_bullet(self.x, self.y, direction_to_target, self, 3, kill_weapon=self.weapon_sprites[self.attack])
            self.ROF = 0
        self.ROF += 1

    def splitter_enemy(self):
        rof_end = 50
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1]) + random.randrange(-4, 4)
        self.weapon_direction = direction_to_target
        if self.ROF > rof_end:
            create_bullet(self.x, self.y, direction_to_target, self, 1.75, bullet_type="Splitter", kill_weapon=self.weapon_sprites[self.attack])
            self.ROF = 0
        self.ROF += 1

    def rocket_launcher(self):
        rof_end = 75
        target_pos = self.target.get_pos()
        direction_to_target = point_direction(self.x, self.y, target_pos[0], target_pos[1])
        self.weapon_direction = direction_to_target
        if self.ROF > rof_end:
            create_bullet(self.x, self.y, direction_to_target, self, 3, bullet_type="Rocket", damage=45, kill_weapon=self.weapon_sprites[self.attack])
            self.ROF = 0
        self.ROF += 1

    def slash_enemy(self):
        rof_end = 5
        self.weapon_direction += 40
        c = random.randrange(70, 255)
        create_smoke(self.x + math.cos(self.weapon_direction) * 15
                     , self.y - math.sin(self.weapon_direction) * 15
                     , 6
                     , (0, 0, c))

        if self.ROF > rof_end:
            target_pos = self.target.get_pos()
            if point_distance(self.x, self.y, target_pos[0], target_pos[1]) < 12:
                self.target.hp -= 15
                self.target.killer = self
                self.target.kill_type = "KATANA"
                self.target.take_knockback(4, self.weapon_direction)
                c = random.randrange(70, 255)
                create_smoke_trail(self.x, self.y, random.randrange(0, 360), (c, 0, 0))
            self.ROF = 0
        self.ROF += 1

    def update_position(self):
        self.x = min(max(16, self.x), WINDOW_WIDTH-16)
        self.y = min(max(16, self.y), WINDOW_HEIGHT-16)

    # Arguments of the add fighter function is becoming bloated.
    def __init__(self, x, y, name=f"NONAME{fighter_id}", hp=full_health):
        self.x = x
        self.y = y
        self.hp = hp
        self.recovery_hp = hp

        self.name = name
        self.hurt_cooldown = 0
        self.move_dir = 0
        self.fighter_id = Fighter.fighter_id
        self.ROF = 0
        Fighter.fighter_id += 1

        self.knockback = 0
        self.knockback_dir = 0

        self.target = None

        self.states_list = [ # {movement_function, attack_function, duration, next_pointer
            {"movement_function" : self.route_enemy_left, "attack_function" : -1, "duration" : 2.75 * 60, "next_pointer" : -1, "endstate" : -1,
             "spec_name" : "ROUTE1"},
            {"movement_function": self.route_enemy_right, "attack_function": -1, "duration": 2.75 * 60, "endstate" : -1,
             "next_pointer": -1,
             "spec_name": "ROUTE2"},
            {"movement_function": self.tackle_enemy, "attack_function" : self.slash_enemy, "duration": 2.5 * 60, "next_pointer": -1, "endstate" : -1,
             "spec_name" : "TACKLE"},

            ### MOVING RANDOMLY
            {"movement_function": self.move_random, "attack_function":
                -1  # self.minigun_enemy
                , "duration": 0.25 * 60, "next_pointer": 4, "endstate" : self.change_direction,
             "spec_name": "RAND_MOVE"},
            {"movement_function": self.move_random, "attack_function":
                -1  # self.minigun_enemy
                , "duration": 0.25 * 60, "next_pointer": 5, "endstate": self.change_direction,
             "spec_name": "RAND_MOVE"},
            {"movement_function": self.move_random, "attack_function":
                -1  # self.minigun_enemy
                , "duration": 0.25 * 60, "next_pointer": 6, "endstate": self.change_direction,
             "spec_name": "RAND_MOVE"},
            {"movement_function": self.move_random, "attack_function":
                -1  # self.minigun_enemy
                , "duration": 0.25 * 60, "next_pointer": -1, "endstate": self.change_direction,
             "spec_name": "RAND_MOVE"},

            {"movement_function": self.back_away_enemy, "attack_function" : -1, "duration": 1 * 60, "next_pointer": -1, "endstate" : -1,
             "spec_name" : "BACKOFF"},
            {"movement_function": self.route_enemy_left, "attack_function":
                -1#self.minigun_enemy
                , "duration": 4 * 60, "next_pointer": -1, "endstate" : -1,
             "spec_name": "MINIGUN"}
        ]

        self.weapon_sprites = {
            self.machine_gun_enemy : "MACHINEGUN",
            self.shotgun_enemy : "SHOTGUN",
            self.minigun_enemy : "MINIGUN",
            self.splitter_enemy : "SPLITTER",
            self.rocket_launcher : 'ROCKETLAUNCHER',
            self.slash_enemy : "KATANA"
        }

        self.movement_direction = 0

        self.weapon_direction = 0

        self.killer = None
        self.kill_type = None

        # ALL RANDOMIZABLE ATTACK PATTERNS MUST GO HERE
        self.attacks_list = [
            self.machine_gun_enemy,
            self.shotgun_enemy,
            self.splitter_enemy,
            self.rocket_launcher,
            self.minigun_enemy
        ]
        self.state = random.choice(self.states_list)
        self.attack = random.choice(self.attacks_list) if self.state["attack_function"] == -1 else self.state["attack_function"]

        self.state_countdown = 0

        self.re_target_countdown = 0

        self.color = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))

        # Dramatic explosion effect
        create_explosion(self.x, self.y, 0)

    # ALSO DEFINES THE GAME'S WIN STATE FOR SOME DAMNED REASON
    def target_fighter(self):
        if len(Fighter.list_of_fighters) > 1:
            ls = Fighter.list_of_fighters[:]
            ls.remove(self)

            self.target = random.choice(ls)
            while self.target.get_health() <= 0:
                self.target = random.choice(ls)
        else:
            self.target = None
            self.hp = Fighter.full_health

    def action(self):
        if self.target is None: # Triggers to fight
            self.target_fighter()
        else:
            ### Ending states
            if self.re_target_countdown >= random.randrange(2, 4) * 60:
                self.target_fighter()
                self.re_target_countdown = 0
            else:
                self.re_target_countdown += 1

            # State machine
            curr_state = self.state

            # If the countdown to a state is over, then switch state, performing any last actions
            if self.state_countdown > curr_state["duration"]:
                self.state = self.states_list[random.randint(0, len(self.states_list)-1)] if curr_state["next_pointer"] == -1 else self.states_list[curr_state["next_pointer"]]
                self.attack = random.choice(self.attacks_list) if self.state["attack_function"] == -1 else self.state["attack_function"]
                self.state_countdown = 0
                if curr_state["endstate"] != -1:
                    curr_state["endstate"]()
            else:
                self.state_countdown += 1

            # Use your attacks
            self.attack()
            if curr_state["movement_function"] is not None:
                curr_state["movement_function"]()
            self.update_position()

            if self.target.get_health() <= 0:
                self.target = None

        # HP reduction
        if self.hurt_cooldown <= 0:
            self.recovery_hp = max(self.recovery_hp * 0.9, self.hp)
        else:
            self.hurt_cooldown -= 1
        # Apply knockback
        self.knockback = max(self.knockback - 0.1, 0)
        self.x += math.cos(math.radians(self.knockback_dir)) * self.knockback
        self.y -= math.sin(math.radians(self.knockback_dir)) * self.knockback

        # Death, then destroy self (aka remove yourself from the list)
        if self.hp <= 0:
            self.destroy()


    def take_damage(self, damage_amount):
        self.hp -= damage_amount
        self.hurt_cooldown = 30

    def take_knockback(self, knockback_speed, knockback_direction):
        self.knockback = knockback_speed
        self.knockback_dir = knockback_direction

    def get_health(self):
        return self.hp

    def get_recovery_health(self):
        return self.recovery_hp

    def get_pos(self):
        return self.x, self.y

    def get_id(self):
        return self.fighter_id

    def get_name(self):
        return self.name

    def get_weapon_sprite(self):
        return self.weapon_sprites[self.attack]

    def get_weapon_direction(self):
        return self.weapon_direction

def add_fighter(x=random.randrange(0, 640), y=random.randrange(0, 320), name=f"NONAME{Fighter.fighter_id}"):
    Fighter.list_of_fighters.append(Fighter(x, y, name, Fighter.full_health))





