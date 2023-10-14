import pygame, sys, os
from player import Player
import obstacle
from alien import Alien, Extra, cluster
from random import choice, randint
from laser import Laser
 
class Game:
	def __init__(self):
		# Screen reset
		set_sig=500
		reset_sig=500
		# Player setup
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# health and score setup
		self.lives = 3
		self.live_surf = pygame.image.load('./graphics/player.png').convert_alpha()
		self.live_x_start_pos = screen_width -self.live_surf.get_size()[0]-10
		self.score = 0

		# Obstacle setup
		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 5
		self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 480)

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup()
		self.alien_direction = 2                              

		# Extra setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(400,800)

		# Audio
		music = pygame.mixer.Sound('./audio/music.wav')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('./audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)
		self.check=False
	def kill(self):
		self.player.sprite.remove()
		#self.extra.sprite.remove()
		self.aliens.empty()
		self.alien_lasers.empty()
		self.blocks.empty()

	def font(self,x=20):
		return pygame.font.Font('./font/Pixeled.ttf ',x)
	def create_obstacle(self, x_start, y_start,offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size,(255,255//(row_index+1),255//(col_index+1)),x,y)
					self.blocks.add(block)

	def create_multiple_obstacles(self,*offset,x_start,y_start):
		for offset_x in offset:
			self.create_obstacle(x_start,y_start,offset_x)

	def alien_setup(self,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(cluster):
			for col_index, col in enumerate(row):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if cluster[row_index][col_index] == 'y': alien_sprite = Alien('yellow',x,y)
				elif cluster[row_index][col_index] == 'g': alien_sprite = Alien('green',x,y)
				elif cluster[row_index][col_index] == 'r': alien_sprite = Alien('red',x,y)
				else: continue #alien_sprite = Alien('red',x,y)
				self.aliens.add(alien_sprite)
	"""def obstacle_position_checker(self):
		all_obs = self.blocks.sprites()
		for obs in all_obs:
			if (self.rect.y<cord[1]): self.rect.y=y_u
			elif (self.rec.y-cord[1]>=y_s): self.rect.y=y_u+cord[1]
			if (self.rect.x<cord[0]): self.rect.x=x_u
			elif (self.rec.x-cord[0]>=x_s): self.rect.x=x_u+cord[1]
	
	def blocks_motion(self,x_s,y_s):
		d=choice(-2,-1,0,1,2)
		if (d<2 and d>-2): self.rect.x+=d
		else: self.rect.y+=d/2
		if (self.rect.y<cord[1]): self.rect.y=y_u
		elif (self.rec.y-cord[1]>=y_s): self.rect.y=y_u+cord[1]
		if (self.rect.x<cord[0]): self.rect.x=x_u
		elif (self.rec.x-cord[0]>=x_s): self.rect.x=x_u+cord[1]"""
	
	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= screen_width:
				self.alien_direction = -2
				self.alien_move_down(5)
			elif alien.rect.left <= 0:
				self.alien_direction = 2
				self.alien_move_down(5)

	def alien_move_down(self,distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,6,screen_height)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']),screen_width))
			self.extra_spawn_time = randint(400,800)
	"""def reset_timer(self,check=false):
		self.reset_sig -= 1
		if (self.reset_sig <= 0):
			self."""
	def collision_checks(self):

		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
					

				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					laser.kill()
					self.explosion_sound.play()

				# extra collision
				if pygame.sprite.spritecollide(laser,self.extra,True):
					self.score += 500
					laser.kill()

		# alien lasers 
		if self.alien_lasers:
			for laser in self.alien_lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()

				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					if self.lives <= 0:
						screen.fill((0,0,0))
						pygame.display.update()
						self.kill()
						self.defeat_message()
						self.check=True
						

		# aliens
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien,self.blocks,True)
				if pygame.sprite.spritecollide(alien,self.player,False):
					pygame.quit()
					sys.exit()
	
	def display_lives(self):
		for live in range(self.lives):
			x = self.live_x_start_pos - (live * (self.live_surf.get_size()[0] + 10))
			screen.blit(self.live_surf,(x,8))

	def display_score(self):
		score_surf = self.font(30).render(f'SCORE: {self.score}',False,(255,255,255))
		score_rect = score_surf.get_rect(topleft = (0,0))
		screen.blit(score_surf,score_rect)

	def victory_message(self):
		if not self.aliens.sprites():
			victory_surf = self.font(40).render('You won',False,(255,255,255))
			victory_rect = victory_surf.get_rect(center = (screen_width // 2, screen_height // 2))
			screen.blit(victory_surf,victory_rect)
	def defeat_message(self):
		if not self.lives:
			defeat_surf = self.font(40).render('Game Over',False,(255,255,255))
			defeat_rect = defeat_surf.get_rect(center = (screen_width // 2, screen_height // 2))
			screen.blit(defeat_surf,defeat_rect)



	def run(self):
		self.player.update()
		self.alien_lasers.update()
		self.extra.update()
		
		self.aliens.update(self.alien_direction)
		self.alien_position_checker()
		self.extra_alien_timer()
		self.collision_checks()
		#for spir in self.blocks.sprites():
		#	spir.blocks_motion(20,10)
		
		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		self.blocks.draw(screen)
		self.aliens.draw(screen)
		self.alien_lasers.draw(screen)
		self.extra.draw(screen)
		self.display_lives()
		self.display_score()
		#self.victory_message()
		#self.defeat_message()
class CRT:
	def __init__(self):
		self.tv = pygame.image.load('./graphics/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

	def create_crt_lines(self):
		line_height = 5
		line_amount = int(screen_height / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,(0,0,0),(0,y_pos),(screen_width,y_pos),1)

	def draw(self):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		screen.blit(self.tv,(0,0))

if __name__ == '__main__':
	pygame.init()
	screen_width = 1280
	screen_height = 600
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()
	reset=False
	crt = CRT()

	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,800)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key in [pygame.K_ESCAPE]:
					pygame.quit()
					sys.exit()
			if event.type == ALIENLASER:
				game.alien_shoot()

		screen.fill((0,0,0))
		
		if (game.check): 
			while game.check:
				for eve in pygame.event.get():
					if eve.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if eve.type==pygame.KEYDOWN:
						if (eve.key==pygame.K_ESCAPE):
							pygame.quit()
							sys.exit()
						elif eve.key==pygame.K_RETURN:
							game = Game()
							reset=False
							ALIENLASER = pygame.USEREVENT + 1
							pygame.time.set_timer(ALIENLASER,800)
							game.check=False
							break
		game.run()
		"""screen.fill((0,0,0))
		game.run()"""
		#crt.draw()	
		pygame.display.flip()
		clock.tick(60)