import random
import math
from Camera import *
class Smoke:
    list_of_smoke = []
    def __init__(self, x, y, radius, color=(128, 128, 128)):
        self.x = x
        self.y = y
        self.radius = radius
        self.reduction_speed = 0
        self.color = color
    def destroy(self):
        Smoke.list_of_smoke.remove(self)
    def action(self):
        if self.radius < 0:
            self.destroy()
        self.radius -= self.reduction_speed
        self.reduction_speed += 0.1
    def get_color(self):
        return self.color

def create_smoke(x, y, radius, color=(128, 128, 128)):
    Smoke.list_of_smoke.append(Smoke(x, y, radius, color))

class SmokeTrail:
    list_of_smoke_trails = []
    def __init__(self, x, y, direction, color=(128, 128, 128)):
        self.x = x
        self.y = y
        self.speed = random.randrange(3, 5)
        self.direction = direction
        self.timing = random.randrange(1, 2) * 60
        self.countdown = 0
        self.color = color
    def destroy(self):
        SmokeTrail.list_of_smoke_trails.remove(self)

    def action(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y -= math.sin(math.radians(self.direction)) * self.speed
        self.timing -= 1
        if self.countdown > 1:
            self.countdown = 0
            create_smoke(self.x, self.y, random.randrange(4, 10), self.color)
        else:
            self.countdown += 1

        if self.timing <= 0:
            self.destroy()

def create_smoke_trail(x, y, direction=random.randrange(0, 360), color=(128, 128, 128)):
    SmokeTrail.list_of_smoke_trails.append(SmokeTrail(x, y, direction, color))

class Explosion:
    list_of_explosion = []
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        screen_shake(6, 30)
    def destroy(self):
        Explosion.list_of_explosion.remove(self)
    def explode(self):
        for i in range(7):
            create_smoke_trail(self.x, self.y, random.randrange(0, 360), color=(255, 255, 255))
        create_smoke(self.x, self.y, 48, (255, 255, 255))
        self.destroy()

def create_explosion(x, y, radius):
    Explosion.list_of_explosion.append(Explosion(x, y, radius))