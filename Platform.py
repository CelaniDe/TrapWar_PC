import pygame
from ObjectInGame import ObjectInGame

class Platform(ObjectInGame):

    def __init__(self,x,y,image):
        pygame.init()
        super().__init__(x,y)
        self.width = image.get_rect()[2]
        self.height = image.get_rect()[3]
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.kernel = pygame.Rect(self.hitBox.centerx,self.hitBox.centery,int(self.width*0.7),int(self.height*0.7))
        self.kernel.center = self.hitBox.center
        self.isDestroyable = False

        
    def getHitBox(self): return self.hitBox


    def collide(self,rect):
        return self.hitBox.colliderect(rect)    

    def collideKernel(self,rect):
        return self.kernel.colliderect(rect)                


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
        self.kernel = pygame.Rect(self.hitBox.centerx,self.hitBox.centery,int(self.width*0.7),int(self.height*0.7))
        self.kernel.center = self.hitBox.center


class Brick(Platform):
    image = pygame.image.load("texture/brick.png")
    def __init__(self,x,y):
        super().__init__(x,y,Brick.image)

    def spawn(self,win):
        win.blit(Brick.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)

class BlueBrick(Platform):
    image = pygame.image.load("platform/blue_brick.png")
    def __init__(self,x,y):
        super().__init__(x,y,BlueBrick.image)

    def spawn(self,win):
        win.blit(BlueBrick.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)


class Box(Platform):
    image = pygame.image.load('platform/platform4.png')
    def __init__(self,x,y):
        super().__init__(x,y,Box.image)

    def spawn(self,win):
        win.blit(Box.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)


class TwoBox(Platform):
    image = pygame.image.load('platform/platform5.png')
    def __init__(self,x,y):
        super().__init__(x,y,TwoBox.image)

    def spawn(self,win):
        win.blit(TwoBox.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)

class DamageBox(Platform):
    image = pygame.image.load('platform/platform2.png')
    def __init__(self,x,y):
        super().__init__(x,y,DamageBox.image)

    def spawn(self,win):
        win.blit(DamageBox.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)

class FourBox(Platform):
    image = pygame.image.load('platform/platform1.png')
    def __init__(self,x,y):
        super().__init__(x,y,FourBox.image)

    def spawn(self,win):
        win.blit(FourBox.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)

class ColonLava(Platform):
    image = pygame.image.load('platform/colon_lava.png')
    def __init__(self,x,y):
        super().__init__(x,y,ColonLava.image)

    def spawn(self,win):
        win.blit(ColonLava.image,(self.x,self.y))
        #pygame.draw.rect(self.win,(255,0,0),self.hitBox,1)

class Cake(Platform):
    image = pygame.image.load('platform/cake.png')
    def __init__(self,x,y):
        super().__init__(x,y,Cake.image)

    def spawn(self,win):
        win.blit(Cake.image,(self.x,self.y))

class Cactus(Platform):
    image = pygame.image.load('platform/cactus.png')
    def __init__(self,x,y):
        super().__init__(x,y,Cactus.image)

    def spawn(self,win):
        win.blit(Cactus.image,(self.x,self.y))

class Cheese(Platform):
    image = pygame.image.load('platform/cheese.png')
    def __init__(self,x,y):
        super().__init__(x,y,Cheese.image)

    def spawn(self,win):
        win.blit(Cheese.image,(self.x,self.y))

class Crate(Platform):
    image = pygame.image.load('platform/crate.png')
    def __init__(self,x,y):
        super().__init__(x,y,Crate.image)
        self.isDestroyable = True

    def spawn(self,win):
        win.blit(Crate.image,(self.x,self.y))


class StoneBlock(Platform):
    image = pygame.image.load('platform/stoneBlock.png')
    def __init__(self,x,y):
        super().__init__(x,y,StoneBlock.image)

    def spawn(self,win):
        win.blit(StoneBlock.image,(self.x,self.y))


class Elevator(Platform):
    image = pygame.image.load("platform/elevator.png")

    def __init__(self,x,y,velocity,Range):
        self.velocity = velocity
        self.start_point = y
        self.end_point = y+Range
        self.flag = False
        self.begin = True
        super().__init__(x,y,Elevator.image)

    def spawn(self,win):
        win.blit(Elevator.image,(self.x,self.y))
    
    def start(self):
        if self.begin:
            if self.x <= self.end_point and not self.flag:
                self.x += self.velocity
            if self.x >= self.end_point:
                self.flag = True
            if self.flag:
                self.x -= self.velocity
            if self.x <= self.start_point and self.flag:
                self.flag = False

    def finish(self):
        self.begin = not self.begin
    
    def updateHitBox(self):
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)

class GhostPlatform():
    image = None
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width , self.height  = self.__class__.image.get_rect()[2:]
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.kernel = pygame.Rect(0,0,0,0)

    def getHitBox(self): return self.hitBox

    def spawn(self,win): win.blit(self.__class__.image,(self.x,self.y))

class Lava(GhostPlatform):
    image = pygame.image.load('platform/platform3.png')

class Switcher(GhostPlatform):
    image = pygame.image.load('platform/switcher1.png')