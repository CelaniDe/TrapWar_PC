import pygame
from Loading_image import *
from Pickup import *
from Music import *
from StatusWeapon import *

class Player1(Pickup):
    def __init__(self,x,y):
        super().__init__(x,y,100,100)

    def spawn(self):
        pass

    def collide(self):
        pass

    def getHitBox(self):
        pass
    
    def updateHitBox(self):
        pass

    def apply(self,player):
        pass

    def getHeight(self):
        pass

class Player2(Pickup):
    def __init__(self,x,y):
        super().__init__(x,y,100,100)

    def spawn(self):
        pass

    def collide(self):
        pass

    def getHitBox(self):
        pass
    
    def updateHitBox(self):
        pass

    def apply(self,player):
        pass

    def getHeight(self):
        pass



class Player():
    walk_sound = Music.walk
    lista_skins = list()
    lista_skins_weapon = list()
    lista_skins_raygun = list()
    Skins = [lista_skins,lista_skins_weapon,lista_skins_raygun]
    def __init__(self,x,y,name,health,in_list_index,idle_index,walk_index_range,dead_Index):
        self.x = x
        self.y = y
        self.position = pygame.Vector2(self.x,self.y)
        self.name = name
        self.health = health
        self.status = 0
        self.side = 0
        self.superStatus = 0
        self.skin_counter = 0
        self.in_list_index = in_list_index
        self.hitBox = pygame.Rect(self.x,self.y,80,230)
        self.idle_Index = idle_index
        self.dead_Index = dead_Index
        self.AnimStart = False
        self.isJump = False
        self.walk_index_range = walk_index_range
        self.weapon = NoWeapon()
        self.deathAnim = False
        self.death = False
        self.height = 220
        self.width = None
        self.play_walk_sound = False
        self.ammo = 0
        self.gravity_force = 10
        self.jump_counter = 0
        self.inInterpolation = False
        self.skin_counter_to_return = 7

    def __eq__(self,other):
        if isinstance(other, Player):
            if other.x == self.x and other.y == self.y:
                return True
            return False
        raise Exception("PLAYER ERROR")

    def spawn(self,win):
        skin = self.__class__.Skins[self.superStatus][self.status][self.side].get_item(self.skin_counter)
        win.blit(skin,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitBox,1)   

    def updateHitBox(self): 
        try: 
            skin = self.__class__.Skins[self.superStatus][self.status][self.side].get_item(self.skin_counter)
            width , height = skin.get_rect()[2:]
            self.hitBox = pygame.Rect(self.x,self.y,width,height)
        except Exception as e:
            print(f"{e} - > ERROR SKIN COUNTER")
        
    def setJump(self,lista_platforms):
        for platform in lista_platforms:
            if self.hitBox.bottom  == platform.top:
                self.isJump = False


    def toWeapon(self,weapon):
        self.weapon = weapon
        self.skin_counter = 0
        self.superStatus = self.weapon.superstatus
        self.idle_Index = self.Skins[self.superStatus][2][0].get_length()
        self.walk_index_range = self.__class__.Skins[self.superStatus][0][0].get_length()

    def collide(self,rect): return self.hitBox.colliderect(rect)


    def getHitBox(self): return self.hitBox 

    def plusX(self,amount):
        self.x += amount

    def getX(self):
        return self.x

    def getHeight(self):
        return self.height

    def getStatus(self): return self.status
    
    def setStatus(self,status):
        self.status = status

    def setSide(self,side):
        self.side = side

    def getSide(self): return self.side        
    
    def setX(self,x):
        self.x = x

  
    def getY(self):
        return self.y

    def setY(self,y):
        self.y = y

    def plusY(self,n): self.y += n

    def jump(self,platforms):
        """
        lista = range(-force,force,10)
        self.isJump = True
        if(self.isJump):
            self.move_collide((0,lista[self.jump_counter]),[x.getHitBox() for x in platforms]) #self.y += lista[self.jump_counter]
            self.jump_counter += 1
            if self.jump_counter >= len(lista):
                self.isJump = False
                self.jump_counter = 0
        """
        self.move_collide([0,-50],platforms)


    def move(self):
        if(self.status == 0 and not self.AnimStart):
            if(self.skin_counter >= self.walk_index_range-2): 
                self.skin_counter = 7
            self.skin_counter+=1

    def playAnimation(self):
        if self.skin_counter >= self.__class__.Skins[self.superStatus][self.status][0].get_length() - 2:
            self.skin_counter = self.skin_counter_to_return
            self.AnimStart = False
        else:
            self.skin_counter += 1

    def lastSkinNumber(self):
        return self.__class__.Skins[self.superStatus][self.status][0].get_length()

    def collision_test(self,platoforms):
        collisions = list()
        for platoform in platoforms:
            if self.hitBox.colliderect(platoform):
                collisions.append(platoform)
        return collisions

    def move_to(self,vector):
        self.x , self.y = vector.xy
        self.hitBox.x , self.hitBox.y = vector.xy
        self.position = pygame.Vector2(self.x,self.y)

    def move_collide(self,movement,platoforms):
        #self.x += movement[0]
        self.hitBox.x += movement[0]
        collisions = self.collision_test(platoforms)
        for platform in collisions:
            if movement[0] > 0:
                self.hitBox.right = platform.left
            if movement[0] < 0:
                self.hitBox.left = platform.right
        #self.y += movement[1]
        self.hitBox.y += movement[1]
        collisions = self.collision_test(platoforms)
        for platform in collisions:
            if movement[1] > 0:
                self.hitBox.bottom = platform.top
            if movement[1] < 0:
                self.hitBox.top = platform.bottom

        self.x = self.hitBox[0]
        self.y = self.hitBox[1]
        self.position = pygame.Vector2(self.x,self.y)

    """
    def idle(self):
        if(self.status == 2 and not self.AnimStart):
            if(self.skin_counter >= self.idle_Index-2): 
                self.skin_counter = 0
            self.skin_counter+=1
            self.play_walk_sound = False

    def Pjump(self):
        if(self.status == 4):
            self.AnimStart = True
            if(self.skin_counter >= 87):
                self.skin_counter = 0
                self.AnimStart = False
            self.skin_counter += 1

    def death(self):
        if(self.deathAnim == False):
            self.skin_counter = 0
        if(self.status == 1):
            self.deathAnim= True
            if(self.skin_counter >= self.dead_Index):
                self.skin_counter = self.dead_Index-1
            self.skin_counter += 1    
    """

    def plussHealht(self,n): self.health += n

    def getHealth(self): return self.health

    def decHealth(self,n): self.health-=n

    def fire(self):
        return self.weapon.behavior.fire(self.weapon,self.side,self.x,self.y)

    def setupInterpolationValues(self,movements,steps):
        if not self.inInterpolation:
            self.xstart = self.x
            self.xend = self.x + movements
            self.deltax = (self.xend - self.xstart)/steps
            self.inInterpolation = True

    def interpolaite(self):
        if self.inInterpolation:
            if self.deltax > 0:
                if self.x < self.xend:
                    self.x += self.deltax
                else:
                    self.inInterpolation = False
            else:
                if self.x > self.xend:
                    self.x += self.deltax
                else:
                    self.inInterpolation = False

    def returnLista(self):
        return [self.x,self.y,self.health,self.status,self.side,self.skin_counter,self.superStatus,self.hitBox,self.play_walk_sound,self.weapon.getAmmo(),self.in_list_index]

    def update(self,information_for_players):
        self.x = information_for_players[0]
        self.y = information_for_players[1]
        self.health = information_for_players[2]
        self.status = information_for_players[3]
        self.side = information_for_players[4]
        self.skin_counter = information_for_players[5]
        self.superStatus = information_for_players[6]
        self.hitBox = information_for_players[7]
        self.play_walk_sound = information_for_players[8]
        self.weapon.ammo = information_for_players[9]

