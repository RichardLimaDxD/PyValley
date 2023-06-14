import pygame
from settings import *


class Transition:
    def __init__(self, reset, player):
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        self.image = pygame.Surface((screen_width, screen_width))
        self.color = 255
        self.speed = -2

    def play(self):
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(
            self.image, (0, 0), special_flags=pygame.BLEND_RGB_MULT
        )