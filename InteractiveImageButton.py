import pygame
from ImageButton import *


class InteractiveImageButton(ImageButton):
    def __init__(self,x,y,image,second_image,click_sound):
        super().__init__(x,y,image,click_sound)
        self.initial_image = self.image
        self.second_image = second_image


    def spawn(self):
        self.win.blit(self.image,(self.image.get_rect(center = (self.x,self.y))))

        if self.mouseHover():
            self.image = self.second_image
        else:
            self.image = self.initial_image


