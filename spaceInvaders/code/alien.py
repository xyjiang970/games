import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
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

        filepath = 'graphics/' + color + '.png'
        self.image = pygame.image.load(filepath).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        else: self.value = 300 # Yellow aliens at top.

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
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

        self.image = pygame.image.load('graphics/extra.png').convert_alpha() 

        ## Extra alien is supposed to either come in from the left and go to the right,
        ## or come in from the right and go to the left.
        if side == 'right':
            x = screen_width + 50 # 50 pixels for wiggle room
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        ## Either spawn the extra alien on the left or right side of the screen depending
        ## on what is specified for "side" argument.
        self.rect = self.image.get_rect(topleft = (x, 80))

    def update(self):
        self.rect.x += self.speed