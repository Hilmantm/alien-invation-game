import sys
import pygame
from settings import Settings

class AlienInvation:

    def __init__(self):
        pygame.init()
        self.settings = Settings

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invation")


    def run_game(self):
        while True:
            # watch event from keyboard and mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.settings.bg_color)

            pygame.display.flip()


if __name__ == '__main__':

    ai = AlienInvation()
    ai.run_game()