import pygame
from .. import constants as C
from . import coin
from .. import setup, tools

pygame.font.init()


class Info:
    def __init__(self, state, game_info):
        self.state = state
        self.game_info = game_info
        self.create_state_lables()
        self.create_info_lables()
        # self.flash_coin = coin.FlashingCoins()

        # initial timer for recording time

    # state provides different information to deffent levels
    def create_state_lables(self):
        # all lable are in center mode!
        self.state_lables = []
        if self.state == 'main_menu':
            self.state_lables.append(
                (self.create_lable('BRIEF MARIO', int(C.SCREEN_W / 16), (0, 0, 0)), C.SCREEN_W / 2, C.SCREEN_H / 4))
            self.state_lables.append((self.create_lable('play'), C.SCREEN_W / 2, C.SCREEN_H / 2))
            self.state_lables.append((self.create_lable('settings'), C.SCREEN_W / 2, C.SCREEN_H / 8 * 5))
            self.state_lables.append((self.create_lable('quit'), C.SCREEN_W / 2, C.SCREEN_H / 4 * 3))
        elif self.state == 'chose_map':
            self.state_lables.append((self.create_lable('MAP1'), C.SCREEN_W / 2, C.SCREEN_H / 4))
            self.state_lables.append((self.create_lable('MAP2'), C.SCREEN_W / 2, C.SCREEN_H / 2))
            self.state_lables.append((self.create_lable('MAP3'), C.SCREEN_W / 2, C.SCREEN_H / 4 * 3))
            # self.state_lables.append((self.create_lable('back'), C.SCREEN_W / 8, C.SCREEN_H * 7 / 8))

        elif self.state == 'load_screen':
            if self.game_info['player_state'] == 'not_complete':
                self.state_lables.append((self.create_lable('loading...'), C.SCREEN_W / 2, C.SCREEN_H / 2))
                self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0),
                                                    C.BG_MULTI)
            else:
                self.state_lables.append((self.create_lable('completed!'), C.SCREEN_W / 2, C.SCREEN_H / 2))
        elif self.state == 'game_over':
            self.state_lables.append((self.create_lable('GAME OVER'), C.SCREEN_W / 2, C.SCREEN_H / 2))
        elif self.state == 'settings':
            self.state_lables.append(
                (self.create_lable('BG Music', int(C.SCREEN_W / 24)), C.SCREEN_W / 2, C.SCREEN_H / 8 * 3))
            self.state_lables.append(
                (self.create_lable('Back', int(C.SCREEN_W / 24)), C.SCREEN_W / 8, C.SCREEN_H * 7 / 8))
        elif self.state == 'level':
            if self.game_info['level'] != 1:
                self.state_lables.append((self.create_lable('SCORE      {}'.format(self.game_info['score']),
                                                            int(C.SCREEN_W / 36), (0, 0, 0)), C.SCREEN_W / 8,
                                            C.SCREEN_H / 8))
                self.state_lables.append((self.create_lable('COIN      {}'.format(self.game_info['coin']),
                                                            int(C.SCREEN_W / 36), (0, 0, 0)), C.SCREEN_W / 8 * 3,
                                        C.SCREEN_H / 8))
                self.state_lables.append((self.create_lable('LIVES      {}'.format(self.game_info['lives']),
                                                            int(C.SCREEN_W / 36), (0, 0, 0)), C.SCREEN_W / 8 * 5,
                                          C.SCREEN_H / 8))
            if self.game_info['level'] == 1:
                self.state_lables.append((self.create_lable('SCORE      {}'.format(self.game_info['score']),
                                                            int(C.SCREEN_W / 36), (255, 255, 255)), C.SCREEN_W / 8,
                                          C.SCREEN_H / 8))
                self.state_lables.append((self.create_lable('COIN      {}'.format(self.game_info['coin']),
                                                            int(C.SCREEN_W / 36), (255, 255, 255)), C.SCREEN_W / 8 * 3,
                                          C.SCREEN_H / 8))
                self.state_lables.append((self.create_lable('LIVES      {}'.format(self.game_info['lives']),
                                                            int(C.SCREEN_W / 36), (255, 255, 255)), C.SCREEN_W / 8 * 5,
                                          C.SCREEN_H / 8))
            died = 0
            # initial time
            if self.game_info['re_game'] == 1:
                time = self.game_info['time']
                self.game_info['time'] = 0
                died = 1
                self.game_info['re_game'] = 0
            if died == 0:
                self.game_info['time'] = int((pygame.time.get_ticks()) / 1000)
                if self.game_info['level'] != 1:
                    self.state_lables.append((self.create_lable('TIME      {}'.format(self.game_info['time']),
                                                                int(C.SCREEN_W / 36), (0, 0, 0)),
                                              C.SCREEN_W / 8 * 3, C.SCREEN_H / 16 * 3))
                if self.game_info['level'] == 1:
                    self.state_lables.append((self.create_lable('TIME      {}'.format(self.game_info['time']),
                                                                int(C.SCREEN_W / 36), (255, 255, 255)),
                                              C.SCREEN_W / 8 * 3, C.SCREEN_H / 16 * 3))
            else:
                timer = pygame.time.get_ticks() - time
                self.game_info['time'] = int(timer / 1000)
                if self.game_info['level'] != 1:
                    self.state_lables.append((self.create_lable('TIME      {}'.format(self.game_info['time']),
                                                                int(C.SCREEN_W / 36), (0, 0, 0)),
                                              C.SCREEN_W / 8 * 3, C.SCREEN_H / 16 * 3))
                if self.game_info['level'] == 1:
                    self.state_lables.append((self.create_lable('TIME      {}'.format(self.game_info['time']),
                                                                int(C.SCREEN_W / 36), (255, 255, 255)),
                                              C.SCREEN_W / 8 * 3, C.SCREEN_H / 16 * 3))

            if self.game_info['level'] != 1:
                self.state_lables.append((self.create_lable('WORLD      {}'.format(self.game_info['level'] + 1),
                                                            int(C.SCREEN_W / 36), (0, 0, 0)),
                                          C.SCREEN_W / 8, C.SCREEN_H / 16 * 3))
            if self.game_info['level'] == 1:
                self.state_lables.append((self.create_lable('WORLD      {}'.format(self.game_info['level'] + 1),
                                                            int(C.SCREEN_W / 36), (255, 255, 255)),
                                          C.SCREEN_W / 8, C.SCREEN_H / 16 * 3))

    def create_info_lables(self):
        self.info_lables = []
        # self.info_lables.append((self.create_lable('HELLO'), (75, 30)))
        # self.info_lables.append((self.create_lable('WORLD'), (450, 30)))
        pass

    # create_lable processes the infomation and display to the screen totally
    def create_lable(self, lable, size=-1, color=(255, 255, 255), width_scale=1.25, height_scale=1):
        if size == -1:
            size = int(C.SCREEN_W / 32)
        font = pygame.font.SysFont(C.FONT, size)
        # "1" is smooth edge
        lable_image = font.render(lable, 1, color)
        # reduce the font size and amplify it to produce smooth edge(pygame property)
        rect = lable_image.get_rect()
        lable_image = pygame.transform.scale(lable_image, (int(rect.width * width_scale),
                                                           int(rect.height * height_scale)))
        return lable_image

    # frash it
    def update(self):
        # self.flash_coin.update()
        pass

    # draw...
    def draw(self, surface):
        # surface.blit(self.create_lable('F**k you!', size=60), (100, 400))
        # draw the lables
        for lable in self.state_lables:
            # 0 is picture,1 ans 2 are position
            surface.blit(lable[0],
                         (lable[1] - lable[0].get_rect().size[0] * 0.5, lable[2] - lable[0].get_rect().size[1] * 0.5))

        for lable2 in self.info_lables:
            surface.blit(lable2[0], (
            lable2[1] - lable2[0].get_rect().size[0] * 0.5, lable2[2] - lable2[0].get_rect().size[1] * 0.5))
        # surface.blit(self.flash_coin.image, self.flash_coin.rect)

        if self.state == 'load_screen':
            # surface.blit(self.player_image, (300, 270))
            pass
