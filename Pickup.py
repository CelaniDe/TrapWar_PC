from abc import ABC,abstractclassmethod
from ObjectInGame import *
import pygame
from function import *
from StatusWeapon import *
from Bullet import *
from message import Health , DrinkLean

class Pickup(ObjectInGame):
    image = None 
    def __init__(self,x,y):
        super().__init__(x,y)
        self.width = self.__class__.image[0].get_rect()[2]
        self.height = self.__class__.image[0].get_rect()[3]
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.kernel = pygame.Rect(0,0,0,0)
        self.isRespwnable = False
        self.gravity_force = 8
        self.time_picked = 0
        self.time_to_spawn = 5
        self.skinCounter = 0
        self.hasEffect = False
        self.hasDisabble = False

    def animation(self):
        if self.skinCounter >= len(self.__class__.image) - 2:
            self.skinCounter = 0
        else:
            self.skinCounter += 1
    
    def spawn(self,win):
        win.blit(self.__class__.image[self.skinCounter],(self.x,self.y))
        #pygame.draw.rect(win , (255,0,0), self.hitBox, 2)

    
    def collide(self,rect):
        return self.hitBox.colliderect(rect)


    @abstractclassmethod
    def apply(self,player):
        pass

    def __eq__(self, other):
        if not isinstance(other , Pickup):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    

    def getHitBox(self): return self.hitBox

    def updateHitBox(self): self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height) 

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


class PurpleDrank(Pickup):
    image = ricevi_foto("/pickup/PurpleDrank")
    def __init__(self,x,y):
        pygame.init()
        super().__init__(x, y)
        self.isRespwnable = True
        self.hasEffect = True
        self.effect = DrinkLean
        self.time_to_spawn = 10
        self.hasDisabble = True

    def apply(self, player):
        self.player = player
        self.player.gravity_force = 2    
        self.player.skin_counter = 0
        self.player.setStatus(3)
        self.player.AnimStart = True

    def disApplay(self):
        self.player.gravity_force = 10
  

class ShotGun(Pickup):
    image = ricevi_foto("/pickup/ShotGun")
    def __init__(self,x,y):
        pygame.init()
        super().__init__(x, y)
        self.weapon = StatusShotgun(5,BulletShotgun(),1)

    def apply(self,player):
        player.toWeapon(self.weapon) 


class RayGun(Pickup):
    image = ricevi_foto("/pickup/RayGun")
    def __init__(self,x,y):
        pygame.init()
        super().__init__(x, y)
        self.weapon = StatusRaygun(5,BulletRaygun(),2)

    def apply(self,player):
        player.toWeapon(self.weapon)  

class Ammo(Pickup):
    image = ricevi_foto("/pickup/Ammo")
    def __init__(self,x,y):
        pygame.init()
        super().__init__(x, y)
        self.isRespwnable = True
        self.time_to_spawn = 2

    def apply(self,player):
        player.weapon.ammo += 10 

class Weed(Pickup):
    image = ricevi_foto("/pickup/weed")
    def __init__(self,x,y):
        pygame.init()
        super().__init__(x, y)
        self.isRespwnable = True
        self.hasEffect = True
        self.effect = Health

    def apply(self,player):
        player.plussHealht(30)
        if player.getHealth() > 150:
            player.health = 150
        player.skin_counter = 0
        player.setStatus(5)
        player.AnimStart = True
