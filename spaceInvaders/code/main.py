import pygame, sys
from player import Player

class Game:
    def __init__(self):
        """
        Initiate method of a class (equivalent to C++ constructor). The __init__ function is called
        every time an object is created from a class. The __init__ method lets the class initialize
        the object's attributes and serves no other purpose.

        Sprite groups will be added here (player, aliens, etc).
        """
        player_sprite = Player((300, 300))
        self.player = pygame.sprite.GroupSingle(player_sprite)
    
    def run(self):
        """
        Update and draw all sprite groups.
        """
        self.player.draw(screen)

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