class SferaEbbasta(Player):
    face = Loader("/characters/sfera_ebbasta/face").get_item(0)
    sfera_ebbastaR = Loader("/characters/sfera_ebbasta/move/right")
    sfera_ebbastaL = Loader("/characters/sfera_ebbasta/move/left")
    sfera_ebbasta_deadR = Loader("/characters/sfera_ebbasta/dead/right")
    sfera_ebbasta_deadL = Loader("/characters/sfera_ebbasta/dead/left")
    sfera_ebbasta_breatheR = Loader("/characters/sfera_ebbasta/breathe/right")
    sfera_ebbasta_breatheL = Loader("/characters/sfera_ebbasta/breathe/left")
    sfera_ebbasta_weaponL = Loader("/characters/sfera_ebbasta/move_weapon/left2")
    sfera_ebbasta_weaponR = Loader("/characters/sfera_ebbasta/move_weapon/right2")
    sfera_ebbasta_breathe_weaponL = Loader("/characters/sfera_ebbasta/breathe_weapon/left")
    sfera_ebbasta_breathe_weaponR = Loader("/characters/sfera_ebbasta/breathe_weapon/right")
    sfera_ebbasta_jump_left = Loader("/characters/sfera_ebbasta/jump/left")
    sfera_ebbasta_jump_right = Loader("/characters/sfera_ebbasta/jump/right")
    sfera_ebbasta_raygunL = Loader("/characters/sfera_ebbasta/walk_raygun/left")
    sfera_ebbasta_raygunR = Loader("/characters/sfera_ebbasta/walk_raygun/right")
    sfera_ebbasta_breathe_raygunL = Loader("/characters/sfera_ebbasta/breathe_raygun/left")
    sfera_ebbasta_breathe_raygunR = Loader("/characters/sfera_ebbasta/breathe_raygun/right")
    sfera_ebbasta_drink_leanL = Loader("/characters/sfera_ebbasta/drink_lean/left")
    sfera_ebbasta_drink_leanR = Loader("/characters/sfera_ebbasta/drink_lean/right")
    sfera_ebbasta_smokeL = Loader("/characters/sfera_ebbasta/smoke/left")
    sfera_ebbasta_smokeR = Loader("/characters/sfera_ebbasta/smoke/right")
    winner = Loader("/characters/sfera_ebbasta/win")
    loser = Loader("/characters/sfera_ebbasta/lose")
    
    lista_skins = [[sfera_ebbastaL,sfera_ebbastaR],[sfera_ebbasta_deadL,sfera_ebbasta_deadR],[sfera_ebbasta_breatheL,sfera_ebbasta_breatheR],[sfera_ebbasta_drink_leanL,sfera_ebbasta_drink_leanR],[sfera_ebbasta_jump_left,sfera_ebbasta_jump_right],[sfera_ebbasta_smokeL,sfera_ebbasta_smokeR]]
    lista_skins_weapon = [[sfera_ebbasta_weaponL,sfera_ebbasta_weaponR],[sfera_ebbasta_deadL,sfera_ebbasta_deadR],[sfera_ebbasta_breathe_weaponL,sfera_ebbasta_breathe_weaponR],[sfera_ebbasta_drink_leanL,sfera_ebbasta_drink_leanR],[sfera_ebbasta_jump_left,sfera_ebbasta_jump_right],[sfera_ebbasta_smokeL,sfera_ebbasta_smokeR]]
    lista_skins_raygun = [[sfera_ebbasta_raygunL,sfera_ebbasta_raygunR],[sfera_ebbasta_deadL,sfera_ebbasta_deadR],[sfera_ebbasta_breathe_raygunL,sfera_ebbasta_breathe_raygunR],[sfera_ebbasta_drink_leanL,sfera_ebbasta_drink_leanR],[sfera_ebbasta_jump_left,sfera_ebbasta_jump_right],[sfera_ebbasta_smokeL,sfera_ebbasta_smokeR]]
    Skins = [lista_skins,lista_skins_weapon,lista_skins_raygun]
    def __init__(self,x,y):
        super().__init__(x,y,"Sfera Ebbasta",146,1,__class__.sfera_ebbasta_breatheL.get_length(),36,47)

