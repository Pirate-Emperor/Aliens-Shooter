import pygame
from random import choice

shape = [
' xx  xxx  xx ',
'x  xxxxxxx  x',
'xxxxx   xxxxx',
'x   x   x   x',
'xxxxx   xxxxx',
'x  xxxxxxx  x',
' xx  xxx  xx ']

class Block(pygame.sprite.Sprite):
	def __init__(self,size,color,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft = (x,y))
		self.cord=(x,y)
	def blocks_motion(self,x_s,y_s):
		d=choice([-2,-1,0,1,2])
		if (d<2 and d>-2): self.rect.x+=d
		else: self.rect.y+=d/2
		if (self.rect.y<self.cord[1]): self.rect.y=self.cord[1]
		elif (self.rect.y-self.cord[1]>=y_s): self.rect.y=y_s+self.cord[1]
		if (self.rect.x<self.cord[0]): self.rect.x=self.cord[0]
		elif (self.rect.x-self.cord[0]>=x_s): self.rect.x=x_s+self.cord[1]
