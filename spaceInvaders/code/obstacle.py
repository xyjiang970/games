import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
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
        
        self.image = pygame.Surface((size, size)) # Square
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))

# A block will be created wherever there is an 'x'.
# The obstacle consists of individual blocks and each of the blocks is a sprite. 
# All sprites are arranged in a way to look like an obstacle (couple of square shaped sprites 
# in a certain shape). The obstacle is just a list with strings inside of it.
shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']