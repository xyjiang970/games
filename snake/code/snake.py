import pygame, sys
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        ## Create an x and y position
        self.x = 5
        self.y = 4
        ## An efficient way of working with & storing two-dimensional data
        ## is by using the Vector2D to control x, y conordinates rather 
        ## than using lists.
            ### Since we imported Vector2 from pygame.math we dont need to repeatedly
            ### type pygame.math.Vector2()
        self.pos = Vector2(self.x, self.y)
        
        ## draw a square
    
    def draw_fruit(self):
        ## Create a rectangle
        ## Rect(x, y, w, h)
        ## Take each object pixel (self.pos.x, self.pos.y) and multiply it by 
        ## cell_size to create the illusion of a grid.
        fruit_rect = pygame.Rect(
                                 int(self.pos.x * cell_size), # Getting values from a vector results in floats
                                 int(self.pos.y * cell_size), # Getting values from a vector results in floats
                                 cell_size, cell_size
                                )
        ## Drawing the rectangle
        ## pygame.draw.rect(surface, color, rectangle)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

pygame.init()
cell_size = 40 
cell_number = 20 
screen = pygame.display.set_mode((cell_number*cell_size, 
                                  cell_number*cell_size
                                 )
                                )
clock = pygame.time.Clock()

fruit = FRUIT()

while True: 
    ## Handling inputs
    for event in pygame.event.get():
        ## pygame user inputs are all CAPITALIZED
        ## "\" is used for new line
        if event.type == pygame.QUIT or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            pygame.quit()
            sys.exit()

    screen.fill((175, 215, 70))

    fruit.draw_fruit()

    pygame.display.update()
    clock.tick(60)