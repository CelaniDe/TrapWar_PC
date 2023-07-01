import pygame
from graph import *

class MenuInGame(pygame.sprite.Sprite):
    def __init__(self,position,win,s):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.win = win
        self.s = s
        self.image = pygame.surface.Surface(self.position)
        self.image.fill((197,223,127))
        self.rect = self.image.get_rect(center=(int(1360/2),int(768/2)))
        self.font = pygame.font.SysFont('Comic Sans MS', 40)
        self.text = self.font.render("MENU",True,(153,20,200))
        self.rect_text = self.text.get_rect(center=(int(1360/2),int(768/2)-200))
        self.return_menu_button = Button(self.rect[0]+120,self.rect[1]+200,60,305,(255,125,100),self.win)
        self.back_button = Button(self.rect[0]+120,self.rect[1]+350,60,150,(255,125,100),self.win)

    def update(self):
        self.win.blit(self.text,(self.rect_text))

        self.return_menu_button.spawn()
        self.return_menu_button.setText("Return To Menu",(0,0,0),40)

        self.back_button.spawn()
        self.back_button.setText("BACK",(0,0,0),40)

        if self.return_menu_button.mouseHover():
            self.return_menu_button.changeColor((0,255,0))
            if pygame.mouse.get_pressed()[0]:
                self.s.close()
                self.kill()
        else:
            self.return_menu_button.changeColor((255,0,0))

        if self.back_button.mouseHover():
            self.back_button.changeColor((0,255,0))
            if pygame.mouse.get_pressed()[0]:
                self.kill()
        else:
            self.back_button.changeColor((255,0,0))
