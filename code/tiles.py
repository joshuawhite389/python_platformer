import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (pos))

    def update(self, x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, surface, pos, size):
        super().__init__(pos, size)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, pos):
        super().__init__(pos, size, pygame.image.load('../graphics/terrain/crate.png').convert_alpha())