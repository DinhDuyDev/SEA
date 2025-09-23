import random
class Camera:
    screen_offset_x = 0
    screen_offset_y = 0
    shake_length = 0
    countdown = 0
    shake_amount = 0
    @staticmethod
    def update(self):
        strength_ratio = Camera.countdown / Camera.shake_length if Camera.shake_length != 0 else 0
        Camera.screen_offset_x = random.choice([-1, 1]) * strength_ratio * Camera.shake_amount
        Camera.screen_offset_y = random.choice([-1, 1]) * strength_ratio * Camera.shake_amount

        if Camera.countdown > 0:
            Camera.countdown -= 1

def screen_shake(magnitude, length):
    Camera.shake_length = length
    Camera.countdown = length
    Camera.shake_amount = magnitude

def cxy():
    return Camera.screen_offset_x, Camera.screen_offset_y