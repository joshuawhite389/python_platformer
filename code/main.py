import sys
from settings import *
from tiles import *
from level import Level
from game_data import level_0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
game_title = pygame.display.set_caption('Platformer Game')
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    #right now this just draws the tiles onto the screen and shifts the view
    level.run()

    pygame.display.update()
    clock.tick(60)