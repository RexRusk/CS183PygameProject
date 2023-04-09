from ..components import info, brick, box, enemy, coin
from .. import tools, setup, buttons
from ..components import player, stuff
from .. import constants as C
import pygame
import os
import json


class Level:
    def start(self, game_info):
        self.game_info = game_info
        self.setup_music(self.game_info)
        self.finished = False
        self.next = 'game_over'
        self.info = info.Info('level', self.game_info)
        self.level = self.game_info['level']
        # loading maps' json
        self.load_map_data()
        self.setup_background()
        # loading player's position in each map
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks_boxes_coins()
        self.setup_enemies()
        self.setup_checkpoints()
        self.check_win()
        self.current_time = 0
        self.setup_touches()
        self.a = 0  # pause
        self.b = 0  # menu
        self.stop = False
        self.hold = False  # buttons

    def load_map_data(self):
        file_name = ['level_1.json', 'level_2.json', 'level_3.json', 'level_4.json']
        file_path = os.path.join('source/data/maps', file_name[self.level])
        with open(file_path) as f:
            self.map_data = json.load(f)

    # set up level_1 background
    def setup_background(self):
        self.image_name = self.map_data['image_name']
        # sky is here
        self.sky = setup.GRAPHICS['Sky']
        sky_rect = self.sky.get_rect()
        self.sky = pygame.transform.scale(self.sky, (int(sky_rect.width * C.BG_MULTI),
                                                     int(sky_rect.height * C.BG_MULTI)))

        self.black = setup.GRAPHICS['black']
        sky_rect = self.sky.get_rect()
        self.black = pygame.transform.scale(self.black, (int(sky_rect.width * C.NBG_MULTI),
                                                         int(sky_rect.height * C.NBG_MULTI)))

        # background is level ground incoudes ground but not sky
        self.background = setup.GRAPHICS[self.image_name]
        rect = self.background.get_rect()

        map_pic = ['level_1', 'level_2', 'level_3', 'level_4']
        self.background = tools.get_image(setup.GRAPHICS[map_pic[self.level]], 0, 0, 3692, 224, (0, 0, 0), C.BG_MULTI)
        if self.level == 1:
            self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI2),
                                                                       int(rect.height * C.BG_MULTI2)))
        else:
            self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI),
                                                                       int(rect.height * C.BG_MULTI)))
        # TODO:this line is testing
        self.background_rect = self.background.get_rect()

        self.game_window = setup.SCREEN.get_rect()

        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def setup_start_positions(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        # test
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def setup_player(self):
        self.player = player.Player('mario', self.game_info)
        self.player.rect.x = self.game_window.x + self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_items(self):
        # collision detection datas
        # group is to handle multiply sprite objects
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_bricks_boxes_coins(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()

        # bricks
        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x, y = brick_data['x'], brick_data['y']
                brick_type = brick_data['type']
                if 'brick_num' in brick_data:
                    # TODO batch bricks
                    pass
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type))

        # boxes
        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x, y = box_data['x'], box_data['y']
                box_type = box_data['type']
                self.box_group.add(box.Box(x, y, box_type))

        # coins
        if 'coin' in self.map_data:
            for coin_data in self.map_data['coin']:
                x, y = coin_data['x'], coin_data['y']
                self.coin_group.add(coin.FlashingCoins(x, y))

    def setup_enemies(self):
        # enemy put into this group after checkpoints
        self.dying_group = pygame.sprite.Group()
        self.shell_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id] = group

    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_group_id = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_group_id))

    def setup_music(self, game_info):
        if game_info['level'] == 0:
            pygame.mixer.stop()
            tools.load_musics('resources/music/level1.mp3', -1)
        elif game_info['level'] == 1:
            pygame.mixer.stop()
            tools.load_musics('resources/music/level2.mp3', -1)
        elif game_info['level'] == 2:
            pygame.mixer.stop()
            tools.load_musics('resources/music/level3.mp3', -1)
        elif game_info['level'] == 3:
            pygame.mixer.stop()
            tools.load_musics('resources/music/happily.mp3', -1)

    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        # update player's position

        # pause button
        if self.stop == True:
            self.update_touches(keys)
        else:
            if self.player.dead:
                self.player.update(keys)
                if self.current_time - self.player.death_timer > 3000:
                    self.finished = True
                    self.update_game_info()
            else:
                self.player.update(keys)
                self.game_info.update()
                self.update_touches(keys)
                self.update_player_position()
                self.check_checkpoints()
                self.check_if_go_die()
                self.update_game_window()
                self.info.update()
                self.brick_group.update()
                self.box_group.update()
                self.coin_group.update()
                self.enemy_group.update(self)
                self.dying_group.update(self)
                self.shell_group.update(self)
                self.check_win()
                self.info.create_state_lables()

        self.draw(surface)

    def update_player_position(self):
        # x direction
        # TODO +=
        self.player.rect.x += self.player.x_vel
        # self.player.rect.x = int(pygame.mouse.get_pos()[0])
        # self.player.rect.y = int(pygame.mouse.get_pos()[1])
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x_collisions()

        # y direction
        if not self.player.dead:
            self.player.rect.y += self.player.y_vel
            self.check_y_collisions()

    # collision detection
    def check_x_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if collided_sprite:
            self.adjust_player_x(collided_sprite)

        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.player.go_die()

        shell = pygame.sprite.spritecollideany(self.player, self.shell_group)
        if shell:
            if shell.state == 'slide':
                self.player.go_die()
            else:
                if self.player.rect.x < shell.rect.x:
                    shell.x_vel = 10
                    shell.rect.x += 40
                    shell.direction = 1
                else:
                    shell.x_vel = -10
                    shell.rect.x -= 40
                    shell.direction = -1
                shell.state = 'slide'

    def check_y_collisions(self):

        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        brick = pygame.sprite.spritecollideany(self.player, self.brick_group)
        box = pygame.sprite.spritecollideany(self.player, self.box_group)
        coin = pygame.sprite.spritecollideany(self.player, self.coin_group)
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)

        # conclude which to bump
        if brick and box:
            to_brick = abs(self.player.rect.centerx - brick.rect.centerx)
            to_box = abs(self.player.rect.centerx - box.rect.centerx)
            if to_brick > to_box:
                brick = None
            else:
                box = None

        if ground_item:
            self.adjust_player_y(ground_item)
        if brick:
            self.adjust_player_y(brick)
        if box:
            self.adjust_player_y(box)
            if box.box_type == 2:
                tools.load_sounds('resources/sound/aha.mp3', 1.0)
        if coin:
            tools.load_sounds('resources/sound/coin.mp3', 1.0)
            coin.kill()
            self.game_info['coin'] += 1
        if enemy:
            tools.load_sounds('resources/sound/trampled.mp3', self.game_info['volume'])
            # move enemy in groups
            self.enemy_group.remove(enemy)
            if enemy.name == 'koopa':
                self.shell_group.add(enemy)
            else:
                self.dying_group.add(enemy)
            if self.player.y_vel < 0:
                how = 'bumped'
            else:
                how = 'trampled'
                self.player.state = 'jump'
                self.player.rect.bottom = enemy.rect.top
                self.player.current_time2 = pygame.time.get_ticks()
                self.player.y_vel = self.player.jump_vel * 0.8

            enemy.go_die(how)

            # add score
            self.game_info['score'] += 100
        self.check_will_fall(self.player)

    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        # downwards
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.rect.bottom = sprite.rect.top
            self.player.y_vel = 0
            self.player.state = 'walk'
        # upwards
        else:
            self.player.rect.top = sprite.rect.bottom
            self.player.y_vel = 7
            self.player.state = 'fall'

            # box bumped
            if sprite.name == 'box':
                if sprite.state == 'rest':
                    self.game_info['score'] += 100
                    sprite.go_bumped()

    def check_will_fall(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(sprite, check_group)
        if not collided_sprite and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1

    def update_game_window(self):
        half = self.game_window.x + self.game_window.width / 2
        if self.player.x_vel > 0 and self.player.rect.centerx > half \
                and self.game_window.right < self.end_x:
            # print(self.player.x_vel, self.player.rect.centerx, self.game_window.left, self.start_x)
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

        if self.player.x_vel < 0 and self.player.rect.centerx < half \
                and self.game_window.left > 0:
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

    def draw(self, surface):
        # blit(source,dest,area=None)
        self.game_ground.blit(self.black, self.game_window)
        self.game_ground.blit(self.background, self.game_window, self.game_window)

        # draw player
        self.game_ground.blit(self.player.image, self.player.rect)
        # put the game player,background to ground, and blit ground
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        self.coin_group.draw(self.game_ground)

        # enemies
        self.enemy_group.draw(self.game_ground)
        self.dying_group.draw(self.game_ground)
        self.shell_group.draw(self.game_ground)

        surface.blit(self.game_ground, (0, 0), self.game_window)
        self.info.draw(surface)

        # buttons
        surface.blit(self.pause_button, (C.SCREEN_W * 7 / 8 - self.pause_button.get_rect().size[0] / 2,
                                         C.SCREEN_H * 1 / 8 - self.pause_button.get_rect().size[1] / 2))

        # menu button
        if self.stop == True:
            surface.blit(self.menu_button, (C.SCREEN_W / 2 - self.menu_button.get_rect().size[0] / 2,
                                            C.SCREEN_H / 8 * 3 - self.menu_button.get_rect().size[1] / 2))

    def check_checkpoints(self):
        # check whether player invoke checkpoints
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
        if checkpoint:
            # checkpoints for enemy appearance
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_group_id)])
            checkpoint.kill()

    def check_if_go_die(self):
        if self.player.rect.y > C.SCREEN_H:
            self.player.go_die()

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
            self.game_info['score'] = self.game_info['next_score']
            self.game_info['coin'] = self.game_info['next_coin']
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load_screen'

    def check_win(self):
        if (self.player.rect.x > 8900 and self.game_info['level'] == 0) \
                or (self.player.rect.x > 8000 and self.game_info['level'] == 1):
            self.player.x_vel = 7
            if (self.player.rect.x > 9000 and self.game_info['level'] == 0) \
                    or (self.player.rect.x > 8100 and self.game_info['level'] == 1):
                self.game_info['next_score'] += self.game_info['score']
                self.game_info['next_coin'] += self.game_info['coin']
                self.next = 'load_screen'
                self.game_info['level'] += 1
                pygame.time.delay(200)
                self.finished = True
        if (self.player.rect.x > 6800 and self.game_info['level'] == 2):
            self.player.x_vel = 7
            if (self.player.rect.x > 7000 and self.game_info['level'] == 2 and self.finished == False):
                tools.load_musics('resources/sound/completed.mp3')
                self.game_info['next_score'] = self.game_info['score']
                self.game_info['next_coin'] += self.game_info['coin']
                self.game_info['level'] += 1
                self.game_info['player_state'] = 'complete'
                self.next = 'load_screen'
                pygame.time.delay(400)
                self.finished = True

    def setup_touches(self):
        self.pause_button = tools.get_image(setup.GRAPHICS['Iconic2048x2048'], 140, 810, 138, 138, (0, 0, 0),
                                            C.NBG_MULTI)
        # back to manu
        self.menu_button = tools.get_image(setup.GRAPHICS['Iconic2048x2048'], 1324, 1105, 138, 138, (0, 0, 0),
                                           2 * C.NBG_MULTI)

    def update_touches(self, keys):
        x, y = pygame.mouse.get_pos()
        pressed_array = pygame.mouse.get_pressed()

        if self.a % 2 == 0 \
                and x >= C.SCREEN_W * 7 / 8 - 69 / 2 \
                and x <= C.SCREEN_W * 7 / 8 + 69 / 2 \
                and y >= C.SCREEN_H * 1 / 8 - 69 / 2 \
                and y <= C.SCREEN_H * 1 / 8 + 69 / 2:
            self.pause_button = buttons.button_pressed(self.pause_button)
            self.a = 1

        if not (x >= C.SCREEN_W * 7 / 8 - 69 / 2 \
                and x <= C.SCREEN_W * 7 / 8 + 69 / 2 \
                and y >= C.SCREEN_H * 1 / 8 - 69 / 2 \
                and y <= C.SCREEN_H * 1 / 8 + 69 / 2):
            self.pause_button = tools.get_image(setup.GRAPHICS['Iconic2048x2048'], 140, 810, 138, 138, (0, 0, 0),
                                                C.NBG_MULTI)
            self.a = 0

        # play button
        if pressed_array[0] \
                and self.hold == False \
                and self.stop == False \
                and x >= C.SCREEN_W * 7 / 8 - 69 / 2 \
                and x <= C.SCREEN_W * 7 / 8 + 69 / 2 \
                and y >= C.SCREEN_H * 1 / 8 - 69 / 2 \
                and y <= C.SCREEN_H * 1 / 8 + 69 / 2:
            self.hold = True
            self.stop = True

        if not pygame.mouse.get_pressed()[0]:
            self.hold = False

        if self.stop == True:
            # go main_menu button
            if pressed_array[0] \
                    and x >= C.SCREEN_W / 2 - 69 * 2 \
                    and x <= C.SCREEN_W / 2 + 69 * 2 \
                    and y >= C.SCREEN_H / 2 - 69 * 2 \
                    and y <= C.SCREEN_H / 2 + 69 * 2:
                self.stop = False
                self.next = 'main_menu'
                pygame.time.delay(50)
                self.finished = True

            # back to play
            elif pressed_array[0] and self.hold == False and self.stop == True:
                self.hold = True
                self.stop = False
