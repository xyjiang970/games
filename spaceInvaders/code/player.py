# Player Requirements:
# 1. Show image of the player.
# 2. Move the player.
# 3. Constrain player to the window.
# 4. Shoot a laser & recharge.

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
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