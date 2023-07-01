import pygame
from function import *
from ObjectInGame import *
from Music import *

class Bullet(ObjectInGame):
    def __init__(self,width,height,v,r,damage,can_destroy_brick):
        self.x = 0
        self.y = 0
        self.velocity = v
        self.Range = r
        self.width = width
        self.height = height
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.Spawn = False
        self.side = 0
        self.ID = -1
        self.damage = damage
        self.can_destroy_brick = can_destroy_brick
        self.movements = [0,0]

    def setX(self,x): self.x = x
    def setY(self,y): self.y = y
    def getX(self): return self.x
    def getY(self): return self.y
    def getVelocity(self): return self.velocity
    def getRange(self): return self.Range
    def setRange(self,ran): self.Range = ran 
    def getHitBox(self): return self.hitBox
    def updateHitBox(self): self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
    def collide(self,rect): return self.hitBox.colliderect(rect)
    def setSide(self,s): self.side = s
    def getSide(self): return self.side
    def setId(self,ID): self.ID = ID
    def getId(self): return self.ID
    def getDamage(self): return self.damage

    def decRange(self,n): self.Range -= 1

    def isSpawn(self): return self.Spawn
    def setSpawn(self,sp): self.Spawn = sp

    def move(self):
        self.x += self.movements[0]
        self.y += self.movements[1]


class BulletShotgun(Bullet):
    sound =  Music.shotgun_sound
    skin_bullet = ricevi_foto("/bullets/shotgun")
    def __init__(self):
        width = BulletShotgun.skin_bullet[0].get_rect()[2]
        height = BulletShotgun.skin_bullet[0].get_rect()[3]
        velocity = 10
        range_bullet = 30  
        damage = 5
        can_destroy_brick = False
        super().__init__(width,height,velocity,range_bullet,damage,can_destroy_brick)

    def spawn(self):
        self.Spawn = True 
        self.win.blit(BulletShotgun.skin_bullet[self.side],(self.x,self.y))

class BulletRaygun(Bullet):
    sound = Music.raygun_sound
    skin_bullet = ricevi_foto("/bullets/raygun")
    def __init__(self):
        width = BulletRaygun.skin_bullet[0].get_rect()[2]
        height = BulletRaygun.skin_bullet[0].get_rect()[3]
        velocity = 10
        range_bullet = 50  
        damage = 10
        can_destroy_brick = True
        super().__init__(width,height,velocity,range_bullet,damage,can_destroy_brick)

    def spawn(self):
        self.Spawn = True 
        self.win.blit(BulletRaygun.skin_bullet[self.side],(self.x,self.y))