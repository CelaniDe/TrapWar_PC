import pygame
#from Loading_image import *
from ObjectInGame import *
from function import ricevi_foto

class Background(ObjectInGame):
    def __init__(self,name):
        super().__init__(0,0)
        self.counter = 0
        self.map = ricevi_foto(f"/MovedMaps/{name}") #Loader(f"/MovedMaps/{name}")

    def spawn(self,win):
        win.blit(self.map[self.counter],(self.x,self.y)) #win.blit(self.map.get_item(self.counter),(self.x,self.y))
        self.counter += 1
        if self.counter >= len(self.map):
            self.counter = 0
        
