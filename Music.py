import pygame

class Music(object):
    pygame.mixer.init()
    volume = 0.5
    background_instrumental = pygame.mixer.Sound('sounds/Bimbi_Instrumental.wav')
    click = pygame.mixer.Sound('sounds/click.wav')
    walk = pygame.mixer.Sound('sounds/gameplay/walk2.wav')
    pick_powerup = pygame.mixer.Sound('sounds/gameplay/powerup.wav')
    raygun_sound = pygame.mixer.Sound('sounds/gameplay/raygun_sound.wav')
    shotgun_sound = pygame.mixer.Sound('sounds/gameplay/shotgun_sound.wav')
    pablo_instrumnetal = pygame.mixer.Sound('sounds/gameplay/pablo_instrumental.wav')
    pablo_instrumnetal.set_volume(0.3)
    shotgun = pygame.mixer.Sound('sounds/gameplay/Shotgun.wav')
    shotgun.set_volume(0.5)
    collision = pygame.mixer.Sound('sounds/gameplay/collision.wav')
    desert = pygame.mixer.Sound('sounds/gameplay/desert.wav')
    desert.set_volume(0.2)
    win = pygame.mixer.Sound('sounds/gameplay/win.wav')
    lose = pygame.mixer.Sound('sounds/gameplay/lose.wav')
    sounds = [
                background_instrumental,
                click,
                walk,
                pick_powerup,
                raygun_sound,
                shotgun_sound,
                pablo_instrumnetal,
                collision,
                collision,
                win,
                lose
    ]

    @classmethod
    def change_volume(cls,volume):
        for i in range(len(Music.sounds)):
            Music.sounds[i].set_volume(volume)