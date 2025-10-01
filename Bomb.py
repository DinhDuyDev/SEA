from Smoke_And_Explosions import *
class Bomb:
    list_of_bombs = []
    def destroy(self):
        create_explosion(self.x, self.y, 64, self.spawner, create_ray=False)
        Bomb.list_of_bombs.remove(self)
    def __init__(self, x, y, direction, spawner):
        self.x = x
        self.y = y
        self.timer = random.randrange(2 * 60, 5 * 60)
        self.speed = random.randrange(4, 8)
        self.direction = direction
        self.rand_dir = random.randrange(0, 360)
        self.spawner = spawner
        Bomb.list_of_bombs.append(self)

    def action(self):
        self.speed = max(self.speed - 0.1, 0)
        self.rand_dir += self.speed
        if self.timer <= 0:
            self.destroy()
        else:
            self.timer -= 1

        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y -= math.sin(math.radians(self.direction)) * self.speed

def create_bomb(x, y, direction, spawner):
    Bomb(x, y, direction, spawner)