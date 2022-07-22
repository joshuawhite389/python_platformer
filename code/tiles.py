import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos))

    def update(self, x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, surface, pos, size):
        super().__init__(pos, size)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, pos):
        super().__init__(pygame.image.load('../graphics/terrain/crate.png').convert_alpha(), pos, size)
        x = pos[0]
        y = pos[1]
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))

class AnimatedTile(Tile):
    def __init__(self, size, pos, path):
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]


    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]



    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

class Coin(AnimatedTile):
    def __init__(self, size, pos, path):
        super().__init__(size, pos, path)
        center_x = pos[0] + int(size / 2)
        center_y = pos[1] + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))

class Palm(AnimatedTile):
    def __init__(self, size, pos, path, offset):
        super().__init__(size, pos, path)
        x = pos[0]
        y = pos[1]
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)