class Supreme(Player):
    face = Loader("/characters/supreme/face").get_item(0)#[0]
    supremeL = Loader("/characters/supreme/move/left")
    supremeR = Loader("/characters/supreme/move/right")
    supreme_dead_L = Loader("/characters/supreme/dead/left")
    supreme_dead_R = Loader("/characters/supreme/dead/right")
    supreme_breatheL = Loader("/characters/supreme/breathe/left")
    supreme_breatheR = Loader("/characters/supreme/breathe/right")
    supreme_weaponR = Loader("/characters/supreme/move_weapon/right")
    supreme_weaponL = Loader("/characters/supreme/move_weapon/left")
    supreme_breathe_weaponR = Loader("/characters/supreme/breathe_weapon/right")
    supreme_breathe_weaponL = Loader("/characters/supreme/breathe_weapon/left")
    supreme_raygunL = Loader("/characters/supreme/move_raygun/left")
    supreme_raygunR = Loader("/characters/supreme/move_raygun/right")
    supreme_breathe_raygunL = Loader("/characters/supreme/breathe_raygun/left")
    supreme_breathe_raygunR = Loader("/characters/supreme/breathe_raygun/right")
    supreme_drink_leanL = Loader("/characters/supreme/drink_lean/left")
    supreme_drink_leanR = Loader("/characters/supreme/drink_lean/right")
    supreme_smokeL = Loader("/characters/supreme/smoke/left")
    supreme_smokeR = Loader("/characters/supreme/smoke/right")
    winner = Loader("/characters/supreme/win")
    loser = Loader("/characters/supreme/lose")

    lista_skins = [[supremeL,supremeR],[supreme_dead_L,supreme_dead_R],[supreme_breatheL,supreme_breatheR],[supreme_drink_leanL,supreme_drink_leanR],[],[supreme_smokeL,supreme_smokeR]]
    lista_skins_weapon = [[supreme_weaponL,supreme_weaponR ],[supreme_dead_L,supreme_dead_R],[supreme_breathe_weaponL,supreme_breathe_weaponR],[supreme_drink_leanL,supreme_drink_leanR],[],[supreme_smokeL,supreme_smokeR]]
    lista_skins_raygun = [[supreme_raygunL,supreme_raygunR],[supreme_dead_L,supreme_dead_R],[supreme_breathe_raygunL,supreme_breathe_raygunR],[supreme_drink_leanL,supreme_drink_leanR],[],[supreme_smokeL,supreme_smokeR]]
    Skins = [lista_skins,lista_skins_weapon,lista_skins_raygun]
    def __init__(self,x,y):
        super().__init__(x,y,"Supreme",146,0,__class__.supreme_breatheL.get_length(),36,37)

