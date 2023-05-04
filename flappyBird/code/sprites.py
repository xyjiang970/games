import pygame
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        """Background init"""
        super().__init__(groups)
        bg_image = pygame.image.load('./graphics/environment/background.png').convert()
        
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width*2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))
        
        self.rect = self.image.get_rect(topleft = (0, 0)) 
        self.pos = pygame.math.Vector2(self.rect.topleft)


    def update(self, dt):
        """Background update"""
        self.pos.x -= 300*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        """Ground init"""
        super().__init__(groups)

        # image
        ground_surf = pygame.image.load('./graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)

        # position
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    
    def update(self, dt):
        """Ground init"""
        self.pos.x -= 360*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor) # import a list of surfaces
        self.frame_index = 0 # pick one of the surfaces
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 600 # how fast the plane falls
        self.direction = 0 # plane can go up and down


    def import_frames(self, scale_factor):
        self.frames = []

        for i in range(3):
            surf = pygame.image.load(f'./graphics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)


    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    
    def jump(self):
        self.direction = -400


    def animate(self, dt):
        self.frame_index += 20 * dt # animation speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


    def rotate(self):
        # rotozoom takes 3 arguments: surface, rotation/ angle, and scale
        rotated_plane = pygame.transform.rotozoom(self.image,
                                                  -self.direction * 0.075,
                                                  1)
        self.image = rotated_plane


    def update(self, dt):
        # order matters here! 
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()