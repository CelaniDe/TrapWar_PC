import pygame

class Button():
    def __init__(self,x,y,height,width,color,win):
        pygame.init()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = (255,0,0)   
        self.win = win     
        self.clicked = False

    def plusWidth(self,amount):
        self.width += amount

    def changeWidth(self,width):
        self.width = width

    def changeColor(self,color):
        self.color = color

    def mouseHover(self): 
        if (self.x < pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] < self.x + self.width) and (pygame.mouse.get_pos()[1] > self.y and pygame.mouse.get_pos()[1]<self.y + self.height):
            return True
        return False

    def setText(self,text,color,size):
        pygame.font.init()
        f = pygame.font.SysFont('Comic Sans MS', size)
        txt = f.render(text,True,color)   
        self.win.blit(txt,(self.x,self.y))

    def spawn(self):
        pygame.draw.rect(self.win,self.color,(self.x,self.y,self.width,self.height))

class ButtonConnect(Button):
    def __init__(self,x,y,IP,PORT_TCP,PORT_UDP,win):
        self.IP = IP
        self.PORT_TCP = PORT_TCP
        self.PORT_UDP = PORT_UDP
        super().__init__(x,y,90,190,(255,0,0),win)

    def getIP(self):
        return self.IP

    def getPort(self):
        return self.PORT_TCP

class ServerLabel:
    def __init__(self,x,y,ip,port_tcp,port_udp,players,win):
        self.x = x
        self.y = y
        self.ip = ip
        self.port_tcp = port_tcp
        self.port_udp = port_udp
        self.players = players
        self.status = True
        self.win = win

        pygame.font.init()
        font_comic_sans = pygame.font.SysFont('Comic Sans MS', 40)
        self.ip_label = font_comic_sans.render(str(self.ip),True,(0,0,0))
        self.port_label = font_comic_sans.render(str(self.port_tcp),True,(0,0,0))
        self.players_label = font_comic_sans.render(str(self.players),True,(0,0,0))

        space = self.ip_label.get_rect()[2] + self.port_label.get_rect()[2] + 500
        self.Button = ButtonConnect(self.x+space,self.y,str(self.ip),str(self.port_tcp),str(self.port_udp),win)

    def spawn(self):
        self.win.blit(self.ip_label,(self.x,self.y))
        space = self.ip_label.get_rect()[2] + 140
        self.win.blit(self.port_label,(self.x+space,self.y))
        space = self.ip_label.get_rect()[2] + self.port_label.get_rect()[2] + 365
        self.win.blit(self.players_label,(self.x+space,self.y))


