import pygame
from .. import setup
from .. import tools, buttons
from .. import constants as C
from .. components import info
from ..states import settings
import  sys
class MainMenu:
    def __init__(self):
        game_info = {
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'not_complete',
            'level': 0,
            'volume': 0.5,
            'time': 0,
            're_game': 0,
            'next_score': 0,
        }
        self.start(game_info)
    def start(self, game_info):
        #game_info receive information from last state
        self.game_info = game_info
        self.setup_background()
        self.setup_player()
        self.setup_gui()
        self.setup_buttons()
        self.setup_cursor()
        self.setup_music()
        self.info = info.Info('main_menu', self.game_info)
        self.finished = False
        self.next = 'a'
        #a,b,c judge when cursor is in buttons then return 1
        self.a = 0
        self.b = 0
        self.c = 0
        self.timer = 0


    def setup_background(self):
        #these codes allow long pictures appear in window as slading rectangle
        #self.background = setup.GRAPHICS['Background']
        self.background1 = setup.GRAPHICS['Background_8_6']
        self.background1_rect = self.background1.get_rect()
        self.background1 = pygame.transform.scale(self.background1, (int(self.background1_rect.width), int(self.background1_rect.height)))
        self.background1 = tools.get_image(setup.GRAPHICS['Background_8_6'], 0, 0, self.background1_rect.width,
                                           self.background1_rect.height, (0, 0, 0), 1)

        self.viweport = setup.SCREEN.get_rect()

        #self.caption = tools.get_image(setup.GRAPHICS['logo1'], 0, 0, 700, 290, (0, 0, 0), C.NBG_MULTI)

    def update_background(self, keys):
        self.timer += 1
        if self.timer - C.SCREEN_W > 0:
            self.timer = 0
        # self.background1.get_rect().x += 500

        self.viweport = (-self.timer, 0)
        self.viewport = (C.SCREEN_W - self.timer, 0)


    def setup_player(self):
        self.player_image = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0), C.BG_MULTI)
    def setup_gui(self):
        #these codes print main menu ui graphics
        #self.gui1 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 48, 525, 136, (0, 0, 0), C.NBG_MULTI)
        self.gui2 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 315, 525, 136, (0, 0, 0), C.NBG_MULTI)
        self.gui3 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 585, 525, 136, (0, 0, 0), C.NBG_MULTI)

    def setup_buttons(self):
        self.gui1 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 48, 525, 136, (0, 0, 0), C.NBG_MULTI)

    def setup_cursor(self):
        #setup the main menu cursor(mush)
        #self.cursor = pygame.sprite.Sprite()
        #self.cursor.image = tools.get_image(setup.GRAPHICS['cursor'], 0, 0, 100, 100, (0, 0, 0), C.NBG_MULTI)
        #rect = self.cursor.image.get_rect()
        #rect.x, rect.y = (220, 360)
        #self.cursor.rect = rect
        #initial cursor to 1 player
        #self.cursor.state = 1
        pass



    #use keyboard to control the cursor
    def update_cursor(self, keys):
        if keys[pygame.K_UP] and self.cursor.state > 1:
            self.cursor.state -= 1
            self.cursor.rect.y -= 180

        elif keys[pygame.K_DOWN] and self.cursor.state < 3:
            self.cursor.state += 1
            self.cursor.rect.y += 180
        elif keys[pygame.K_RETURN]:
            if self.cursor.state == 1:
                #finish means the main menu windows finished
                self.finished = True
            elif self.cursor.state == 2:
                self.finished = True
            elif self.cursor.state == 3:
                self.finished = True

    def update_buttons(self, keys):
        x, y = pygame.mouse.get_pos()
        pressed_array = pygame.mouse.get_pressed()
        #play button
        if pressed_array[0] \
                and x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 2 - 68\
                and y <= C.SCREEN_H / 2 + 68:
            tools.load_sounds('resources/sound/move.wav', self.game_info['volume'])
            self.reset_game_info()
            self.next = 'choose_map'
            pygame.time.delay(50)
            self.finished = True
            # motion when cursor is in play button
        if self.a % 2 == 0 \
                and x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 2 - 68 \
                and y <= C.SCREEN_H / 2 + 68:
            self.gui1 = buttons.button_pressed(self.gui1)
            self.a = 1
        if not (x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 2 - 68 \
                and y <= C.SCREEN_H / 2 + 68):
            self.gui1 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 48, 525, 136, (0, 0, 0), C.NBG_MULTI)
            self.a = 0


        #settings button:
        if pressed_array[0] \
                and x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 8 * 5 - 68 \
                and y <= C.SCREEN_H / 8 * 5 + 68:
            tools.load_sounds('resources/sound/move.wav', self.game_info['volume'])
            self.next = 'settings'
            pygame.time.delay(50)
            self.finished = True

        # motion when cursor is in settings button
        if self.b % 2 == 0 \
                and x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 8 * 5 -68\
                and y <= C.SCREEN_H / 8 * 5 + 68:
            self.gui2 = buttons.button_pressed(self.gui2)
            #print(self.info.state_lables[2][0])
            #self.info.state_lables[2][0] = buttons.button_pressed((self.info.state_lables[2][0]))
            self.b = 1

        if not(x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 8 * 5 -68\
                and y <= C.SCREEN_H / 8 * 5 + 68):
            self.gui2 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 315, 525, 136, (0, 0, 0), C.NBG_MULTI)
            self.b = 0


        #quit button
        if pressed_array[0] \
                and x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 4 * 3 -68\
                and y <= C.SCREEN_H / 4 * 3 + 68:
            tools.load_sounds('resources/sound/move.wav', self.game_info['volume'])
            pygame.time.delay(50)
            pygame.quit()
            sys.exit()
            # motion when cursor is in settings button
        if self.c % 2 == 0 \
                and x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 4 * 3 - 68 \
                and y <= C.SCREEN_H / 4 * 3 + 68:
            self.gui3 = buttons.button_pressed(self.gui3)
            self.c = 1
        if not (x >= C.SCREEN_W / 2 - 262 \
                and x <= C.SCREEN_W / 2 - 262 + 525 \
                and y >= C.SCREEN_H / 4 * 3 - 68 \
                and y <= C.SCREEN_H / 4 * 3 + 68):
            self.gui3 = tools.get_image(setup.GUI['Empty1024x1024'], 477, 585, 525, 136, (0, 0, 0), C.NBG_MULTI)
            self.c = 0

    def update(self, surface, keys):
        #gameinfo
        self.game_info.update()
        #(graphics,position)

        #self.update_cursor(keys)

        self.update_background(keys)
        self.update_buttons(keys)


        surface.blit(self.background1, self.viweport)
        surface.blit(self.background1, self.viewport)


        #surface.blit(self.caption, (C.SCREEN_W / 2 - 350, 0))
        #surface.blit(self.player_image, (110, 494))
        surface.blit(self.gui1, (C.SCREEN_W / 2 - self.gui1.get_rect().size[0] / 2, C.SCREEN_H / 2 - self.gui1.get_rect().size[1] / 2))
        surface.blit(self.gui2, (C.SCREEN_W / 2 - self.gui2.get_rect().size[0] / 2, C.SCREEN_H / 8 * 5 - self.gui2.get_rect().size[1] / 2))
        surface.blit(self.gui3, (C.SCREEN_W / 2 - self.gui3.get_rect().size[0] / 2, C.SCREEN_H / 4 * 3 - self.gui3.get_rect().size[1] / 2))

        #surface.blit(self.cursor.image, self.cursor.rect)

        #buttons.Buttons.update_state(keys)

        #surface.blit(self.button1, (C.SCREEN_W / 2 - 262, C.SCREEN_H / 2))

#display the main menu status words
        self.info.update()
        self.info.draw(surface)


    def reset_game_info(self):
        self.game_info.update({
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'not_complete',
            'level': 0,
            'volume': 0.5,
            're_game': 1,
            'next_score': 0,
        })

    def setup_music(self):
        tools.load_musics('resources/music/menu.wav')
        #pygame.mixer.music.queue('resources/music/Happy_BGM2.mp3')

