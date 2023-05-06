import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
 
class Game:
    def __init__(self):
        """init"""
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('FlappyPlane')
        self.clock = pygame.time.Clock()

        self.active = True # tracks status of game

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('./graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT/bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, 
                self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.95)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1

        # Shorter timer = faster/ more spawns
        pygame.time.set_timer(self.obstacle_timer, 1000) 

        # text
        self.font = pygame.font.Font('./graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0 # starts at 0
        self.start_offset = 0

        # menu
        self.menu_surf = pygame.image.load('./graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,
                                                           WINDOW_HEIGHT / 2)
                                                          )

        # music
        self.music = pygame.mixer.Sound('./sounds/music.wav')
        self.music.set_volume(0.1)
        self.music.play(loops = -1)
 
    def collisions(self):
        # We want to trigger a collision if the plane collides with an obstacle
        # or if the plane goes goes too high (all the way above the top - thus
        # technically avoiding the obstacles).
        if pygame.sprite.spritecollide(self.plane, 
                                       self.collision_sprites, 
                                       False,
                                       pygame.sprite.collide_mask
                                       ) or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == "obstacle":
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            # get_ticks() gets the time since the game has started -
            # it doesn't really care what happens in game.
            # milliseconds - to convert to seconds just divide by 1000
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5 )

        score_surf = self.font.render(str(self.score), True, "Black")
        # score_rect = position of score
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y)) 
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        """running"""
        last_time = time.time()

        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()
 
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.95)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                # Can increase obstacle vertical length by multiplying
                # scale_factor.
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, 
                              self.collision_sprites], self.scale_factor * 1.1)
            
            # game logic (order matters!)
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active: 
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)
 
if __name__ == '__main__':
    game = Game()
    game.run()