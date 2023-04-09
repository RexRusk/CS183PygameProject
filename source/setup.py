import pygame
from . import constants as C
from . import tools

pygame.init()
# transformed screen
# infoObject = pygame.display.Info()
# SCREEN = pygame.display.set_mode((int(infoObject.current_w), int(infoObject.current_h)))
SCREEN = pygame.display.set_mode((800, 600))
# loading graphics
GRAPHICS = tools.load_graphics('resources/graphics')
GUI = tools.load_graphics('resources/graphics')
