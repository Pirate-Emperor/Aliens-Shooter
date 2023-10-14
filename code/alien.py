import pygame
"""cluster=[
	"rrrrrrrrr",
	"ggggggggg",
	"yyyyyyyyy"
]"""
"""cluster=[
	"  rrr  rrrr  rrr ",
	" rrrr gg gg rrrr ",
	"r gg y y y y gg r",
	" rrrr gg gg rrrr ",
	"  rrr  rrrr  rrr "
]"""
"""cluster=[
	"r   rrr     rrr   r",
	"r   rggr   rggr   r",
	"grrry y yry y yrrrg",
	"r   rggr   rggr   r",
	"r   rrr     rrr   r"
]"""
cluster=[
	"   rrr     rrr   ",
	"   rggr   rggr   ",
	"rrry y yry y yrrr",
	"   rggr   rggr   ",
	"   rrr     rrr   "
]
class Alien(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = './graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))

		if color == 'red': self.value = 100
		elif color == 'green': self.value = 200
		else: self.value = 300

	def update(self,direction):
		self.rect.x += direction


class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		self.image = pygame.image.load('./graphics/extra.png').convert_alpha()
		
		if side == 'right':
			x = screen_width + 50
			self.speed = - 3
		else:
			x = -50
			self.speed = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed