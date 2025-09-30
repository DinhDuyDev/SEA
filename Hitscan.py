import math
from Smoke_And_Explosions import *
class Hitscan:
    list_of_hitscan = []

    def destroy(self):
        Hitscan.list_of_hitscan.remove(self)

    def __init__(self, x, y, damage, direction, range_, spawner):
        self.x = x
        self.y = y
        self.end_x = x + math.cos(math.radians(direction)) * range_
        self.end_y = y - math.sin(math.radians(direction)) * range_
        self.damage = damage
        self.range = range_
        self.direction = direction
        self.hit_radius = 14
        self.spawner = spawner

    def action(self):
        x, y = self.x, self.y
        while self.range > 0:
            x += math.cos(math.radians(self.direction)) * 4
            y -= math.sin(math.radians(self.direction)) * 4
            create_smoke(x, y, 10, color='white')
            self.range -= 4

    def get_damage(self):
        return self.damage

    def get_spawner(self):
        return self.spawner

    def get_hit_radius(self):
        return self.hit_radius

    def get_pos(self):
        return self.x, self.y, self.end_x, self.end_y


def create_hitscan(x, y, damage, direction, range_, spawner):
    Hitscan.list_of_hitscan.append(Hitscan(x, y, damage, direction, range_, spawner))