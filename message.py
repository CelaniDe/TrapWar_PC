import pygame
from ImageButton import *
import webbrowser
import pickle
from FCommands import Exit
from LifeBar import Image
from Loading_image import Loader


class EndGame(pygame.sprite.Sprite):
    image_bb = pygame.image.load("exit_button/000.png")
    def __init__(self,pos,win,s):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.s = s
        self.returnn_button = ImageButton(pos[0],pos[1],EndGame.image_bb,None)
        self.image = pygame.surface.Surface(pos)
        self.image.fill((197,223,127))
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):
        self.returnn_button.spawn()

        if self.returnn_button.clicked():
            self.kill()
            self.s.close()

class WaitPlayerMessage(pygame.sprite.Sprite):
    image_ = pygame.image.load("messages/wait_player.png")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.image = self.__class__.image_
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):
        pass



class Blood(pygame.sprite.Sprite):
    lista_images = Loader("/effects/blood")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.skin_counter = 0
        self.pos = pos
        self.win = win
        self.image = self.__class__.lista_images.get_item(self.skin_counter)
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):
        if self.skin_counter >= self.__class__.lista_images.get_length() - 1:
            self.kill()
        else:
            self.skin_counter += 1
            self.image = self.__class__.lista_images.get_item(self.skin_counter)
            self.rect = self.image.get_rect(center=self.pos)


class Hit(pygame.sprite.Sprite):
    lista_images = Loader("/effects/hit")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.skin_counter = 0
        self.pos = pos
        self.win = win
        self.image = self.__class__.lista_images.get_item(self.skin_counter)
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):
        if self.skin_counter >= self.__class__.lista_images.get_length() - 1:
            self.kill()
        else:
            self.skin_counter += 1
            self.image = self.__class__.lista_images.get_item(self.skin_counter)
            self.rect = self.image.get_rect(center=self.pos)


class Health(pygame.sprite.Sprite):
    lista_images = Loader("/effects/health")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.skin_counter = 0
        self.pos = pos
        self.win = win
        self.image = self.__class__.lista_images.get_item(self.skin_counter)
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):
        if self.skin_counter >= self.__class__.lista_images.get_length() - 1:
            self.kill()
        else:
            self.skin_counter += 1
            self.image = self.__class__.lista_images.get_item(self.skin_counter)
            self.rect = self.image.get_rect(center=self.pos)


class DrinkLean(pygame.sprite.Sprite):
    lista_images = Loader("/effects/drink_lean")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.skin_counter = 0
        self.pos = pos
        self.win = win
        self.image = self.__class__.lista_images.get_item(self.skin_counter)
        self.rect = self.image.get_rect(bottom = pos[1])
        self.display = True

    def update(self):
        if self.skin_counter >= self.__class__.lista_images.get_length() - 1:
            self.kill()
        else:
            self.skin_counter += 1
            self.image = self.__class__.lista_images.get_item(self.skin_counter)
            self.rect = self.image.get_rect(center=self.pos)

class MenuInGamee(pygame.sprite.Sprite):
    image_bb = pygame.image.load("messages/resume_button.png")
    image_exit = pygame.image.load("messages/exit_button.png")
    image_x = pygame.image.load("messages/x_button.png")
    def __init__(self,pos,win,z,server_address):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.z = z
        self.server_address = server_address
        self.continue_button = ImageButton(pos[0],pos[1]-50,MenuInGamee.image_bb,None)
        self.exit_button = ImageButton(pos[0],pos[1]+50,MenuInGamee.image_exit,None)
        self.x_button = ImageButton(pos[0]+116,pos[1]-134,MenuInGamee.image_x,None)
        self.image = pygame.image.load("messages/menu_background.png") 
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):

        self.continue_button.spawn()

        if self.continue_button.clicked():
            self.kill()

        self.exit_button.spawn()

        if self.exit_button.clicked():
            self.z.sendto(pickle.dumps(Exit()),self.server_address)
            self.kill()

        self.x_button.spawn()

        if self.x_button.clicked():
            self.kill()

class OtherPlayerOut(pygame.sprite.Sprite):
    image_bb = pygame.image.load("messages/player_off_button.png")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.returnn_button = ImageButton(pos[0],pos[1]+100,OtherPlayerOut.image_bb,None)
        self.image = pygame.image.load("messages/player_off_background.png") 
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):

        self.returnn_button.spawn()

        if self.returnn_button.clicked():
            self.kill()


class WinGame(pygame.sprite.Sprite):
    image_bb = pygame.image.load("messages/victory_button.png")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.returnn_button = ImageButton(pos[0],pos[1]+100,WinGame.image_bb,None)
        self.image = pygame.image.load("messages/victory_background.png") 
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):

        self.returnn_button.spawn()

        if self.returnn_button.clicked():
            self.kill()

class LoseGame(pygame.sprite.Sprite):
    image_bb = pygame.image.load("messages/lose_button.png")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.returnn_button = ImageButton(pos[0],pos[1]+85,LoseGame.image_bb,None)
        self.image = pygame.image.load("messages/lose_background.png")
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):
        self.returnn_button.spawn()

        if self.returnn_button.clicked():
            self.kill()

class ConnectionErrorr(pygame.sprite.Sprite):
    image_bb = pygame.image.load("messages/player_off_button.png")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.returnn_button = ImageButton(pos[0],pos[1]+80,OtherPlayerOut.image_bb,None)
        self.image = pygame.image.load("messages/connErrorBackground.png") 
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):

        self.returnn_button.spawn()

        if self.returnn_button.clicked():
            self.kill()


class UpdateMessage(pygame.sprite.Sprite):
    image_bb = pygame.image.load("messages/update_button.png")
    def __init__(self,pos,win):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.win = win
        self.returnn_button = ImageButton(pos[0],pos[1]+80,UpdateMessage.image_bb,None)
        self.image = pygame.image.load("messages/update_background.png") 
        self.rect = self.image.get_rect(center=pos)
        self.display = True

    def update(self):

        self.returnn_button.spawn()

        if self.returnn_button.clicked():
            webbrowser.open("https://google.com")
            self.kill()