import pygame
pygame.mixer.init()
class Sounds:
    bullet_shoot = pygame.mixer.Sound('./sounds/shooting_sound.wav')
    bullet_shoot.set_volume(0.1)

    rocket_explosion = pygame.mixer.Sound('./sounds/rocket_explosion.wav')
    rocket_explosion.set_volume(0.565)

    rocket_firing = pygame.mixer.Sound('./sounds/rocket_firing.wav')
    rocket_firing.set_volume(0.25)

    rocket_firing1 = pygame.mixer.Sound('./sounds/rocket_firing_off.wav')
    rocket_firing1.set_volume(0.25)

    death_sound = pygame.mixer.Sound('./sounds/deathsound.wav')
    death_sound.set_volume(0.37)

    splitter_sound = pygame.mixer.Sound('./sounds/splitter_splitting.wav')
    splitter_sound.set_volume(0.25)

    splitter_shoot = pygame.mixer.Sound('./sounds/splitter_shoot.wav')
    splitter_shoot.set_volume(0.25)

    katana_sound = pygame.mixer.Sound('./sounds/katanasound.wav')
    katana_sound.set_volume(0.25)

    katana_hit_sound = pygame.mixer.Sound('./sounds/katana_hit_sound.wav')
    katana_hit_sound.set_volume(0.25)

    button_click_sound = pygame.mixer.Sound('./sounds/buttonclick.wav')
    button_click_sound.set_volume(0.25)

    keyboard_sound = pygame.mixer.Sound('./sounds/keyboard.wav')
    keyboard_sound.set_volume(0.25)

    delete_sound = pygame.mixer.Sound('./sounds/delete_sound.wav')
    delete_sound.set_volume(0.25)

    added_names_sound = pygame.mixer.Sound('./sounds/added_names.wav')
    added_names_sound.set_volume(0.25)

    rocket_trail = pygame.mixer.Sound('./sounds/rocket_trail.wav')
    rocket_trail.set_volume(0.4)

    rocket_launch = pygame.mixer.Sound('./sounds/rocketlaunch.wav')
    rocket_launch.set_volume(0.1)

    deleted_name = pygame.mixer.Sound('./sounds/deleted_names.wav')
    deleted_name.set_volume(0.25)

    shotgun_sound = pygame.mixer.Sound('./sounds/shotgun.wav')
    shotgun_sound.set_volume(0.25)

    sniper_sound = pygame.mixer.Sound('./sounds/sniper_supplement.wav')
    sniper_sound.set_volume(0.25)