from support import import_csv_layout, import_cut_graphics
from level_settings import tile_size, screen_height, screen_width, map_height
from tiles import Tile, StaticTile, AnimatedTile, Life, Palm
from enemy import Enemy, Obstacle, Explotion
from decoration import Sky, Water, Clouds
from player import Player
from game_data import levels
from ui import Timer
import pygame

class Level:
    def __init__(self,current_level,surface,create_overworld,game_over,change_treats,change_health,change_score,cur_health,max_health,pause):

        self.display_surface = surface
        self.world_shift = 0

        self.paused = pause
        self.time = Timer(self.display_surface, (600,25))
        self.time_up = False

        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        self.game_over = game_over

        self.cur_score = 0

        #audio
        self.treat_sound = pygame.mixer.Sound('assets/sounds/effects/crunch.wav')
        self.explosion_sound = pygame.mixer.Sound('assets/sounds/effects/explode.wav')
        self.extra_life_sound = pygame.mixer.Sound('assets/sounds/effects/life.wav')
        self.game_over_sound = pygame.mixer.Sound('assets/sounds/effects/game_over.wav')
        self.level_completed_sound = pygame.mixer.Sound('assets/sounds/effects/level_completed.wav')

        #score
        self.score_menu = pygame.image.load("assets/images/score/score_menu.png").convert_alpha()
        self.scores_button = pygame.image.load("assets/images/score/scores_button.png").convert_alpha()
        self.continue_option = pygame.image.load("assets/images/pause/continue.png").convert_alpha()

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
        self.change_score = change_score

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
        self.enemy_bullets = pygame.sprite.Group()

        #explotions
        self.explosions = pygame.sprite.Group()

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
        self.water = Water(map_height - 40, level_width)
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
    
    
    def enemy_constraints_collision(self,enemy_positions):
         for enemy, enemy_pos in zip(self.enemy_sprites.sprites(), enemy_positions):
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse(self.enemy_bullets,enemy_pos)
    
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
            self.treat_sound.play()
            for treat in collided_treat:
                self.change_treats(1)
                self.cur_score = self.change_score(5)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        obstacle_collisions = pygame.sprite.spritecollide(self.player.sprite,self.obstacle_sprites,False)
        enemy_bullet_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_bullets,False)

        if enemy_collisions or obstacle_collisions or enemy_bullet_collisions:
            self.current_health = self.player.sprite.get_damage(self.current_health)
            if obstacle_collisions:
                self.explosion_sound.play()
                for obstacle in obstacle_collisions:
                    explotion = Explotion(obstacle.rect.center, 'assets/images/obstacle/explosion', 0.5)
                    self.explosions.add(explotion)
                    obstacle.kill()

        for enemy in self.enemy_sprites:
            bullet_collisions = pygame.sprite.spritecollide(enemy, self.bullets, True)
            if bullet_collisions:
                self.explosion_sound.play()
                explotion = Explotion(enemy.rect.center, 'assets/images/enemies/shark/explosion', 0.5)
                self.explosions.add(explotion)
                enemy.kill()
                self.cur_score = self.change_score(10)
        pygame.sprite.groupcollide(self.enemy_bullets, self.bullets, True, True)

    def check_life_collisions(self):
        
        extra_life_collisions = pygame.sprite.spritecollide(self.player.sprite, self.extralife_sprites, False)
        if extra_life_collisions and self.current_health < self.max_health:
            self.extra_life_sound.play()
            for life in extra_life_collisions:
                self.current_health = self.change_health(1)
                life.kill()

    def check_death(self):
        if self.player.sprite.rect.top > screen_height or self.current_health == 0 or self.time_up:
            self.game_over_sound.play()
            self.game_over()
    
    def check_win(self):
        if len(self.treat_sprites) == 0 and len(self.enemy_sprites) == 0:
            self.level_completed_sound.play()
            self.time.pause()
            elapsed_seconds = self.time.get_elapsed_time()
            remaining_seconds = 60 - elapsed_seconds
            
            self.cur_score = self.change_score(remaining_seconds * 100)
            
            self.create_overworld(self.current_level,self.new_max_level)
    
    def run(self):

        self.sky.draw(self.display_surface)

        self.clouds.draw(self.display_surface,self.world_shift)

        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        self.palm_sprites.draw(self.display_surface)
        self.palm_sprites.update(self.world_shift)

        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        self.enemy_bullets.draw(self.display_surface)
        self.enemy_bullets.update()
        self.enemy_sprites.draw(self.display_surface)
        enemy_positions = []
        for enemy in self.enemy_sprites:
            enemy_pos = enemy.rect.center
            enemy_positions.append(enemy_pos)
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_constraints_collision(enemy_positions)

        self.obstacle_sprites.draw(self.display_surface)
        self.obstacle_sprites.update(self.world_shift)
        self.obstacle_constraint_sprites.update(self.world_shift)
        self.obstacle_constraints_collision()

        self.explosions.draw(self.display_surface)
        self.explosions.update(self.world_shift)
        
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

        self.check_death()
        self.check_win()

        self.water.draw(self.display_surface,self.world_shift)

        self.paused()
        self.time.draw()
        self.time.update()
        self.time_up = self.time.time_up()

        return self.current_level, self.cur_score
        