from csv import reader
from level_settings import tile_size
import os
import pygame

def import_folder(path) -> list:
    
    surface_list = []

    file_names = [file_name for file_name in os.listdir(path) if file_name.endswith(".png")]
    sorted_file_names = sorted(file_names, key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))
    
    for file_name in sorted_file_names:
        if file_name.endswith(".png"):
            full_path = os.path.join(path, file_name)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
    
    return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size,tile_size), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles








