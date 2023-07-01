import pygame

class Player_model():
    def __init__(self,lista_skins,win):
        pygame.init()
        self.lista_skins = lista_skins
        self.win = win
        self.counter_skin = 0
        self.height = self.lista_skins[0].get_rect()[3]
        self.width = self.lista_skins[0].get_rect()[2]
        self.x = 680 - int(self.width/2)
        self.y = 130

    def mouseHover(self): 
        if (self.x < pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < self.x + self.width) and (pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1]<self.y + self.height):
            return True
        return False

    def plusIndex(self,amount = 1):
        self.counter_skin += amount

    def spawn(self):
        self.win.blit(self.lista_skins[0],(self.x,self.y))

    