class TonyEffe(Player):
    face = Loader("/characters/tony_effe/face").get_item(0)#[0]
    tony_effeL = Loader("/characters/tony_effe/move/left") 
    tony_effeR = Loader("/characters/tony_effe/move/right")
    tony_effe_deadL = Loader("/characters/tony_effe/dead/left")
    tony_effe_deadR = Loader("/characters/tony_effe/dead/right")
    tony_effe_breatheR = Loader("/characters/tony_effe/breathe/right")
    tony_effe_breatheL = Loader("/characters/tony_effe/breathe/left")
    tony_effe_jumpL = Loader("/characters/tony_effe/jump/left")
    tony_effe_jumpR = Loader("/characters/tony_effe/jump/right")
    tony_effe_weaponL = Loader("/characters/tony_effe/move_weapon/left")
    tony_effe_weaponR = Loader("/characters/tony_effe/move_weapon/right")
    tony_effe_breathe_weaponL = Loader("/characters/tony_effe/breathe_weapon/left")
    tony_effe_breathe_weaponR = Loader("/characters/tony_effe/breathe_weapon/right")
    tony_effe_raygunL = Loader("/characters/tony_effe/move_raygun/left")
    tony_effe_raygunR = Loader("/characters/tony_effe/move_raygun/right")
    tony_effe_breathe_raygunL = Loader("/characters/tony_effe/breathe_raygun/left")
    tony_effe_breathe_raygunR = Loader("/characters/tony_effe/breathe_raygun/right")
    tony_effe_drink_leanL = Loader("/characters/tony_effe/drink_lean/left")
    tony_effe_drink_leanR = Loader("/characters/tony_effe/drink_lean/right")
    tony_effe_smokeL = Loader("/characters/tony_effe/smoke/left")
    tony_effe_smokeR = Loader("/characters/tony_effe/smoke/right")
    winner = Loader("/characters/tony_effe/win")
    loser = Loader("/characters/tony_effe/lose")

    lista_skins = [[tony_effeL,tony_effeR],[tony_effe_deadL,tony_effe_deadR],[tony_effe_breatheL,tony_effe_breatheR],[tony_effe_drink_leanL,tony_effe_drink_leanR],[tony_effe_jumpL,tony_effe_jumpR],[tony_effe_smokeL,tony_effe_smokeR]]
    lista_skins_weapon = [[tony_effe_weaponL,tony_effe_weaponR ],[tony_effe_deadL,tony_effe_deadR],[tony_effe_breathe_weaponL,tony_effe_breathe_weaponR],[tony_effe_drink_leanL,tony_effe_drink_leanR],[tony_effe_jumpL,tony_effe_jumpR],[tony_effe_smokeL,tony_effe_smokeR]]
    lista_skins_raygun = [[tony_effe_raygunL,tony_effe_raygunR],[tony_effe_deadL,tony_effe_deadR],[tony_effe_breathe_raygunL,tony_effe_breathe_raygunR],[tony_effe_drink_leanL,tony_effe_drink_leanR],[tony_effe_jumpL,tony_effe_jumpR],[tony_effe_smokeL,tony_effe_smokeR]]
    Skins = [lista_skins,lista_skins_weapon,lista_skins_raygun]
    def __init__(self,x,y):
        super().__init__(x,y,"Tony Effe",146,2,__class__.tony_effe_breatheL.get_length(),36,39)


