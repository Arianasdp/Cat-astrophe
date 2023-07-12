import pygame
from tiles import AnimatedTile
from random import randint
from player import Bullet
from support import import_folder
from level_settings import screen_width, screen_height

class Enemy(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path,0.15)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3,5)
        self.facing_right = False

        #audio
        self.enemy_bullet_sound = pygame.mixer.Sound('assets/sounds/effects/laser.mp3')
        self.enemy_bullet_sound.set_volume(0.3)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
            self.facing_right = True
        else:
            self.facing_right = False

    def reverse(self,bullets,enemy_pos):
        self.speed *= -1
        new_x = enemy_pos[0] + self.speed
        if not (0 <= new_x <= screen_width and 0 <= enemy_pos[1] <= screen_height):
            return
        else:
            self.attack(bullets,enemy_pos,self.facing_right)

    def attack(self,bullets,enemy_pos,facing_right):
        self.enemy_bullet_sound.play()
        bullet = Bullet(enemy_pos[0],enemy_pos[1],facing_right,"assets/images/proyectiles/enemy's")
        bullets.add(bullet)

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.reverse_image()

class Obstacle(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path,0.1)
        self.rect.x += -10
        self.speed = randint(3,5)
    
    def move(self):
        self.rect.y += self.speed

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()

class Explotion(pygame.sprite.Sprite):
    def __init__(self, pos, path, speed) -> None:
        super().__init__()
        self.frame_index = 0
        self.frame_speed = speed
        self.frames = import_folder(path)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

    

        