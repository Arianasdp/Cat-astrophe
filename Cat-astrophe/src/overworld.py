import pygame
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, path) -> None:
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf,(0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.image.load('assets/images/nodes/cat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)


class Overworld:
    def __init__(self,start_level,max_level,surface,create_level) -> None:
        
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        self.change_cooldown = 500
        self.last_change_time = 0

        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(7, 'overworld')
    
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node = Node(node_data['node_pos'], 'available', node_data['node_graphics'])
            else:
                node = Node(node_data['node_pos'], 'locked', node_data['node_graphics'])
            self.nodes.add(node)
    
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon)
    
    def input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_change_time >= self.change_cooldown:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.current_level += 1
                self.last_change_time = current_time
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.current_level -= 1
                self.last_change_time = current_time
        
        if keys[pygame.K_SPACE]:
            self.create_level(self.current_level)
    
    def update_icon_position(self):
        self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
    
    def _check_timer_elapsed(self, interval):
        current_time = pygame.time.get_ticks()
        return current_time - self.change_timer >= interval

    def run(self):
        self.input()
        self.update_icon_position()
        self.nodes.update()
        self.sky.draw(self.display_surface)
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

        