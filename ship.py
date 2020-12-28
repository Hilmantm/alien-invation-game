import pygame


class Ship:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image
        self.image = pygame.image.load('./images/ship.bmp')
        self.rect = self.image.get_rect()

        # start each new ship in middle bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Update the ship by flag movement
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """
        Draw new ship at its current location
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """
        Center the new ship in middle bottom of the screen
        :return:
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)