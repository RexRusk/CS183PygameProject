import pygame


class Item(pygame.sprite.Sprite):
    #sprite in level
    def __init__(self, x, y, w, h, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name

class Checkpoint(Item):
    def __init__(self, x, y, w, h, checkpoint_type, enemy_group_id=None, name='checkpoint'):
        Item.__init__(self, x - 400, y, w, h, name)
        self.checkpoint_type = checkpoint_type
        self.enemy_group_id = enemy_group_id