class Fedez(Player):
    face = Loader("/characters/fedez/face").get_item(0)#[0]
    fedezL = Loader("/characters/fedez/move/left")
    fedezR = Loader("/characters/fedez/move/right")
    fedezDeadL = Loader("/characters/fedez/death/left")
    fedezDeadR = Loader("/characters/fedez/death/right")
    fedez_breatheL = Loader("/characters/fedez/breathe/left")
    fedez_breatheR = Loader("/characters/fedez/breathe/right")
    fedez_weapon_breatheL = Loader("/characters/fedez/breathe_weapon/left")
    fedez_weapon_breatheR = Loader("/characters/fedez/breathe_weapon/right")
    fedez_galaxyL = Loader("/characters/fedez/move_galaxy/left")
    fedez_galaxyR = Loader("/characters/fedez/move_galaxy/right")
    fedez_raygunL = Loader("/characters/fedez/move_raygun/left")
    fedez_raygunR = Loader("/characters/fedez/move_raygun/right")
    fedez_breathe_raygunL = Loader("/characters/fedez/breathe_raygun/left")
    fedez_breathe_raygunR = Loader("/characters/fedez/breathe_raygun/right")
    fedez_drink_leanL = Loader("/characters/fedez/drink_lean/left")
    fedez_drink_leanR = Loader("/characters/fedez/drink_lean/right")
    fedez_smokeL = Loader("/characters/fedez/smoke/left")
    fedez_smokeR = Loader("/characters/fedez/smoke/right")
    winner = Loader("/characters/fedez/win")
    loser = Loader("/characters/fedez/lose")

    lista_skins = [[fedezL,fedezR],[fedezDeadL,fedezDeadR],[fedez_breatheL,fedez_breatheR],[fedez_drink_leanL,fedez_drink_leanR],[],[fedez_smokeL,fedez_smokeR]]
    lista_skins_weapon = [[fedez_galaxyL,fedez_galaxyR],[fedezDeadL,fedezDeadR],[fedez_weapon_breatheL,fedez_weapon_breatheR],[fedez_drink_leanL,fedez_drink_leanR],[],[fedez_smokeL,fedez_smokeR]]
    lista_skins_raygun = [[fedez_raygunL,fedez_raygunR],[fedezDeadL,fedezDeadR],[fedez_breathe_raygunL,fedez_breathe_raygunR],[fedez_drink_leanL,fedez_drink_leanR],[],[fedez_smokeL,fedez_smokeR]]
    Skins = [lista_skins,lista_skins_weapon,lista_skins_raygun]
    def __init__(self,x,y):
        super().__init__(x,y,"Fedez",146,3,__class__.fedez_breatheL.get_length(),__class__.fedezR.get_length(),40)

