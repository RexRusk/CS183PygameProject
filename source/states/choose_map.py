import pygame
from .. import setup, tools
from .. import constants as C
from ..components import info


class ChoseMap:
    def start(self, game_info):
        self.finished = False
        self.next = 'load_screen'
        self.setup_background()
        self.setup_buttons()
        self.game_info = game_info
        self.info = info.Info('chose_map', game_info)

    def setup_background(self):
        self.background = setup.GRAPHICS['switch_map']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width),
                                                                   int(rect.height)))
        self.background_rect = self.background.get_rect()

    def setup_buttons(self):
        # loose mouse click,fix bug
        self.loose = False
        self.back_button = tools.get_image(setup.GRAPHICS['Iconic2048x2048'], 141, 1106, 140, 140, (0, 0, 0),
                                           C.NBG_MULTI)

    def update_buttons(self, keys):
        x, y = pygame.mouse.get_pos()
        pressed_array = pygame.mouse.get_pressed()
        if not pressed_array[0]:
            self.loose = True
        # switch levels
        if self.loose == True:
            if pressed_array[0] \
                    and y < C.SCREEN_H / 3:
                self.game_info['level'] = 0
                self.finished = True
            elif pressed_array[0] \
                    and C.SCREEN_H * 1 / 3 < y < C.SCREEN_H * 2 / 3:
                self.game_info['level'] = 1
                self.finished = True


            elif pressed_array[0] \
                    and C.SCREEN_H * 2 / 3 < y < C.SCREEN_H \
                    and not (
                    C.SCREEN_W / 8 - 35 <= x <= C.SCREEN_W / 2 + 35 and C.SCREEN_H * 7 / 8 - 35 <= y <= C.SCREEN_H * 7 / 8 + 35):
                self.game_info['level'] = 2
                self.finished = True

            # back button
            elif pressed_array[0] \
                    and C.SCREEN_W / 8 - 35 <= x <= C.SCREEN_W / 2 + 35 \
                    and C.SCREEN_H * 7 / 8 - 35 <= y <= C.SCREEN_H * 7 / 8 + 35:
                self.next = 'main_menu'
                self.finished = True

    def update(self, surface, keys):
        self.game_info.update()
        self.update_buttons(keys)
        self.draw(surface)

    def draw(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.background, (0, 0))
        surface.blit(self.back_button, (C.SCREEN_W / 8 - self.back_button.get_rect().size[0] / 2,
                                        C.SCREEN_H * 7 / 8 - self.back_button.get_rect().size[1] / 2))
        self.info.update()
        self.info.draw(surface)
