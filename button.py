import pygame.font


class Button:

    def __init__(self, ai_game, message):
        """
        Button object constructor
        :param ai_game: main playground
        :param message: message in button
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the button properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # insert text into the button
        self._prep_message(message)

    def _prep_message(self, message):
        """
        Show text message into the button
        :param message: message or text will show in button
        """
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect_center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)