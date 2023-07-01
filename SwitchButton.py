import pygame
from InteractiveImageButton import *
import time
from Music import *

class SwitchButton(InteractiveImageButton):
    def __init__(self,x,y,image,second_image,click_sound):
        super().__init__(x,y,image,second_image,click_sound)
        self.status = False

    def spawn(self):
        
        if self.status:
            self.image = self.initial_image
        else:
            self.image = self.second_image

        self.win.blit(self.image,(self.image.get_rect(center = (self.x,self.y))))
        

    def switch(self):
        self.status = not self.status

    def clicked(self):
        if self.mouseHover() and pygame.mouse.get_pressed()[0]:
            self.switch()
            if self.click_sound != None:
                self.click_sound.play()
            time.sleep(0.2)
            return True
        return False
