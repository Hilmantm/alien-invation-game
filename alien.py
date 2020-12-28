import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """
    Class to represent a single alien object
    """

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image and set rect attribute
        self.image = pygame.image.load('./images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store to exact position
        self.x = float(self.rect.x)

    def update(self):
        """
        Move the alien to right or to left
        :return:
        """
        self.x = (self.settings.alien_speed + self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """
        Return true if alien touch the edge of the screen
        :return:
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True