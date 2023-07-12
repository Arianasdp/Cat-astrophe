import pygame, sys
from level_settings import * 
from overworld import Overworld
from level import Level
from config import *
from ui import UI

class Game:
	def __init__(self) -> None:

		self.max_level = 0 #2 máximo
		self.status = 'intro'
		self.cur_level = self.max_level

		# game attributes
		self.max_health = 3
		self.cur_health = 3
		self.treats = 0
		self.cur_score = 0
		self.level_score = 0

		#audio
		self.overworld_bg_music = pygame.mixer.Sound('assets/sounds/overworld_music.wav')
		self.overworld_bg_music.set_volume(0.3)
		self.level_bg_music = pygame.mixer.Sound('assets/sounds/level_music.wav')
		self.level_bg_music.set_volume(0.3)
		
		#primera creación del overworld
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.overworld_bg_music.play(loops = -1)
		
		#intro
		self.title = pygame.image.load("assets/images/intro/Cat-astrophe.png").convert_alpha()
		
		self.play = pygame.image.load("assets/images/intro/play.png").convert_alpha()
		self.exit = pygame.image.load("assets/images/intro/exit.png").convert_alpha()
		self.background = pygame.transform.scale(pygame.image.load("assets/images/intro/background.jpg").convert(), (screen_width, screen_height))
		
		self.exit_rect = pygame.Rect(500, 400, self.exit.get_width(), self.exit.get_height())

		#game over
		self.game_over = pygame.image.load("assets/images/game over/game_over.png").convert_alpha()
		self.retry = pygame.image.load("assets/images/game over/retry.png").convert_alpha()

		#pause_menu
		self.pause_title = pygame.image.load("assets/images/pause/pause.png").convert_alpha()
		self.continue_option = pygame.image.load("assets/images/pause/continue.png").convert_alpha()
		self.music_title = pygame.image.load("assets/images/pause/music.png").convert_alpha()
		self.music_option = pygame.image.load("assets/images/pause/on-off.png").convert_alpha()
		self.pause_option = pygame.image.load("assets/images/pause/pause_option.png").convert_alpha()

		#score menu
		self.score_menu = pygame.image.load("assets/images/score/score_menu.png").convert_alpha()
		self.scores_button = pygame.image.load("assets/images/score/scores_button.png").convert_alpha()

		#user interface
		self.ui = UI(screen)
	
	def create_intro(self):

		play_rect = pygame.Rect(500, 350, self.play.get_width(), self.play.get_height())
		
		if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				if play_rect.collidepoint(mouse_pos):
					self.status = 'overworld'
				elif self.exit_rect.collidepoint(mouse_pos):
					pygame.quit()
					sys.exit()
			
		screen.blit(self.background, ORIGIN)
		screen.blit(self.title, (300,200))
		screen.blit(self.play, play_rect)
		screen.blit(self.exit, self.exit_rect)

	def create_game_over(self):
		self.level_bg_music.stop()
		self.status = 'game_over'
		retry_rect = pygame.Rect(500, 350, self.retry.get_width(), self.retry.get_height())

		screen.blit(self.background, ORIGIN)
		screen.blit(self.game_over, (400,200))
		screen.blit(self.retry, retry_rect)
		screen.blit(self.exit, self.exit_rect)

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			if retry_rect.collidepoint(mouse_pos):
				self.create_overworld(self.cur_level,0)
				self.reset_game()
			elif self.exit_rect.collidepoint(mouse_pos):
				pygame.quit()
				sys.exit()

	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.create_game_over,self.change_treats,self.change_health,self.change_score,self.cur_health,self.max_health,self.check_pause)
		self.status = 'level'
		self.overworld_bg_music.stop()
		self.level_bg_music.play(loops = -1)
	
	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.level_bg_music.stop()
		self.overworld_bg_music.play(loops = -1)

	def check_pause(self):

		pause_rect = pygame.Rect(1100, 20, self.pause_option.get_width(), self.pause_option.get_height())

		screen.blit(self.pause_option, pause_rect)

		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_p]:
			self.status = 'paused'
	
	def pause(self):

		music_state = False

		while self.status == 'paused':
			
			continue_rect = pygame.Rect(430, 355, self.continue_option.get_width(), self.continue_option.get_height())
			music_rect = pygame.Rect(560, 290, self.music_option.get_width(), self.music_option.get_height())

			screen.blit(self.pause_title, (435,200))
			screen.blit(self.music_title, (400,290))
			screen.blit(self.continue_option, continue_rect)
			screen.blit(self.music_option, music_rect)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					if continue_rect.collidepoint(mouse_pos):
						self.status = 'level'
					elif music_rect.collidepoint(mouse_pos):
						music_state = not music_state
						if music_state:
							pygame.mixer.pause()
						else:
							pygame.mixer.unpause() 
			pygame.display.update()

	def change_treats(self,amount):
		self.treats += amount

	def change_health(self,amount):
		self.cur_health += amount
		return self.cur_health

	def change_score(self,amount):
		self.cur_score += amount
		return self.cur_score
	
	def reset_game(self):
		self.cur_health = self.max_health
		self.treats = 0
		self.level_score = 0

	def run(self):
		if self.status == 'intro':
			self.create_intro()
		if self.status == 'overworld':
			self.overworld.run()
			self.ui.show_score(self.cur_score,(700,20))
		elif self.status == 'level':
			self.cur_level, self.level_score = self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_treats(self.treats)
			self.ui.show_score(self.level_score,(850,30))
		elif self.status == 'game_over':
			self.create_game_over()
			self.reset_game()
		elif self.status == 'paused':
			self.pause()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

pygame.display.set_caption("Cat-astrophe")

icon = pygame.image.load("assets/images/extra-life/01.png").convert_alpha() #porque tiene transparencia - es png
icon = pygame.transform.scale(icon, SIZE_ICON)
pygame.display.set_icon(icon)

while True:

	clock.tick(FPS)

	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	game.run()

	pygame.display.update()
	