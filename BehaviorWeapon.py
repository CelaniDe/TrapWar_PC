from abc import ABC , abstractclassmethod

class BehaviorWeapon(ABC):
    @abstractclassmethod
    def fire(self,weapon,side,x,y):
        pass

class BehaviorOneBullet(BehaviorWeapon):

    def fire(self,weapon,side,x,y):
        bullet = weapon.getBullet()
        if side == 1:
            bullet.x  = x+210
            bullet.y =  y+80
            bullet.setSide(1)
            bullet.movements = [bullet.velocity,0]
        else:
            bullet.x  = x-110
            bullet.y =  y+80
            bullet.setSide(0)  
            bullet.movements = [-bullet.velocity,0]

        return [bullet]

class BehaviorShotgun(BehaviorWeapon):

    def fire(self,weapon,side,x,y):
        lista_bullets = [weapon.getBullet(),weapon.getBullet(),weapon.getBullet()]
        velocity = lista_bullets[0].velocity
        movements = [[[-velocity,-velocity],[-velocity,0],[-velocity,velocity]],
                    [[velocity,velocity],[velocity,0],[velocity,-velocity]]]
        
        for ID_ in range(len(lista_bullets)):
            if side == 1:
                lista_bullets[ID_].x = x + 210
                lista_bullets[ID_].y = y + 80
                lista_bullets[ID_].setSide(1)
                lista_bullets[ID_].movements = movements[1][ID_]
            else:
                lista_bullets[ID_].x = x - 110
                lista_bullets[ID_].y = y + 80
                lista_bullets[ID_].setSide(0)
                lista_bullets[ID_].movements = movements[0][ID_]

        return lista_bullets