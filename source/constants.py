import pygame
from . import setup

# setup the full screen
# SCREEN_W, SCREEN_H = setup.infoObject.current_w, setup.infoObject.current_h
SCREEN_W, SCREEN_H = 800, 600
SCREEN_SIZE = (SCREEN_W, SCREEN_H)
# NBG_MULTI is the proportion to change graphics to the screen
BG_MULTI = 2.68
BG_MULTI2 = 2.67889447
NBG_MULTI = 800 / 1980
PLAYER_MUNTI = 2.9
MONSTER_MULTI = 2.5
GRAVITY = 0.2
GROUND_HEIGHT = SCREEN_H / 256 * 127
ENEMY_SPEED = 1
BRICK_MULTI = 2.69
# a font
FONT = 'arial'
