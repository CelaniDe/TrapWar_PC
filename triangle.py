import pygame

class ImageButton():
    def __init__(self,x,y,image,win):
        pygame.init()
        self.x = x
        self.y = y
        self.image = image
        self.win = win
        self.height = self.image.get_rect()[3]
        self.width = self.image.get_rect()[2]

    def mouseHover(self): 
        if (self.x < pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < self.x + abs(self.width)) and (pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1]<self.y + self.height):
            return True
        return False

    def spawn(self):
        self.win.blit(self.image,(self.x,self.y))