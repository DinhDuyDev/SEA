import pygame
pygame.mixer.init()
class Sounds:
    bullet_shoot = pygame.mixer.Sound('./sounds/normal_calibre_shoot.wav')
    bullet_shoot.set_volume(0.25)

    rocket_explosion = pygame.mixer.Sound('./sounds/rocket_explosion.wav')
    rocket_explosion.set_volume(0.75)

    rocket_firing = pygame.mixer.Sound('./sounds/rocket_firing.wav')
    rocket_firing.set_volume(0.5)

    death_sound = pygame.mixer.Sound('./sounds/deathsound.wav')
    death_sound.set_volume(0.75)

    splitter_sound = pygame.mixer.Sound('./sounds/splitter_splitting.wav')
    splitter_sound.set_volume(0.5)

    katana_sound = pygame.mixer.Sound('./sounds/katanasound.wav')
    katana_sound.set_volume(0.5)

    katana_hit_sound = pygame.mixer.Sound('./sounds/katana_hit_sound.wav')
    katana_hit_sound.set_volume(0.5)