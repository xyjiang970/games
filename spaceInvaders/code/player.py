# Player Requirements:
# 1. Show image of the player.
# 2. Move the player.
# 3. Constrain player to the window.
# 4. Shoot a laser & recharge.

import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        ## super.__init__() is a way to call the __init__ method of a parent class in Python.
        ## The super() function returns a temp. object of the superclass, which allows you to 
        ## call its methods. this can be useful when you want to extend the functionality of 
        ## a previously build class without having to rewrite its methods in your subclass.
        ## For example:
        ##
        ## class Animal:
        ##     def __init__(self, name):
        ##         self.name = name
        ##
        ## class Dog(Animal):
        ##     def __init__(self, name, breed):
        ##         super().__init__(name)
        ##         self.breed = breed
        super().__init__()

        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0 
        self.laser_cooldown = 500 # Shoot laser every 600 milliseconds.

        self.lasers = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.05)

    def get_input(self):
        """
        Checks different keys being pressed.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            ## Laser will need a timer otherwise player can hold down key and shoot forever.
            self.ready = False
            self.laser_time = pygame.time.get_ticks() # Measure time since game has started (only used once).
            self.laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks() # Being run continuously (multiple times).
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0: # left side
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint: # right side
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
        
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()