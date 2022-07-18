import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = pygame.Surface ((32,64))
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = (pos))

        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.09
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        #player status, these inform the animation states and are set in the levels class with collisions
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        #support.py class loads files in a usable way, we load images into the below dictionary, we then take those animations and use them in animate method
        character_path = '../graphics/character/'
        self.animations = {'idle' : [], 'run' : [], 'jump' : [], 'fall' : []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        #making the frame index an int rounds the number to the nearest whole, effectively slowing down animation
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = animation[int(self.frame_index)]
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        #set the rect
        #this fixes the animation so that it fits exactly on the corresponding surfaces
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = (self.rect.bottomright))
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = (self.rect.bottomleft))
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = (self.rect.midbottom))
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = (self.rect.topright))
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = (self.rect.topleft))
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = (self.rect.midtop))

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                #subtracting this vector makes the animation appear in the correct place
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)

            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)


    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_speed
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x == 0:
                self.status = 'idle'
            else:
                self.status = 'run'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def update(self):
        self.get_input()
        self.animate()
        self.get_status()
        self.run_dust_animation()


