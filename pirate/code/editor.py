import pygame
from settings import *

class Editor:
    def __init__(self):
        ## Main Setup
        ### Allows us to draw on the display surface (so what the player sees right away).
        self.display_surface = pygame.display.get_surface()
    
    def run(self, dt):
        self.display_surface.fill('white')