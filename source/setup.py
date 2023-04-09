import pygame
from . import constants as C
from . import tools

pygame.init()
#transformed screen
#infoObject = pygame.display.Info()
#SCREEN = pygame.display.set_mode((int(infoObject.current_w), int(infoObject.current_h)))
SCREEN = pygame.display.set_mode((800, 600))
#loading graphics
GRAPHICS = tools.load_graphics('resources/graphics')
GUI = tools.load_graphics('Free Platform Game Assets/GUI ( Update 1.7 )/png')
MAP1_BG = tools.load_graphics('Free Platform Game Assets/Backgrounds/New Background ( Update 1.9 )/png/1920x1080/background')
