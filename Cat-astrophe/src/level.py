from support import import_csv_layout, import_cut_graphics
from level_settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, AnimatedTile, Life, Palm
from enemy import Enemy, Obstacle
from decoration import Sky, Water, Clouds
from player import Player
import pygame

class Level:
    def __init__(self,level_data,surface,change_treats,change_health,cur_health,max_health):

        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)
        self.bullets = pygame.sprite.Group()

        #user interface
        self.change_treats = change_treats
        self.current_health = cur_health
        self.max_health = max_health
        self.change_health = change_health

        #terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        #palms
        palm_layout = import_csv_layout(level_data['palms'])
        self.palm_sprites = self.create_tile_group(palm_layout, 'palms')

        #treats
        treat_layout = import_csv_layout(level_data['treats'])
        self.treat_sprites = self.create_tile_group(treat_layout, 'treats')

        #extra-life
        extralife_layout = import_csv_layout(level_data['extra-life'])
        self.extralife_sprites = self.create_tile_group(extralife_layout, 'extra-life')

        #enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        #constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        #obstacles
        obstacle_layout = import_csv_layout(level_data['obstacles'])
        self.obstacle_sprites = self.create_tile_group(obstacle_layout, 'obstacles')

        #obstacles constraints
        obstacle_constraint_layout = import_csv_layout(level_data['obstacle_constraints'])
        self.obstacle_constraint_sprites = self.create_tile_group(obstacle_constraint_layout, 'obstacle_constraints')

        #decoration
        horizon = 7
        self.sky = Sky(horizon)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400,level_width,20)
    
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('assets/images/terrain/terrain_tiles.png') 
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('assets/images/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'palms':
                        if val == '0': sprite = Palm(tile_size,x,y,'assets/images/terrain/palm_small',0.1,38)
                        if val == '1': sprite = Palm(tile_size,x,y,'assets/images/terrain/palm_large',0.1,70)
                        if val == '2': sprite = Palm(tile_size,x,y,'assets/images/terrain/palm_bg',0.1,64)

                    if type == 'treats':
                        sprite = AnimatedTile(tile_size,x,y,'assets/images/treat',0.05)

                    if type == 'extra-life':
                        sprite = Life(tile_size,x,y,'assets/images/extra-life',0.1)

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y,'assets/images/enemies/shark/run')

                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)

                    if type == 'obstacles':
                        sprite = Obstacle(tile_size,x,y,'assets/images/obstacle/run')

                    if type == 'obstacle_constraints':
                        sprite = Tile(tile_size,x,y)
                    
                    sprite_group.add(sprite)
        
        return sprite_group
    
    def player_setup(self,layout,change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y),change_health)
                    self.player.add(sprite)
    
    def enemy_constraints_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()
    
    def obstacle_constraints_collision(self):
        for obstacle in self.obstacle_sprites.sprites():
            if pygame.sprite.spritecollide(obstacle,self.obstacle_constraint_sprites,False):
                obstacle.reverse()
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_width // 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width * 3/4 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):

        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ground = False
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

    def check_treat_collisions(self):
        collided_treat = pygame.sprite.spritecollide(self.player.sprite,self.treat_sprites,True)
        if collided_treat:
            for treat in collided_treat:
                self.change_treats(1)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        obstacle_collisions = pygame.sprite.spritecollide(self.player.sprite,self.obstacle_sprites,False)
        if enemy_collisions or obstacle_collisions:
            self.player.sprite.get_damage()
        pygame.sprite.groupcollide(self.enemy_sprites, self.bullets, True, True)
        # pygame.sprite.groupcollide(self.obstacle_sprites, self.bullets, True, True)

    def check_life_collisions(self):
        
        extra_life_collisions = pygame.sprite.spritecollide(self.player.sprite, self.extralife_sprites, True)
        if extra_life_collisions: #and self.current_health < self.max_health (no me carga la vida con este if statement)
            #incluso en get damage, con change_health, el cur health que le paso sigue siendo 3, ese es el problema.
            for life in extra_life_collisions:
                self.change_health(1)

    def death(self):
        pass
    
    def win(self):
        pass
    
    def run(self):

        self.sky.draw(self.display_surface)

        self.clouds.draw(self.display_surface,self.world_shift)

        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        self.palm_sprites.draw(self.display_surface)
        self.palm_sprites.update(self.world_shift)

        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        self.enemy_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_constraints_collision()

        self.obstacle_sprites.draw(self.display_surface)
        self.obstacle_sprites.update(self.world_shift)
        self.obstacle_constraint_sprites.update(self.world_shift)
        self.obstacle_constraints_collision()

        self.treat_sprites.draw(self.display_surface)
        self.treat_sprites.update(self.world_shift)

        self.extralife_sprites.draw(self.display_surface)
        self.extralife_sprites.update(self.world_shift)

        self.bullets.draw(self.display_surface)
        self.bullets.update()
        self.player.draw(self.display_surface)
        player_position = self.player.sprite.rect.center
        self.player.update(self.bullets,player_position)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()

        self.check_treat_collisions()
        self.check_enemy_collisions()
        self.check_life_collisions()

        self.water.draw(self.display_surface,self.world_shift)
        