import pygame
from ObjectInGame import *
from SwitchButton import *

background_label = pygame.image.load("connect_to_server_images/background_label.png")

start_button_image = pygame.image.load("connect_to_server_images/connect.png")

full_button_image = pygame.image.load("connect_to_server_images/full.png")


class Text(object):
    pygame.font.init()
    def __init__(self,x,y,text,size,win):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont('Century Gothic', size)
        self.text_surface = self.font.render(self.text, False, (255,255,255))
        self.height = self.text_surface.get_rect(center = (self.x,self.y))[3]
        self.width = self.text_surface.get_rect(center = (self.x,self.y))[2]
        self.win = win

    def spawn(self):
        self.win.blit(self.text_surface,(self.text_surface.get_rect(center = (self.x, self.y))))

class Label(object):
    def __init__(self,x,y,objects,space,win):
        self.x = x
        self.y = y
        self.lista_objects = objects

        self.width = 0
        for object_ in objects:
            self.width += object_.width
        
        self.width += space * (len(objects) -1)

        self.height = 0
        for object_ in objects:
            if object_.height > self.height:
                self.height = object_.height


        self.space = space
        self.win = win 

    def spawn(self):

        space = 0
        for object_to_spawn in self.lista_objects:
            object_to_spawn.x = self.x - int(object_to_spawn.width/2) + space
            object_to_spawn.y = self.y - int(object_to_spawn.height/2)
            object_to_spawn.spawn()

            space += object_to_spawn.width + self.space

class ServerLabel(ObjectInGame):
    def __init__(self,x,y,ip,port_tcp,port_udp,players):
        super().__init__(x,y)
        self.ip = Text(0,0,str(ip),30,self.win)
        self.port_tcp = Text(0,0,str(port_tcp),30,self.win)
        self.port_udp = str(port_udp)
        self.players = Text(0,0,str(players),30,self.win)
        self.connect_button = SwitchButton(0,0,start_button_image,full_button_image,None)
        self.background = background_label
        self.height = self.background.get_rect()[3]
        self.width = self.background.get_rect()[2]
        self.status = False

    def setNumberOfPlayers(self,number):
        self.players = Text(0,0,str(number),30,self.win)


    def spawn(self):

        space = 150
        self.win.blit(self.background,(self.x,self.y))

        self.ip.x = self.x + 100
        self.ip.y = self.y + 45
        self.ip.spawn()

        self.port_tcp.x = self.x + 360
        self.port_tcp.y = self.y + 45
        self.port_tcp.spawn()

        self.players.x = self.x + 550
        self.players.y = self.y + 45
        self.players.spawn()

        if self.players.text == "2":
            self.connect_button.status = False
        else:
            self.connect_button.status = True

        self.connect_button.x = self.players.x + self.players.width + space + 125
        self.connect_button.y = self.y + 45 
        self.connect_button.spawn()