import pygame

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

    def show_score(self,amount,pos):
        score = self.font.render(f'score: {str(amount)}',False,'#33323d')
        self.display_surface.blit(score,pos)


class Timer:
    def __init__(self, surface, pos):

        self.font = pygame.font.Font('assets/images/ui/ARCADEPI.ttf', 36)
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.display_surface = surface
        self.pos = pos
        self.paused = False
        
    def update(self):
        if not self.paused:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
    
    def get_elapsed_time(self):
        return self.elapsed_time
    
    def time_up(self):
        time_up = False
        if self.elapsed_time >= 60:
            time_up = True
        return time_up
    
    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False

    def get_formatted_time(self):
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        return f"{minutes:02}:{seconds:02}"

    def draw(self):
        timer_text = self.get_formatted_time()
        timer_surface = self.font.render(timer_text, True, '#33323d')
        self.display_surface.blit(timer_surface, self.pos)
