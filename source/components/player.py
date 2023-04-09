import pygame
from .. import tools, setup
from .. import constants as C
import json
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, name, game_info):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.game_info = game_info
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    #load player's picture transform data
    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    #the player's state
    def setup_states(self):
        self.state = 'stand'
        self.face_right = True
        self.dead = False
        self.big = False
        #todo
        self.can_jump = 2
    # player's speed
    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0
        #from mario.json
        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = C.GRAVITY
        #initial the speed

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel
    # record player's time from different states
    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0
        self.death_timer = 0
    def load_images(self):
        sheet = setup.GRAPHICS['mario_bros']
        frame_rects = self.player_data['image_frames']

        #these are frame pictures in different while pressing keys
        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []
        #collection
        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]
        #all
        self.all_frames = [
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames,
        ]
        #left and right data
        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                              frame_rect['width'], frame_rect['height'], (0, 0, 0), C.PLAYER_MUNTI)
                # True means left_right flip,False means up_down NOT flip
                left_image = pygame.transform.flip(right_image, True, False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)

        #frame_index from 1 to 4 represent different frames of player
        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
    #update the player's position
    def update(self, keys):
        self.game_info.update()
        #use current_time th update the time while changing player
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys)

    def handle_states(self, keys):
        self.can_jump_or_not(keys)
        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'die':
            self.die(keys)

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def can_jump_or_not(self, keys):
        if self.can_jump == 0 and (self.state == 'walk' or self.state == 'stand'):
            #todo
            self.can_jump = 2
            #second jump must before first jump
            self.can_second_jump = 0



    def stand(self, keys):
        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_SPACE] and self.can_jump > 0:
            self.can_jump -= 1
            self.y_vel = self.jump_vel
            self.current_time2 = pygame.time.get_ticks()
            tools.load_sounds('resources/music/jump.wav', self.game_info['volume'])
            self.state = 'jump'


    def walk(self, keys):
        if keys[pygame.K_LSHIFT]:
            self.max_x_vel = self.max_run_vel
            self.x_accel = self.run_accel
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel
        if keys[pygame.K_SPACE] and self.can_jump > 0:
            self.current_time2 = pygame.time.get_ticks()
            tools.load_sounds('resources/music/jump.wav', self.game_info['volume'])
            self.state = 'jump'
            self.can_jump -= 1
            self.y_vel = self.jump_vel
        if self.current_time - self.walking_timer > self.calc_frame_duration():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_right:
                self.x_vel -= self.x_accel
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel += self.x_accel
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'



    def jump(self, keys):
        self.frame_index = 4
        self.y_vel += self.gravity
        #self.can_jump  = 0
        if self.y_vel >= 0:
            self.state = 'fall'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.face_right = True
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.face_right = False
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        #fondermantal jump distance
        if not keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.current_time2 > 250:
            self.y_vel = 0
            self.state = 'fall'
            self.current_time = 0


    def fall(self, keys):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

        #if self.rect.bottom > C.GROUND_HEIGHT:
        #    self.rect.bottom = C.GROUND_HEIGHT
        #    self.y_vel = 0
        #    self.state = 'walk'

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.face_right = True
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.face_right = False
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

        if not keys[pygame.K_SPACE] and self.can_jump > 0:
            self.can_second_jump = 2

        if keys[pygame.K_SPACE] and self.can_jump > 0 and self.can_second_jump:
            self.current_time2 = pygame.time.get_ticks()
            tools.load_sounds('resources/music/jump.wav', self.game_info['volume'])
            self.state = 'jump'
            self.can_jump = 0
            self.can_second_jump = 1
            self.y_vel = self.jump_vel


    def die(self, keys):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

    def go_die(self):
        pygame.mixer.music.stop()
        tools.load_sounds('resources/music/dead.mp3', self.game_info['volume'])
        self.dead = True
        self.y_vel = self.jump_vel
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time


    #calculate
    def calc_vel(self, vel, accel, max_vel, is_positive=True):
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)
    def calc_frame_duration(self):
        duration = -60 / self.max_run_vel * abs(self.x_vel) + 80
        return duration

