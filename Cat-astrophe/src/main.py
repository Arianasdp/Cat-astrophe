import pygame, sys
from level_settings import * 
from overworld import Overworld
from level import Level
from config import *
from game_data import level_1
from ui import UI

class Game:
	def __init__(self) -> None:

		self.max_level = 3

		self.overworld = Overworld(0,self.max_level,screen)
	
	def run(self):

		self.overworld.run()

class GameStatus:
	def __init__(self) -> None:

		self.state = 'intro'
		
		# game attributes
		self.max_health = 3
		self.cur_health = 3
		self.treats = 0
		
		# audio 
		self.level_bg_music = pygame.mixer.Sound('assets/sounds/level_music.wav')
		self.intro_bg_music = pygame.mixer.Sound('assets/sounds/intro_music.wav')

		#user interface
		self.ui = UI(screen)

		self.level1 = Level(level_1,screen,self.change_treats,self.change_health,self.cur_health,self.max_health)

	def change_treats(self,amount):
		self.treats += amount

	def change_health(self,amount):
		self.cur_health += amount

	def intro(self,title,background,play,exit):

		play_rect = pygame.Rect(500, 350, play.get_width(), play.get_height())
		exit_rect = pygame.Rect(500, 400, exit.get_width(), exit.get_height())

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				if play_rect.collidepoint(mouse_pos):
					self.state = 'main_game'
				elif exit_rect.collidepoint(mouse_pos):
					pygame.quit()
					sys.exit()
		
		screen.blit(background, ORIGIN)
		screen.blit(title, (300,200))
		screen.blit(play, (500,350))
		screen.blit(exit, (500,400))

		pygame.display.update()
		
	
	def main_game(self):
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
	
		self.level1.run()
		self.ui.show_health(self.cur_health,self.max_health)
		self.ui.show_treats(self.treats)

		pygame.display.update()
	
	def state_manager(self):
		if self.state == 'intro':
			self.intro(title,background,play,exit)
		if self.state == 'main_game':
			self.main_game()

	# def reset_game(self):
	# 	self.cur_health = self.max_health
	# 	self.treats = 0
	# 	self.game_over = False
			
		
# Game over
#retry_rect = pygame.Rect(500, 350, retry.get_width(), retry.get_height())
# exit_rect = pygame.Rect(500, 400, exit.get_width(), exit.get_height())
# screen.blit(background, ORIGIN)
# screen.blit(game_over, (400,200))
# screen.blit(retry, (500,350))
# screen.blit(exit, (500,400))

# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	mouse_pos = pygame.mouse.get_pos()
			# 	if retry_rect.collidepoint(mouse_pos):
			# 		self.state = 'intro'  
			# 		self.game_over = True 
			# 	elif exit_rect.collidepoint(mouse_pos):
			# 		pygame.quit()
			# 		sys.exit()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
# old_game = GameStatus()
game = Game()

pygame.display.set_caption("Cat-astrophe")

icon = pygame.image.load("assets/images/extra-life/01.png").convert_alpha() #porque tiene transparencia - es png
icon = pygame.transform.scale(icon, SIZE_ICON)
pygame.display.set_icon(icon)

title = pygame.image.load("assets/images/intro/Cat-astrophe.png").convert_alpha()
game_over = pygame.image.load("assets/images/game over/game_over.png").convert_alpha()
play = pygame.image.load("assets/images/intro/play.png").convert_alpha()
exit = pygame.image.load("assets/images/intro/exit.png").convert_alpha()
retry = pygame.image.load("assets/images/game over/retry.png").convert_alpha()

background = pygame.image.load("assets/images/intro/background.jpg").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

while True:

	clock.tick(FPS)

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	# old_game.state_manager()

	screen.blit(background, ORIGIN)
	game.run()

	pygame.display.update()
	