from Bullet import *
from BehaviorWeapon import *
from abc import ABC , abstractclassmethod
from Music import Music

class StatusWeapon(ABC):
    def __init__(self,ammo,bullet,superstatus,behavior):
        self.ammo = ammo
        self.bullet = bullet
        self.superstatus = superstatus
        self.behavior = behavior
    def getAmmo(self): return self.ammo
    def decAmmo(self , amount = 1): self.ammo -= amount

    @abstractclassmethod
    def getBullet(self):
        pass

class StatusShotgun(StatusWeapon):
    sound = Music.shotgun
    def __init__(self,ammo,bullet,superstatus):
        super().__init__(ammo,bullet,superstatus,BehaviorShotgun())

    def getBullet(self): return BulletShotgun()

class StatusRaygun(StatusWeapon):
    sound = Music.raygun_sound
    def __init__(self,ammo,bullet,superstatus):
        super().__init__(ammo,bullet,superstatus,BehaviorOneBullet())

    def getBullet(self): return BulletRaygun()


class NoWeapon(StatusWeapon):
    sound = None
    def __init__(self):
        super().__init__(0,None,0,None)

    def getBullet(self): return None