import sys
import pygame
from settings import Settings
from ship import Ship


class AlienInvation:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        # this setting use display width and height in settings class
        # uncomment if you want to use this
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height


        pygame.display.set_caption("Alien Invation")

        self.ship = Ship(self)

    def run_game(self):
        while True:
            # watch event from keyboard and mouse
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        # watch event from keyboard and mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """
        Respond to keypress.
        :param event:
        :return:
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """
        Respond to key release.
        :param event:
        :return:
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvation()
    ai.run_game()
