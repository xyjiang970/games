# Imports
import pygame, sys, random
from pygame.math import Vector2

#################################################################################################################
# Classes
class SNAKE:
    def __init__(self):
        ## store all the Vector2s that create the snake
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] 
        
        self.direction = Vector2(0, 0)

        ## New block attribute.
        self.new_block = False

        ## All possible head positions.
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        ## All possible tail positions.
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        ## All possible body positional directions.
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        ## All possible CURVED body positions (corners).
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha() # tr = topRight
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha() # tl = topLeft
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha() # br = bottomRight
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha() # bl = bottomLeft

        ## Sound effect when eating food.
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    ## Method that draws snake
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        ## Enumerate gives us an index on what object we are inside of our list.
        ## Index is the INDEX we are on, and block is the ACTUAL OBJECT that we are going to look at.
        for index, block in enumerate(self.body):
            ## 1. Still need rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)            
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            ## 2. What direction is the face heading? 
            if index == 0: # head is always the first element.
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                ## Horizontal and Vertical body parts
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)

                else:
                    ## Total of 4 different corners
                    ## Left+Up and Down+Right will use the same corner, etc etc

                    ### Top Left Body Corner
                    if (previous_block.x == -1 and next_block.y == -1) or \
                        (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect) 
                    ### Bottom Left Body Corner
                    elif (previous_block.x == -1 and next_block.y == 1) or \
                        (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect) 
                    ### Top Right Body Corner
                    elif (previous_block.x == 1 and next_block.y == -1) or \
                        (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect) 
                    ### Bottom Right Body Corner
                    elif (previous_block.x == 1 and next_block.y == 1) or \
                        (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect) 

        ## Old Block Body Code:
        # for block in self.body: # cycles through Vectors
        #     ## Create a rectangle from position and then
        #     ## draw the rectangle.
        #     ## Rect(x, y, w, h)
        #     block_rect = pygame.Rect(
        #                              int(block.x * cell_size), # Getting values from a vector results in floats
        #                              int(block.y * cell_size), # Getting values from a vector results in floats
        #                              cell_size, cell_size
        #                             )
        #     pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): # if head is to the left of next block
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): 
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:] # this is the body we are going to draw
            self.new_block = False
        else:
            ## Copy entire body, but remove the last item.
            ## Then, add one more element in front (which is 
            ## the first element of the previous list + direction
            ## desired to move to) - that way the entire snake moves.
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:] # this is the body we are going to draw

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0) # snake moves (starts) in direction of direction key pressed

class FRUIT:
    def __init__(self):
        ## Calling randomize
        self.randomize()
        
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
        screen.blit(apple, fruit_rect)
        ## Drawing the rectangle
        ## pygame.draw.rect(surface, color, rectangle).
        #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        ## An efficient way of working with & storing two-dimensional data
        ## is by using the Vector2D to control x, y conordinates rather 
        ## than using lists.
            ### Since we imported Vector2 from pygame.math we dont need to repeatedly
            ### type pygame.math.Vector2()
        self.pos = Vector2(self.x, self.y)

# MAIN class will contain entire game logic (+ snake and fruit object)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        ## If fruit position is same as first block of snake.
        if self.fruit.pos == self.snake.body[0]:
            ## Reposition fruit.
            self.fruit.randomize()
            ## Add another block to the snake.
            self.snake.add_block()
            ## Crunch sound.
            self.snake.play_crunch_sound()
        ## Ensures fruit does not end up on snake body - 
        ## everytime the fruit is drawn behind the snake body, randomize it elsewhere.
        for block in self.snake.body[1:]: # everything after the head
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        ## Checks if snake is outside of the screen.
        if (not 0 <= self.snake.body[0].x < cell_number) or \
            (not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()

        ## Checks if snake hits itself.
        for block in self.snake.body[1:]: # only the elements that come after the head
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        ## cycle through each line and draw a slighly darker green rectangle if we have
        ## an odd or an even number.
        grass_color = (167, 209, 61) # dark greenish color

        ## Vertical axis of entire field
        for row in range(cell_number):
            if row%2 == 0:
                ## Horizontal axis of entire field
                for col in range(cell_number):
                    if col%2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, 
                                                 row * cell_size, 
                                                 cell_size, 
                                                 cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                ## Horizontal axis of entire field
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, 
                                                 row * cell_size, 
                                                 cell_size, 
                                                 cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        ## The longer the snake body, the higher the score
        score_text = str(len(self.snake.body) - 3) # Initially starting with 3 blocks.
        ## .render(text, anti-aliasing, color)
        ## Setting anti-aliasing to True so the text is a bit smoother.
        ## Unless working with pixel art or a really slow computer, it's best to leave
        ## aa as True.
        score_surface = game_font.render(score_text, True, (56, 74, 12))

        ## Puttng score text on screen
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, 
                              apple_rect.top, 
                              apple_rect.width + score_rect.width + 6, 
                              apple_rect.height)
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)

        screen.blit(score_surface, score_rect) # Bottom right position of game screen.
        ## Draw apple next to score (slightly to left)
        screen.blit(apple, apple_rect)

        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2) # frame (# determines line width)

#################################################################################################################
# Global Variables
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40 
cell_number = 20 
screen = pygame.display.set_mode((cell_number * cell_size, 
                                  cell_number * cell_size)
                                )
clock = pygame.time.Clock()
# convert_alpha converts image into a format that pygame can work with easier.
apple = pygame.image.load('Graphics/apple.png').convert_alpha() 
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25) # font, font size


#################################################################################################################
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

        ## Key Presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # up key
                ## Cannot allow snake to reverse itself or else it dies (hits itself).
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT: # right key
                ## Cannot allow snake to reverse itself or else it dies (hits itself).
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN: # down key
                ## Cannot allow snake to reverse itself or else it dies (hits itself).
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT: # left key
                ## Cannot allow snake to reverse itself or else it dies (hits itself).
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)