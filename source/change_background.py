import pygame
from . import tools
from . import constants as C


def changing(timer, img):
    changed_width, changed_height = img.get_rect().size
    image = pygame.Surface((changed_width / 2, changed_height / 2))
    image.blit(img, (0, 0), (0, 0, changed_width / 4, changed_height / 4))
    image = pygame.transform.scale(img, (int(changed_width * 1), int(changed_height * 1)))
    return image
