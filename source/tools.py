# tools and control the process of the game
import os
import pygame, sys
from .states import main_menu
from .states import settings


class Game:
    def __init__(self, state_dict, start_state):
        self.mouse_x, self.mouse_y = (0, 0)
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    # judge whether it's the next state
    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)
        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            # pause function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.K_LEFT:
                    self.keys = pygame.key.get_pressed()
                # button's keys
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.keys = pygame.key.get_pressed()

                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    self.mouse_x = pos[0]
                    self.mouse_y = pos[1]
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.keys = pygame.key.get_pressed()
            # try:
            self.update()
            pygame.display.update()
            # except:
            #    pass
            # set frame rate
            self.clock.tick(120)


# loading graphics,accept the pictures' path and extension
def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(path):
        # import operating system dictionary to spilt file name and extension
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            # convert to transparent layer format
            if img.get_alpha():
                img = img.convert_alpha()
            # convert to common layer format
            else:
                img = img.convert()
        graphics[name] = img
    return graphics


# sheet is the pitcure that imports,followed with the position to the screen,underpainting color and amplify scale
def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pygame.Surface((width, height))
    # which position to draw the image
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image


def load_musics(path, times=1):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(times)


def load_sounds(path, volume):
    # this argument 0 represents 1 time, f**k I tried many times,holy shit it is!!!
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    sound.play(0)


def get_music(sheet):
    return sheet
