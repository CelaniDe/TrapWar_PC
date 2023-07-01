import pygame
from labels import Text
from ObjectInGame import *

class Rectangle(ObjectInGame):
	def __init__(self,x,y,height,width,color):
		super().__init__(x,y)
		self.width = width
		self.height = height
		self.height = height
		self.color = color
		
	def spawn(self):
		pygame.draw.rect(self.win,self.color,(self.x,self.y,self.width,self.height))
		
class Circle(ObjectInGame):
	def __init__(self,x,y,radius,color):
		super().__init__(x,y)
		self.radius = radius
		self.color = color
		
	def spawn(self):
		pygame.draw.circle(self.win,self.color,(self.x,self.y),self.radius)


class ProgressBar(ObjectInGame):
	def __init__(self,x,y,width,height,bar_color):
		super().__init__(x,y)
		self.width = width
		self.height =height
		self.bar_color = bar_color
		self.bar = Rectangle(self.x,self.y,self.height,self.width,self.bar_color)
		self.left_circle = Circle(self.x,self.y+int(self.height/2),int(self.height/2),self.bar_color)
		self.right_circle = Circle(self.x+int(self.width),self.y+int(self.height/2),int(self.height/2),self.bar_color) #Circle(self.x+self.width,self.y+int(self.height/4),int(self.height/2),self.bar_color)
		self.lista_shapes = [self.bar,self.left_circle,self.right_circle]

	def update(self):
		self.bar = Rectangle(self.x,self.y,self.height,self.width,self.bar_color)
		self.left_circle = Circle(self.x,self.y+int(self.height/2),int(self.height/2),self.bar_color)
		self.right_circle = Circle(self.x+int(self.width),self.y+int(self.height/2),int(self.height/2),self.bar_color) 
		self.lista_shapes = [self.bar,self.left_circle,self.right_circle]

	def spawn(self):
		self.update()

		for shape in self.lista_shapes:
			shape.spawn()


class LifeBar(ProgressBar):
	def __init__(self,x,y,player_name,player_image,bullets):
		super().__init__(x,y,146,20,[0,255,0])
		self.max_width = 146
		self.life = 146
		self.player_name_text = player_name
		self.player_image_png = player_image
		self.bullets_text = bullets
		self.player_name = Text(self.x+65,self.y-19,str(self.player_name_text),20,self.win)
		self.label_background = Image(self.x-125,self.y-32,pygame.image.load("HUD/label_background.png"))
		self.bullets = Text(self.x+130,self.y+34,str(self.bullets_text),15,self.win)
		self.face_circle = Image(self.x-100,self.y-28,pygame.image.load("HUD/face_circle.png"))
		self.player_image = Image(self.x-90,self.y-20,self.player_image_png)
		self.bar_background = Image(self.x-16,self.y-5,pygame.image.load("HUD/bar_background.png"))

		self.hitBox = pygame.Rect(self.x-125,self.y-32,self.label_background.width,self.label_background.height)

	def update_colors(self):
		self.bar_color[1] = int((255*self.width)/self.max_width)
		self.bar_color[0] = 255 - self.bar_color[1]

	def set_player_name(self,name):
		self.player_name_text = name
		self.player_name = Text(self.x+65,self.y-19,str(self.player_name_text),20,self.win)

	def set_player_image(self,image):
		self.player_image_png = image
		self.player_image = Image(self.x-90,self.y-20,self.player_image_png)

	def setLife(self,life):
		self.width = life

		if self.width >= self.max_width:
			self.width = self.max_width

		if self.width <= 0:
			self.width = 0

	def setBullets(self,bullets):
		self.bullets = Text(self.x+130,self.y+34,str(bullets),15,self.win)

	def plus_life(self,value):
		self.width += value
		if self.width >= self.max_width:
			self.width = self.max_width

	def min_life(self,value):
		self.width -= value
		if self.width <= 0:
			self.width = 0

	def move(self,movement):
		self.x += movement[0]
		self.y += movement[1]
		self.player_name = Text(self.x+65,self.y-19,str(self.player_name_text),20,self.win)
		self.label_background = Image(self.x-125,self.y-32,pygame.image.load("HUD/label_background.png"))
		self.bullets = Text(self.x+130,self.y+34,str(self.bullets_text),15,self.win)
		self.face_circle = Image(self.x-100,self.y-28,pygame.image.load("HUD/face_circle.png"))
		self.player_image = Image(self.x-90,self.y-20,self.player_image_png)
		self.bar_background = Image(self.x-16,self.y-5,pygame.image.load("HUD/bar_background.png"))

		self.hitBox = pygame.Rect(self.x-125,self.y-32,self.label_background.width,self.label_background.height)


	def spawn(self):
		self.label_background.spawn(center=False)
		self.bullets.spawn()
		self.face_circle.spawn(center=False)
		self.player_image.spawn(center=False)
		self.bar_background.spawn(center=False)
		self.player_name.spawn()
		self.update_colors()
		super().spawn()	
		#pygame.draw.rect(self.win , (255,0,50),self.hitBox , 2)

class Image(ObjectInGame):
	def __init__(self,x,y,image):
		super().__init__(x,y)
		self.image = image
		self.width = self.image.get_rect()[2]
		self.height = self.image.get_rect()[3]
	
	def spawn(self, center = True):
		if center:
			self.win.blit(self.image,(self.image.get_rect(center = (self.x , self.y))))
		else:
			self.win.blit(self.image,(self.x , self.y))