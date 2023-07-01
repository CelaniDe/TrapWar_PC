import pygame
from abc import ABC , abstractmethod

class PlayerSpawnPoints(ABC):
    image = None
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.position = (self.x,self.y)
        self.hitBox = pygame.Rect(self.x,self.y,110,220)

    def spawn(self,win):
        win.blit(self.__class__.image,(self.x,self.y))

    def collision_test(self,platoforms):
        collisions = list()
        for platoform in platoforms:
            if self.hitBox.colliderect(platoform):
                collisions.append(platoform)
        return collisions

    def move_collide(self,movement,platoforms):
        self.x += movement[0]
        self.hitBox.x += movement[0]
        collisions = self.collision_test(platoforms)
        for platform in collisions:
            if movement[0] > 0:
                self.hitBox.right = platform.left
            if movement[0] < 0:
                self.hitBox.left = platform.right
        self.y += movement[1]
        self.hitBox.y += movement[1]
        collisions = self.collision_test(platoforms)
        for platform in collisions:
            if movement[1] > 0:
                self.hitBox.bottom = platform.top
            if movement[1] < 0:
                self.hitBox.top = platform.bottom

        self.x = self.hitBox[0]
        self.y = self.hitBox[1] 

class Player1(PlayerSpawnPoints):
    image = pygame.image.load('Images/Player/player1.png')

class Player2(PlayerSpawnPoints):
    image = pygame.image.load('Images/Player/player2.png')