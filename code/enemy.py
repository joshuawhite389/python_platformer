import pygame
from tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, size, pos):
        super().__init__(size, pos, '../graphics/enemy/run')
