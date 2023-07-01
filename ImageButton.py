import pygame
from ObjectInGame import *
from time import *
#from Music import *


class ImageButton(ObjectInGame):
    def __init__(self,x,y,image,click_sound):
        super().__init__(x,y)
        self.image = image
        self.width = image.get_size()[0]
        self.height = image.get_size()[1]
        self.click_sound = click_sound
        self.is_clicked = False

    def spawn(self):
        self.win.blit(self.image,(self.image.get_rect(center = (self.x,self.y))))


    def mouseHover(self): 
        if self.image.get_rect(center = (self.x,self.y)).collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
            return True
        return False

    def clicked(self):
        if not pygame.mouse.get_pressed()[0] and self.mouseHover():
            self.is_clicked = False

        if self.mouseHover() and pygame.mouse.get_pressed()[0] and not self.is_clicked:
            self.is_clicked = not self.is_clicked
            if self.click_sound != None:
                self.click_sound.play()
            return True
        return False