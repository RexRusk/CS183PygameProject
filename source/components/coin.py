import pygame
from .. import tools, setup
from .. import constants as C

class FlashingCoins(pygame.sprite.Sprite):
    def __init__(self, x, y, name='coin'):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.name = name
        self.frames = []
        self.frame_index = 0
        #shinning and shinning
        frame_rects = [(1, 160, 5, 8), (9, 160, 5, 8), (17, 160, 5, 8), (9, 160, 5, 8)]
        self.load_frames(frame_rects)
        #coin's image
        self.image = self.frames[self.frame_index]
        #coin's position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #set frash time
        self.timer = 0

    def load_frames(self, frame_rects):
        sheet = setup.GRAPHICS['item_objects']
        for frame_rect in frame_rects:
            # *let frame rect appears in reasonable position
            self.frames.append(tools.get_image(sheet, *frame_rect, (0, 0, 0), 2 * C.BRICK_MULTI))
        self.frame_index = 0

    def update(self):
        self.current_time = pygame.time.get_ticks()
        #set coin changes color by following time(ms)
        frame_durations = [375, 125, 125, 125]

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            #back to frame 0 when goes to 4
            self.frame_index %= 4
            self.timer = self.current_time
        #update coin's status
        self.image = self.frames[self.frame_index]
