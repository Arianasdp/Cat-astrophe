import pygame 
from support import import_folder
from level_settings import screen_width

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.is_attacking = False

        #movimientos
        self.direction = pygame.math.Vector2(0,0) #con esta función tenés los dos valores (x,y) en la misma variable
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -12 #para ir hacia arriba

        #status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False

        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 700
        self.hurt_time = 0

    def import_character_assets(self):
        character_path = 'assets/images/cat/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation + '/'
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
    
        image = animation[int(self.frame_index)]
        if self.facing_right:    
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image


    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            elif self.direction.x == 0 and self.is_attacking:
                self.status = 'attack'
            else:
                self.status = 'idle'
        

    def get_input(self,bullets,player_pos):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.attack(bullets,player_pos,self.facing_right)
        
        if not keys[pygame.K_SPACE]:
            self.is_attacking = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False
    
    def attack(self, bullets,player_pos, facing_right):
        self.is_attacking = True
        bullet = Bullet(player_pos[0],player_pos[1],facing_right)
        bullets.add(bullet)
    
    def get_damage(self):
        if not self.invincible:
            self.change_health(-1)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
    
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def update(self,bullets,player_pos):
        self.get_input(bullets,player_pos)
        self.get_status()
        self.animate()
        self.invincibility_timer()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x,pos_y,facing_right):
        super().__init__()

        path = "assets\images\proyectiles\player's"
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.facing_right = facing_right       

    def animate(self):

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1
        
        self.image = self.frames[int(self.frame_index)]
        
        image = self.image
        flipped_image = pygame.transform.flip(self.image, True, False)
        if self.facing_right:
            self.image = image
        else:
            self.image = flipped_image

    def update(self):
        self.animate()
        if self.facing_right:
            self.rect.x += 5
            if self.rect.x >= screen_width - 150:
                self.kill()
        else:
            self.rect.x -= 5
            if self.rect.x <= 0:
                self.kill()
		