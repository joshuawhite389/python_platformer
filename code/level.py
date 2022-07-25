import pygame
from tiles import *
from settings import *
from player import Player
from dust_particles import ParticleEffect
from support import import_csv_layout
from support import import_cut_graphic
from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):
        #we pass in the screen in the main file as the surface here
        self.display_surface = surface


        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crate setup
        crate_layout = import_csv_layout(level_data['crate'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crate')

        #coins setup
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        #fg palms
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # bg palms
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        #see below
        self.world_shift = 0
        self.current_x = 0
        self.player_on_ground = False

        #dust particles
        self.dust_sprite = pygame.sprite.GroupSingle()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground= False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def create_tile_group(self, layout, type):
        sprite_group= pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # if we don't multiply by tile size, they all stack on top of each other
                x = col_index * tile_size
                y = row_index * tile_size
                if val != '-1':
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_surface,(x,y),tile_size)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphic('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_surface,(x,y),tile_size)

                    if type == 'crate':
                        sprite = Crate(tile_size,(x,y))

                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, (x, y), '../graphics/coins/gold')
                        if val == '1':
                            sprite = Coin(tile_size, (x, y), '../graphics/coins/silver')

                    if type == 'fg_palms':
                        if val == '0':
                            sprite = Palm(tile_size, (x, y), '../graphics/terrain/palm_small', 38)
                        if val == '1':
                            sprite = Palm(tile_size, (x, y), '../graphics/terrain/palm_large', 70)

                    if type == 'bg_palms':
                        sprite = Palm(tile_size, (x, y), '../graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        print('enemies!!!')
                        sprite = Enemy(tile_size, (x, y))
                        

                    sprite_group.add(sprite)






            #         #this gets drawn in the run method below
            #         self.tiles.add(tile)
            # # we are creating the player here
            #     if val == 'P':
            #         player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
            #         self.player.add(player_sprite)
        return sprite_group

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    #need to separately address vertical and horizontal collisions in pygame

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >=0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        #looping through all the tiles in the tile sprite group to detect collisions
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0 :
                player.on_ceiling = False

    def run(self):


        # dust particles
        # self.dust_sprite.update(self.world_shift)
        # self.dust_sprite.draw(self.display_surface)

        # the world shift is used to scroll the screen
        # calling the update method from the tiles class which just shifts the screen based on some x value

        #level tiles

        # background palms
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)

        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        #foreground palms
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)

        # enemies
        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)

        # self.scroll_x()

        #player
        # self.player.update()
        # self.get_player_on_ground()
        # self.horizontal_movement_collision()
        # self.vertical_movement_collision()
        # self.create_landing_dust()
        # self.player.draw(self.display_surface)
