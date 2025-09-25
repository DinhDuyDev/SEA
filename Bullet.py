import math
import random
from settings import *
from Smoke_And_Explosions import *
class Bullet:
    list_of_bullets = []

    def destroy(self):
        create_smoke(self.x, self.y, 7, (255, 0, 0))
        Bullet.list_of_bullets.remove(self)

    def update_self(self):
        if not (0 < self.x < WINDOW_WIDTH and 0 < self.y < WINDOW_HEIGHT):
            self.decay_countdown -= 1
        if self.decay_countdown < 0 or self.damage <= 0:
            if self.bullet_type == "Splitter":
                for i in range(12):
                    screen_shake(4, 15)
                    create_bullet(self.x, self.y, random.randrange(0, 360), None, spd_mlt=0.25, bullet_type="Yellow Bullet")
            elif self.bullet_type == "Rocket":
                self.damage = 35
                create_explosion(self.x, self.y, 96)
            self.destroy()

    def __init__(self, x, y, dir_, spawner, spd_mlt=1.0, damage=15, bullet_type="Bullet"):
        self.x = x
        self.y = y
        self.dir = dir_
        self.damage = damage
        self.spawner = spawner
        self.speed = random.randrange(6, 8)

        self.decay_countdown = 60
        self.speed_multiplier = spd_mlt
        self.bullet_type = bullet_type
        self.hit_radius = 9

        create_smoke(self.x + math.cos(math.radians(self.dir-7)) * 24
                     , self.y - math.sin(math.radians(self.dir-7)) * 24, 6, (255, 255, 255))

    def action(self):
        self.x += math.cos(math.radians(self.dir)) * self.speed
        self.y -= math.sin(math.radians(self.dir)) * self.speed

        if self.bullet_type == "Splitter" or self.bullet_type == "Rocket":
            self.hit_radius = 33

            if self.bullet_type == "Rocket":
                self.damage -= 0.5
                if self.damage % 2 == 0:
                    c = random.randrange(95, 138)
                    create_smoke(self.x, self.y, random.randrange(3, 5), (c, c, c))

        self.update_self()

    def get_damage(self):
        dam = self.damage
        self.damage = 0
        return dam

    def get_type(self):
        return self.bullet_type

def create_bullet(x, y, dir_, spawner, spd_mlt=1.0, damage=15, bullet_type="Bullet"):
    Bullet.list_of_bullets.append(Bullet(x, y, dir_, spawner, spd_mlt, damage, bullet_type))
