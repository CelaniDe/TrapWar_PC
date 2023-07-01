import pygame

class Player:
	def __init__(self,x,y,color):
		self.x = x
		self.y = y
		self.width = 50
		self.height = 50
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.color = color
		self.position = pygame.Vector2(self.x,self.y)
		self.velocity = pygame.Vector2()

	def spawn(self,win):
		pygame.draw.rect(win , self.color , self.rect)

	def move(self,direction_vector):
		self.position = self.position.elementwise() + direction_vector.elementwise()
		self.rect = pygame.Rect(self.position.x,self.position.y,self.width,self.height)