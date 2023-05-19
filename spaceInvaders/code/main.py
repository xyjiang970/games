import pygame, sys
from player import Player
import obstacle

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

        ## Obstacle Setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.create_obstacle(40, 480)

    def create_obstacle(self, x_start, y_start):
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
                   x = x_start + (col_index * self.block_size)
                   y = y_start + (row_index * self.block_size)
                   block = obstacle.Block(self.block_size, 
                                         (241,79,80), x, y)
                   self.blocks.add(block)
    
    def run(self):
        ## Updates and draw all sprite groups.
        self.player.update()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)

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
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game() # Creates instance of game.

    while True:
        ## Handling inputs
        for event in pygame.event.get():
            ## pygame user inputs are all CAPITALIZED
            ## "\" is used for new line
            if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                pygame.quit()
                sys.exit()
        
        screen.fill((30, 30, 30))
        game.run() # Runs the game.

        pygame.display.flip()
        clock.tick(60)