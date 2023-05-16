import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)] # store all the Vector2s that create the snake
        self.direction = Vector2(1, 0)

    ## Method that draws snake
    def draw_snake(self):
        for block in self.body: # cycles through Vectors
            ## Create a rectangle from position and then
            ## draw the rectangle.
            ## Rect(x, y, w, h)
            block_rect = pygame.Rect(
                                     int(block.x * cell_size), # Getting values from a vector results in floats
                                     int(block.y * cell_size), # Getting values from a vector results in floats
                                     cell_size, cell_size
                                    )
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        ## Copy entire body, but remove the last item.
        ## Then, add one more element in front (which is 
        ## the first element of the previous list + direction
        ## desired to move to) - that way the entire snake moves.
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:] # this is the body we are going to draw

class FRUIT:
    def __init__(self):
        ## Create an x and y position
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
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

# MAIN class will contain entire game logic (+ snake and fruit object)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

pygame.init()
cell_size = 40 
cell_number = 20 
screen = pygame.display.set_mode((cell_number * cell_size, 
                                  cell_number * cell_size)
                                )
clock = pygame.time.Clock()

# Events are capitalized in pygame by convention
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150) # how often we want to trigger=150 milliseconds

main_game = MAIN()

while True: 
    ## Handling inputs
    for event in pygame.event.get():
        ## pygame user inputs are all CAPITALIZED
        ## "\" is used for new line
        if event.type == pygame.QUIT or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # up key
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT: # right key
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN: # down key
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT: # left key
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)