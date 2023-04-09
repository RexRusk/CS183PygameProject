import  pygame
from .. import setup, tools
from .. import  constants as C
from .. components import  info
class ChoseMap:
    def start(self, game_info):
        self.finished = False
        self.list = ['level_1', 'level_2', 'level_3']
        self.next = self.list[0]
        self.setup_background()
        self.setup_buttons()
        self.game_info = game_info
        self.info = info.Info('chose_map', game_info)


    def setup_background(self):
        self.background = setup.GRAPHICS['green']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.NBG_MULTI),
                                                                   int(rect.height * C.NBG_MULTI)))
        self.background_rect = self.background.get_rect()

    def setup_buttons(self):
        self.back_button = tools.get_image(setup.GUI['Iconic1024x1024'], 70, 775, 70, 70, (0, 0, 0), C.NBG_MULTI)

    def update_buttons(self, keys):
        x, y = pygame.mouse.get_pos()
        pressed_array = pygame.mouse.get_pressed()
        #switch levels
        if pressed_array[0] \
            and y < C.SCREEN_H / 3:
            self.next = self.list[0]
        elif pressed_array[0] \
            and y > C.SCREEN_H * 1 / 3 \
            and y < C.SCREEN_H * 2 / 3:
            self.next = self.list[1]
        else: self.next = self.list[2]

        #play button
        if pressed_array[0] \
                and x >= C.SCREEN_W / 8 - 35 \
                and x <=C.SCREEN_W / 2 + 35 \
                and y >= C.SCREEN_H *7 / 8 - 35\
                and y <=C.SCREEN_H *7 / 8 + 35:
            self.next = 'main_menu'
            self.finished = True
        elif pressed_array[0]:
            self.next = 'load_screen'
            self.finished = True
    def update(self, surface, keys):
        self.update_buttons(keys)
        self.draw(surface)

    def draw(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.background, (0, 0))
        surface.blit(self.back_button, (C.SCREEN_W / 8 - self.back_button.get_rect().size[0] / 2,
                                        C.SCREEN_H *7 / 8 - self.back_button.get_rect().size[1] / 2))
        self.info.update()
        self.info.draw(surface)