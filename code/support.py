from os import walk
from csv import reader
import pygame.image
from settings import tile_size
import pygame

#import images for animation
def import_folder(path):
    surface_list = []
    image_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            # .ds_Store file (hidden file in mac) messing up this loop, excluding hidden files with this condition
            # also for some reason, the os.walk function is taking the images out of order causing the animation to look bad, so I sort the images first
            if (image[0] != '.'):
                image_list.append(image)
                image_list.sort()


        for img in image_list:
            full_path = path + '/' + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)


    return surface_list


#import a map from tiled
def import_csv_layout(path):
    with open(path) as map:
        terrain_map = []
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[0] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            # SRCALPHA will give us proper alpha values
            new_surf = pygame.Surface((tile_size, tile_size), flags= pygame.SRCALPHA )
            new_surf.blit(surface, (0,0), pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles