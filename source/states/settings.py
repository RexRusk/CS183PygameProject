import pygame
from .. import setup, tools, buttons
from .. import constants as C
from ..components import info


class Settings:
    def start(self, game_info):
        self.finished = False
        self.next = 'main_menu'
        self.setup_background()
        self.setup_buttons()
        self.info = info.Info('settings', game_info)
        self.setup_musics()
        self.a = 0
        self.b = 0
        self.c = 0
        self.game_info = game_info

    def setup_background(self):
        self.background = setup.GRAPHICS['Background_8_6']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width),
                                                                   int(rect.height)))
        self.background_rect = self.background.get_rect()

    def setup_musics(self):
        tools.load_musics('resources/music/Happy_BGM.mp3')

    def setup_buttons(self):
        self.back_button = tools.get_image(setup.GUI['Empty1024x1024'], 477, 585, 525, 136, (0, 0, 0), C.NBG_MULTI)
        self.BG_button = tools.get_image(setup.GUI['Empty1024x1024'], 477, 585, 525, 136, (0, 0, 0), C.NBG_MULTI)
        self.ball_button = tools.get_image(setup.GRAPHICS['Iconic2048x2048'], 139, 69, 140, 140, (0, 0, 0), C.NBG_MULTI)
        # bug fix
        self.hold = False
        self.ini_x, self.ini_y = C.SCREEN_W / 2 - 35, C.SCREEN_H / 2 - 35
        self.x, self.y = C.SCREEN_W / 2, C.SCREEN_H / 2

    def update_buttons(self, game_info):
        x, y = pygame.mouse.get_pos()
        pressed_array = pygame.mouse.get_pressed()
        # back button
        if pressed_array[0] \
                and x >= C.SCREEN_W / 8 - 105.9 \
                and x <= C.SCREEN_W / 8 + 105.9 \
                and y >= C.SCREEN_H * 7 / 8 - 27.5 \
                and y <= C.SCREEN_H * 7 / 8 + 27.5:
            self.finished = True
        if self.a % 2 == 0 \
                and x >= C.SCREEN_W / 8 - 105.9 \
                and x <= C.SCREEN_W / 8 + 105.9 \
                and y >= C.SCREEN_H * 7 / 8 - 27.5 \
                and y <= C.SCREEN_H * 7 / 8 + 27.5:
            self.back_button = buttons.button_pressed(self.back_button)
            self.a = 1
        if not (x >= C.SCREEN_W / 8 - 105.9 \
                and x <= C.SCREEN_W / 8 + 105.9 \
                and y >= C.SCREEN_H * 7 / 8 - 27.5 \
                and y <= C.SCREEN_H * 7 / 8 + 27.5):
            self.back_button = tools.get_image(setup.GUI['Empty1024x1024'], 477, 585, 525, 136, (0, 0, 0), C.NBG_MULTI)
            self.a = 0

        # BG button
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        if pressed_array[
            0] and C.SCREEN_W / 2 - 105.9 <= self.x <= C.SCREEN_W / 2 + 105.9 and C.SCREEN_H / 2 - 27.5 <= self.y <= C.SCREEN_H / 2 + 27.5:
            self.game_info['volume'] = (self.x - (C.SCREEN_W / 2 - 105.9)) / 211.8
            pygame.mixer.music.set_volume(self.game_info['volume'])

    def update(self, surface, keys):
        self.update_buttons(self.game_info)
        self.draw(surface)

    def draw(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.background, (0, 0))
        surface.blit(self.back_button, (C.SCREEN_W / 8 - self.back_button.get_rect().size[0] / 2,
                                        C.SCREEN_H * 7 / 8 - self.back_button.get_rect().size[1] / 2))
        surface.blit(self.BG_button, (C.SCREEN_W / 2 - self.BG_button.get_rect().size[0] / 2,
                                      C.SCREEN_H / 2 - self.BG_button.get_rect().size[1] / 2))
        if self.ini_x < C.SCREEN_W / 2 - 105.9: self.ini_x = C.SCREEN_W / 2 - 105.9
        if self.ini_x > C.SCREEN_W / 2 + 90: self.ini_x = C.SCREEN_W / 2 + 90
        if self.x < C.SCREEN_W / 2 - 105.9: self.x = C.SCREEN_W / 2 - 105.9
        if self.x > C.SCREEN_W / 2 + 90: self.x = C.SCREEN_W / 2 + 90

        if pygame.mouse.get_pressed()[
            0] and C.SCREEN_W / 2 - 105.9 <= self.x <= C.SCREEN_W / 2 + 105.9 and C.SCREEN_H / 2 - 27.5 <= self.y <= C.SCREEN_H / 2 + 27.5:
            self.hold = True
        if self.hold == True and pygame.mouse.get_pressed()[0]:
            surface.blit(self.ball_button, (self.x - 35, C.SCREEN_H / 2 - 35))
        if not pygame.mouse.get_pressed()[0] and self.hold == True:
            self.ini_x, self.ini_y = self.x - 35, C.SCREEN_H / 2 - 35
            self.hold = False
        if self.hold == False:
            surface.blit(self.ball_button, (self.ini_x, self.ini_y))
        self.info.update()
        self.info.draw(surface)
