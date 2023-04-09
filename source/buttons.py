import pygame
from . import tools
from . import constants as C

class Buttons(pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.finished = False
        self.button_width, self.button_height = 0, 0
        self.image = ()

    # these code create buttons and justify cursor to click the buttons
    # image,x,y is which button image in screen
    def get_button(image):
        width, height = image.get_rect().size
        image.x, image.y = width, height
        button = pygame.Surface((width, height))
        button.blit(image, (0, 0, width, height))
        return button

    def get_button_image(self, sheet, x, y, width, height, colorkey, scale):
        self.button_width, self.button_height = width, height
        self.image = pygame.Surface((width, height))
        # which position to draw the image
        self.image.blit(self.image, (0, 0), (x, y, width, height))
        self.image.set_colorkey(colorkey)
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        return self.image

def button_pressed(img):
    changed_width, changed_height = img.get_rect().size
    image = pygame.Surface((changed_width, changed_height))
    image.blit(img, (0, 0), (0, 0, changed_width, changed_height))
    image = pygame.transform.scale(img, (int(changed_width * 0.9), int(changed_height *0.9)))
    return image



