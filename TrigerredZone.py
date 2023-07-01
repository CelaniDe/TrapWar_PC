import pygame
from abc import ABC,abstractclassmethod
from FCommands import *

class TrigerredZone():
    def __init__(self,x,y,width = 100,height = 100,function = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.hitBox = pygame.Rect(x,y,width,height)
        self.obj_collide = None

    def setObjectCollide(self,obj): self.obj_collide = obj    
    
    def applyFunction(self,obj,key):
        if self.function != None and self.obj_collide.collide(self.hitBox):
            self.function.apply(obj,key)

    def spawn(self,win):
        pygame.draw.rect(win,(255,0,0),self.hitBox,1)

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


class TrigerredFunction(ABC):
    
    @abstractclassmethod
    def apply(self,objects,key):
        pass

class DamageZone(TrigerredFunction):
    def apply(self,objects,key):
        obj = objects[0]
        obj.decHealth(1)

class SwitchDelete(TrigerredFunction):
    def apply(self,objects,key):
        obj = objects[0]
        if isinstance(key,Key_E):
            obj.decHealth(10)

class ElevatorUse(TrigerredFunction):
    counter = 0
    def apply(self,objects,key):
        obj = objects[1]
        ElevatorUse.counter += 1
        if isinstance(key,Key_E) and ElevatorUse.counter > 10:
            obj.finish()
            ElevatorUse.counter = 0
        