class SocialBoom(Player):
    
    face = Loader("/characters/social_boom/face").get_item(0)
    social_boomL = Loader("/characters/social_boom/walk/left")
    social_boomR = Loader("/characters/social_boom/walk/right")
    social_boom_deadL = Loader("/characters/social_boom/death/left")
    social_boom_deadR = Loader("/characters/social_boom/death/right")
    social_boom_breatheL = Loader("/characters/social_boom/breathe/left")
    social_boom_breatheR = Loader("/characters/social_boom/breathe/right")
    social_boom_shotgunL = Loader("/characters/social_boom/walk_shotgun/left")
    social_boom_shotgunR = Loader("/characters/social_boom/walk_shotgun/right")
    social_boom_breathe_shotgunL = Loader("/characters/social_boom/breathe_shotgun/left")
    social_boom_breathe_shotgunR = Loader("/characters/social_boom/breathe_shotgun/right")
    social_boom_raygunL = Loader("/characters/social_boom/walk_raygun/left")
    social_boom_raygunR = Loader("/characters/social_boom/walk_raygun/right")
    social_boom_breathe_raygunL = Loader("/characters/social_boom/breathe_raygun/left")
    social_boom_breathe_raygunR = Loader("/characters/social_boom/breathe_raygun/right")
    social_boom_drink_leanL = Loader("/characters/social_boom/drink_lean/left")
    social_boom_drink_leanR = Loader("/characters/social_boom/drink_lean/right")
    social_boom_smokeL = Loader("/characters/social_boom/smoke/left")
    social_boom_smokeR = Loader("/characters/social_boom/smoke/right")
    winner = Loader("/characters/social_boom/win")
    loser = Loader("/characters/social_boom/lose")
    

    lista_skins = [[social_boomL,social_boomR],[social_boom_deadL,social_boom_deadR],[social_boom_breatheL,social_boom_breatheR],[social_boom_drink_leanL,social_boom_drink_leanR],[],[social_boom_smokeL,social_boom_smokeR]]
    lista_skins_weapon = [[social_boom_shotgunL,social_boom_shotgunR],[social_boom_deadL,social_boom_deadR],[social_boom_breathe_shotgunL,social_boom_breathe_shotgunR],[social_boom_drink_leanL,social_boom_drink_leanR],[],[social_boom_smokeL,social_boom_smokeR]]
    lista_skins_raygun = [[social_boom_raygunL,social_boom_raygunR],[social_boom_deadL,social_boom_deadR],[social_boom_breathe_raygunL,social_boom_breathe_raygunR],[social_boom_drink_leanL,social_boom_drink_leanR],[],[social_boom_smokeL,social_boom_smokeR]]
    Skins = [lista_skins,lista_skins_weapon,lista_skins_raygun]
    def __init__(self,x,y):
        super().__init__(x,y,"Social Boom",146,4,__class__.social_boom_breatheL.get_length(),__class__.social_boomL.get_length(),__class__.social_boom_deadL.get_length())

