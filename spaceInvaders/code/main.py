import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        """
        Initiate method of a class (equivalent to C++ constructor). The __init__ function is called
        every time an object is created from a class. The __init__ method lets the class initialize
        the object's attributes and serves no other purpose.

        Sprite groups will be added here (player, aliens, etc).
        """
        ## Player Setup
        player_sprite = Player((screen_width/2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        ## Health and Score Setup
        self.lives = 3
        self.lives_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.lives_x_start_pos = screen_width - (self.lives_surf.get_size()[0]*2 + 20) # Get x parameter (width)
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)

        ## Obstacle Setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num*(screen_width / self.obstacle_amount) \
                                     for num in range(self.obstacle_amount)]
        ## *self.obstacle_x_positions allows for unpacking of the elements in the 
        ## self.obstacle_x_positions list!
        self.create_multiple_obstacles(*self.obstacle_x_positions, 
                                       # x_start positions left most obstacle
                                       x_start=(screen_width/14), # 14-15 works best
                                       y_start=480)
        
        ## Alien Setup
        self.aliens = pygame.sprite.Group()
        ### Player laser and alien laser needs to be in separate groups due to collision 
        ### logic. If all lasers are in the same group, the player will be hit immediately
        ### every time the player spawns a laser (because the player laser spawns 
        ### right behind the player).
        self.alien_lasers = pygame.sprite.Group()      
        self.alien_setup(rows=6, cols=8) # create all of the aliens in a specific position.
        self.alien_direction = 1
        
        ## For Extra Alien Setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800) # extra alien spawn timer - randomized.

        ## Audio
        ### Background Music
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.03)
        music.play(loops = -1) # -1 to play forever.
        ### Sound Effects
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.05)
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(0.08)

    def create_obstacle(self, x_start, y_start, offset_x):
       """
       Function that creates one obstacle. The obstacle consists of individual blocks
       and each of the blocks is a sprite. All sprites are arranged in a way to look like an obstacle
       (couple of square shaped sprites in a certain shape).

       Nested for loop with enumerate method is used to figure out which row, column (column within each row) 
       we are on.
       """
       for row_index, row in enumerate(self.shape): # vertical direction (rows)
           for col_index, col in enumerate(row): # horizontal direction (columns)
               if col == 'x': # ignore empty spaces
                   x = x_start + (col_index * self.block_size) + offset_x
                   y = y_start + (row_index * self.block_size)
                   block = obstacle.Block(self.block_size, 
                                         (241,79,80), x, y)
                   self.blocks.add(block)

    ## Cannot use positional arguments after named arguments so x_start & y_start
    ## need to come after *offset.
    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        """
        Creates all of the aliens in a specific position.
        """
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = (col_index * x_distance) + x_offset
                y = (row_index * y_distance) + y_offset

                if row_index == 0: # top row
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        """
        Cycle through every single alien and if any of the aliens if too far to the right,
        change the direction (self.alien_direction) to -1 (opposite direction). If the aliens
        move too far to the left (< 0), again change the direction to opposite.
        """
        all_aliens = self.aliens.sprites()
        for alien in all_aliens: # look at all sprites individually
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(1)

    def alien_move_down(self, distance):
        """
        Anytime aliens hit either left or right side, move them downwards by a couple pixels.
        """
        ## Will only be run if they are aliens inside the of the alien class. Because if the player
        ## shot down all of the aliens there is no need to keep this method running (will error out).
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        ## Will only be run if they are aliens inside the of the alien class.
        if self.aliens.sprites():
            ## Randomly select a single alien out of all aliens.
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0: # spawns the extra alien when timer hits 0.
            ## Spawns randomly either on left or right side of screen.
            self.extra.add(Extra(choice(['right', 'left']), screen_width)) 
            self.extra_spawn_time = randint(400, 800) # set new timer for next extra alien.

    def collision_checks(self):
        ## Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                ## Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True): # Destroy block
                    laser.kill() # Destroy laser once it hits the block 

                ## Alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)

                if aliens_hit: # Destroy alien
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill() # Destroy laser once it hits the block 
                    self.explosion_sound.play()

                ## Extra Alien collision
                if pygame.sprite.spritecollide(laser, self.extra, True): # Destroy extra alien
                    self.score += 500
                    laser.kill() # Destroy laser once it hits the block 

        ## Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                ## Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True): # Destroy block
                    laser.kill() # Destroy laser once it hits the block 

                ## Alien collisions
                if pygame.sprite.spritecollide(laser, self.player, False): # False to not destroy player
                    laser.kill() # Destroy laser once it hits the block
                    self.lives -= 1

                    if self.lives <= 0: # End game when out of lives.
                        pygame.quit()
                        sys.exit()

        ## Aliens
        if self.aliens:
            for alien in self.aliens:
                ## If alien collides with block, destroy the block.
                pygame.sprite.spritecollide(alien, self.blocks, True)

                ## If alien collides with block, destroy the player.
                if pygame.sprite.spritecollide(alien, self.player, True):
                    pygame.quit()

    def display_lives(self):
        for lives in range(self.lives - 1):
            x = self.lives_x_start_pos + (lives * (self.lives_surf.get_size()[0] + 10)) # offset of 10
            screen.blit(self.lives_surf, (x, 8))

    def display_score(self):
        score_surface = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft = (10, -10))
        screen.blit(score_surface, score_rect)

    def victory_screen(self):
        if not self.aliens.sprites(): # If there are no more aliens in the aliens group
            victory_surface = self.font.render('YOU WIN!', False, 'White')
            victory_rect = victory_surface.get_rect(center = (screen_width/2, screen_height/2))
            screen.blit(victory_surface, victory_rect)

    def run(self):
        ## Updates and draw all sprite groups.
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()
        
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_screen()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        ## Scale image to match dimensions of screen (if it changes)
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)

        for line in range(line_amount):
            ## Multiply current line by height of each line.
            y_pos = line * line_height
            ## Draw on self.tv instead of screen because the opacity for the lines 
            ## and for the TV will be the same.
            pygame.draw.line(self.tv, 'purple', 
                            (0, y_pos), (screen_width, y_pos), 1) # surface, color, start, end, width

    def draw(self):
        ## Lowering opacity (to fix vignetting issue)
        self.tv.set_alpha(randint(75, 90)) # Flickering effect
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))

# Using this if statement because due to working with multiple files,
# there is a chance to execute code that is not actually intended to run, so
# this if statement prevents that entirely. The statement allows you to execute
# code when the file runs as a script, but not when it's imported as a 
# module. It's useful if you want to write Python code which is intended to be "imported"
# but can also be run as a standalone shell script. The code under this statement only
# gets executed if you run the file directly.
if __name__ == '__main__':
    pygame.init()
    
    ## Global Variables
    screen_width = 600 # 800
    screen_height = 600 # 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game() # Creates instance of game.
    crt = CRT()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800) # One laser shot (from alien) every 800 milliseconds.

    while True:
        ## Handling inputs
        for event in pygame.event.get():
            ## pygame user inputs are all CAPITALIZED
            ## "\" is used for new line
            if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        
        screen.fill((30, 30, 30))
        game.run() # Runs the game.
        crt.draw()

        pygame.display.flip()
        clock.tick(60)