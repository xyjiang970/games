import pygame, sys, random

# Restart ball if it hits left or right side
def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    ## time we are on right now
    current_time = pygame.time.get_ticks()

    ball.center = (screen_width/2, screen_height/2)

    ## counter timer display
    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, 
                                   # positive y values if you want to go DOWN
                                   screen_height/2 + 50) 
                    )
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width/2 - 10, 
                                   screen_height/2 + 50) 
                    )
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width/2 - 10, 
                                   screen_height/2 + 50) 
                    )

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ## randomizes direction
        ball_speed_y = ball_speed * random.choice((1, -1))
        ball_speed_x = ball_speed * random.choice((1, -1))
        score_time = None


# Ball animation function
def ball_animation():
    global ball_speed_x, ball_speed_y, \
           player_score, opponent_score, score_time
    ## Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    ## If ball hits screen
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # When you use two `if` statements, both conditions will be tested 
    # and the code blocks for both `if` statements will be executed if 
    # their respective conditions are `True`. However, when you use an 
    # `if` statement followed by an `elif` statement, the condition 
    # for the `elif` statement will only be tested if the condition for 
    # the `if` statement is False. If the condition for the `if` statement 
    # is `True`, the code block for the `if` statement will be executed 
    # and the code block for the `elif` statement will be skipped.

    ## player score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks() # only running once
        player_score += 1
        ## Give us an interger that tells us for how long the game
        ## has been running since it was started (or more specifically-
        ## since pygame.init() method was called).
    ## opponent score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks() # only running once
        opponent_score += 1

    # If ball collides with player & opponent
    ## checks if collision has occured (player)
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        ## checks what side the collision has occured
        if abs(ball.right - player.left) < 10: # 10 is tolerance for wiggle room
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and (ball_speed_y > 0):
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and (ball_speed_y < 0):
            ball_speed_y *= -1
    ## checks if collision has occured (opponent)
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and (ball_speed_y > 0):
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and (ball_speed_y < 0):
            ball_speed_y *= -1


# Player animation function
def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


# Opponent (computer) animation
def opponent_animation(): 
    if opponent.centery < ball.y:
        opponent.centery += opponent_speed
    if opponent.centery > ball.y:
        opponent.centery -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height



# General setup
pygame.mixer.pre_init(44100, -16, 2, 512) # 512 is the buffer size (default: 4096)
pygame.init() # initiates all pygame modules
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1024 # 1280 # 1024
screen_height = 768 # 960  # 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
bg_color = pygame.Color('#2F373F') # color object
light_grey = (200, 200, 200) # r,g,b

# Game Rectangles
# Origin of the window (x,y) starts at the top left,
# if you want to go down you need to INCREASE y.
## .Rect(width, height, x, y)
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Speed variables
ball_speed = 6
ball_speed_x = ball_speed * random.choice((1, -1)) # random dir. at BEGINNING of game
ball_speed_y = ball_speed * random.choice((1, -1)) # random dir. at BEGINNING of game
player_speed = 0
opponent_speed = 7.5

# Text Variables
player_score = 0
opponent_score = 0
## this font should come with every computer
## .Font(font, size)
game_font = pygame.font.Font("freesansbold.ttf", 25)

# Sound
pong_sound = pygame.mixer.Sound("./sounds/pong.ogg")
score_sound = pygame.mixer.Sound("./sounds/score.ogg")

# Score Timer
score_time = True

# Checkes if the user has pressed the close button 
# at the top of the window.
while True: 
    ## Handling inputs
    for event in pygame.event.get():
        ## pygame user inputs are all CAPITALIZED
        ## "\" is used for new line
        if event.type == pygame.QUIT or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            pygame.quit()
            sys.exit()
        ## key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 5
            if event.key == pygame.K_UP:
                player_speed -= 5
        ## key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 5
            if event.key == pygame.K_UP:
                player_speed += 5

    # Game logic: calling functions
    ball_animation()
    player_animation()
    opponent_animation()

    # Visuals
    # Order matters here - successive elements in the loop are drawn
    # on top of each other (so the first element called in the code
    # will be at the bottom of the frame, and the last one will be at
    # the top).
    screen.fill(bg_color) # drawn first (bottom)
    ## .draw(surface, color, rect)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    
    # Instead of filling the whole rectangle, it uses its frame to draw
    # an ellipse into it. Since all sides are the same length this becomes
    # a circle. 
    pygame.draw.ellipse(screen, light_grey, ball)
    
    # Four arguments needed for aaline:
    # surface to draw on, color, tuple of the start point,
    # and tuple of the end point.
    pygame.draw.aaline(screen, light_grey, 
                        (screen_width/2, 0), 
                        (screen_width/2, screen_height)
                      ) # drawn last (top)

    if score_time:
        ball_start()

    ## display surface for text (player)
    player_text = game_font.render(f"{player_score}", False, light_grey)
    ## putting text surface on main surface
    screen.blit(player_text, 
                (screen_width/2 + 27, screen_height/2)
               ) # blit puts one surface on another | (660,470)
    ## display surface for text (opponent)
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    ## putting text surface on main surface
    screen.blit(opponent_text, 
                (screen_width/2 - 43, screen_height/2)
               ) # blit puts one surface on another | (660,470)

    # Updating the window
    # Entire display.flip() method takes everything that came 
    # before it and draw a picture from that.
    pygame.display.flip()
    # Limits how fast the loop runs (60x per second).
    # If you don't control the speed the computer might just try
    # to run it at 10,000 cycles per second and you won't
    # be able to see anything.
    clock.tick(60)