import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvation:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.background = pygame.image.load("./images/background.jpg")

        # this setting use display width and height in settings class
        # uncomment if you want to use this
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invation")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "play")

        pygame.mixer.music.load("./sound/Throwback Galaxy - Super Mario Galaxy 2.mp3")
        pygame.mixer.music.play(-1)

    def run_game(self):
        while True:
            # watch event from keyboard and mouse
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.fire_sound()
            self.bullets.add(new_bullet)

    def fire_sound(self):
        fire_sound = pygame.mixer.Sound("./sound/fire_pzmCtSSg.wav")
        fire_sound.set_volume(0.3)
        fire_sound.play()

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

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """
        Check if the fleet is in the edge of the screen and then
        update the position of all aliens in the fleet
        :return:
        """
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (7 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # log the result
        print(f"Alien Width => {alien_width}")
        print(f"Alien Height => {alien_height}")
        print(f"Available Space X => {available_space_x}")
        print(f"Available Space Y => {available_space_y}")
        print(f"Number Alien X => {number_alien_x}")
        print(f"Number Rows => {number_rows}")

        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        Drop entire fleet and change the fleet direction
        :return:
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        # Draw button if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _create_alien(self, alien_number, row_number):
        """
        Create an alien and place it in the row
        :param alien_number:
        :param row_number:
        :return:
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x  # kali dengan negatif 1 agar alien digambar dari kanan
        print(alien.rect.x)
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_aliens_bottom(self):
        """
        Check if any aliens reach the edges
        :return:
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """
        Respond the ship if hit by any alien
        :return:
        """
        if self.stats.ships_left > 0:
            # decrement ship left
            self.stats.ships_left -= 1
            self.sb.prep_ship()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_level()
            self.sb.prep_score()
            self.sb.prep_ship()

            self.aliens.empty()
            self.bullets.empty()

            pygame.mouse.set_visible(False)

        # clear all object
        self.aliens.empty()
        self.bullets.empty()

        # reset position
        self._create_fleet()
        self.ship.center_ship()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()


if __name__ == '__main__':
    ai = AlienInvation()
    ai.run_game()
