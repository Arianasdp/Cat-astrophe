import pygame
from level_settings import vertical_tile_number,tile_size, map_width, screen_width
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
    def __init__(self,horizon, style = 'level'):
        self.top = pygame.image.load('assets/images/decoration/sky/sky_top.png').convert()
        self.middle = pygame.image.load('assets/images/decoration/sky/sky_middle.png').convert()
        self.bottom = pygame.image.load('assets/images/decoration/sky/sky_bottom.png').convert()
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top,(map_width,tile_size))
        self.middle = pygame.transform.scale(self.middle,(map_width,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(map_width,tile_size))

        self.style = style
        if self.style == 'overworld':
            palms = import_folder('assets/images/nodes/palms')
            self.palms = []

            for surface in [choice(palms) for image in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50,100)
                rect = surface.get_rect(midbottom = (x,y))
                self.palms.append((surface,rect))

            clouds = import_folder('assets/images/nodes/clouds')
            self.clouds = []

            for surface in [choice(clouds) for image in range(10)]:
                x = randint(0, screen_width)
                y = randint(0,(self.horizon * tile_size) - 100)
                rect = surface.get_rect(midbottom = (x,y))
                self.clouds.append((surface,rect))

    def draw(self,surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.middle,(0,y))
            else:
                surface.blit(self.bottom,(0,y))
        
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0],palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0],cloud[1])

class Water:
    def __init__(self,top,level_width):
        water_start = -map_width
        water_tile_width = 192
        tile_x_amount = int((level_width + map_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192,x,y,'assets/images/decoration/water',0.15)
            self.water_sprites.add(sprite)
    
    def draw(self,surface,x_shift):
        self.water_sprites.draw(surface)
        self.water_sprites.update(x_shift) 

class Clouds():
    def __init__(self,horizon,level_width,cloud_number):
        cloud_surf_list = import_folder('assets/images/decoration/clouds')
        min_x = -map_width
        max_x = level_width + map_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self,surface,x_shift):
        self.cloud_sprites.draw(surface)
        self.cloud_sprites.update(x_shift)