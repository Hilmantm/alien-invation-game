import pygame


class Ship:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image
        self.image = pygame.image.load('./images/ship.bmp')
        self.rect = self.image.get_rect()

        # start each new ship in middle bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """
        Draw new ship at its current location
        """
        self.screen.blit(self.image, self.rect)