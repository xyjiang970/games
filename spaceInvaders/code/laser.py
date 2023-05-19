# Sprite class with a position and speed. 
# 1. Spawn at player position and move up.
# 2. Spawn at alien position and move down.

import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
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
        
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        """
        Lasers never disappear even if they leave the screen. Need to destroy them.
        """
        if (self.rect.y <= -50) or (self.rect.y >= self.height_y_constraint + 50):
            self.kill()

    def update(self):
        ## move laser up by a certain speed (+= because we set negative value for speed in __init__)
        self.rect.y += self.speed 
        self.destroy()
