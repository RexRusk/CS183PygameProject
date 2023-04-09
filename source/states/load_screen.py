from ..components import info
from .. import tools, setup
from .. import constants as C
import pygame


class LoadScreen:
    def start(self, game_info):
        self.game_info = game_info
        self.setup_background()
        self.finished = False
        self.next = 'level'
        self.duration = 2000
        self.timer = 0
        self.info = info.Info('load_screen', self.game_info)

    def setup_background(self):
        self.background = setup.GRAPHICS['Sky_8_6']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width),
                                                                   int(self.background_rect.height)))
        self.viweport = setup.SCREEN.get_rect()

    def update(self, surface, keys):
        self.draw(surface)

        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        # next state is black screen
        # surface.fill((0, 0, 0))
        surface.blit(self.background, self.viweport)
        self.info.draw(surface)


class GameOver(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.setup_background()
        self.finished = False

        self.next = 'main_menu'
        self.duration = 4000
        self.timer = 0
        self.info = info.Info('game_over', self.game_info)

    def setup_background(self):
        self.background = setup.GRAPHICS['Sky_8_6']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width),
                                                                   int(self.background_rect.height)))
        self.viweport = setup.SCREEN.get_rect()

    def update(self, surface, keys):
        self.draw(surface)

        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        # next state is black screen
        # surface.fill((0, 0, 0))
        surface.blit(self.background, self.viweport)
        self.info.draw(surface)
