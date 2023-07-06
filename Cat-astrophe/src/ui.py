import pygame
from level_settings import screen_width,screen_height

class UI:
    def __init__(self,surface):
        
        self.display_surface = surface

        #health
        self.health_0 = pygame.image.load('assets/images/ui/bar health/nolives.png').convert_alpha()
        self.health_1 = pygame.image.load('assets/images/ui/bar health/01life.png').convert_alpha()
        self.health_2 = pygame.image.load('assets/images/ui/bar health/02lives.png').convert_alpha()
        self.health_3 = pygame.image.load('assets/images/ui/bar health/03lives.png').convert_alpha()

        #treat
        self.treat = pygame.image.load('assets/images/ui/treat/treat.png').convert_alpha()
        self.treat_rect = self.treat.get_rect(topleft = (30,70))
        self.font = pygame.font.Font('assets/images/ui/ARCADEPI.ttf',30)
    
    def show_health(self,current,full):
        if current == full:
            health = self.health_3
        elif current == full - 1:
            health = self.health_2
        elif current == full - 2:
            health = self.health_1
        else:
            health = self.health_0
        
        self.display_surface.blit(health,(10,10))

    def show_treats(self,amount):
        self.display_surface.blit(self.treat,self.treat_rect)
        treat_amount_surf = self.font.render(str(amount),False,'#33323d')
        treat_amount_rect = treat_amount_surf.get_rect(midleft = (self.treat_rect.right + 4,self.treat_rect.centery))
        self.display_surface.blit(treat_amount_surf,treat_amount_rect)
