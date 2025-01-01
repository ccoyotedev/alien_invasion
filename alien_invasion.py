import sys
from time import sleep
import random

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from gold_coin import GoldCoin
from shop import Shop

class AlienInvasion:
  """Overall class to manage game assets and behavior."""

  def __init__(self):
    """Initialize the game, and create game resources."""
    pygame.init()
    self.clock = pygame.time.Clock()
    self.settings = Settings()

    self.screen = pygame.display.set_mode(
      (self.settings.screen_width, self.settings.screen_height)
    )

    pygame.display.set_caption("Alien Invasion")

    self.stats = GameStats(self)
    self.scoreboard = Scoreboard(self)
    self.shop = Shop(self)

    self.ship = Ship(self)
    self.bullets = pygame.sprite.Group()
    self.aliens = pygame.sprite.Group()
    self.gold_coins = pygame.sprite.Group()

    self._create_fleet()

    self.game_active = False
    self.shop_active = False

    self.play_button = Button(self, "Play")
  
  def run_game(self):
    """Start the main loop of the game"""
    while True:
      self._check_events()

      if self.game_active:
        self.ship.update()
        self._update_bullets()
        self._update_aliens()
        self._update_gold_coins()
  
      self._update_screen()
      self.clock.tick(60)

  def _check_events(self):
    """Respond to keypresses and mouse events"""
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
          self._check_resume_button(mouse_pos)
  
  def _check_play_button(self, mouse_pos):
    """Start a new game when the player clicks Play."""
    button_clicked = self.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not self.game_active and not self.shop_active:
      self._start_game()

  def _check_resume_button(self, mouse_pos):
    """Start next wave when resume button is clicked."""
    button_clicked = self.shop.resume_button.rect.collidepoint(mouse_pos)
    if button_clicked and self.shop_active:
      self._start_wave()

  def _check_keydown_events(self, event):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
      self.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
      self.ship.moving_left = True
    elif event.key == pygame.K_q:
      sys.exit()
    elif event.key == pygame.K_SPACE:
      self._fire_bullet()
    elif event.key == pygame.K_p:
      if not self.game_active:
        self._start_game()

  def _check_keyup_events(self, event):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
      self.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
      self.ship.moving_left = False

  def _start_game(self):
    """Start a new game"""
    self.settings.initialize_dynamic_settings()
    self.stats.reset_stats()
    self.scoreboard.prep_score()
    self.scoreboard.prep_level()
    self.scoreboard.prep_ships()
    self.game_active = True

    self.bullets.empty()
    self.aliens.empty()
    self.gold_coins.empty()

    self._create_fleet()
    self.ship.center_ship()

    pygame.mouse.set_visible(False)
  
  def _fire_bullet(self):
    """Create a new bullet and add it to the bullets group."""
    if self.game_active and len(self.bullets) < self.settings.bullets_allowed:
      new_bullet = Bullet(self)
      self.bullets.add(new_bullet)
  
  def _update_bullets(self):
    """Update position of bullets and get rid of old bullets"""
    self.bullets.update()

    # Get rid of bullet that have left the screen
    for bullet in self.bullets.copy():
      if bullet.rect.bottom <= 0:
        self.bullets.remove(bullet)

    self._check_bullet_alien_collisions()

  def _check_bullet_alien_collisions(self):
    """Respond to bullet alien collisions"""
    collisions = pygame.sprite.groupcollide(
      self.bullets, self.aliens, True, True
    )
    if collisions:
      for aliens in collisions.values():
        self.stats.score += self.settings.alien_points * len(aliens)
        for alien in aliens:
          rand_no = random.uniform(0, 1.0)
          if (rand_no < self.settings.gold_drop_chance):
            self._drop_coin(alien)

      self.scoreboard.prep_score()
      self.scoreboard.check_high_score()

    if not self.aliens:
      self._end_wave()

  def _drop_coin(self, alien):
    """Handle the dropping of coins"""
    gold_coin = GoldCoin(self)
    gold_coin.rect.centerx = alien.rect.centerx
    gold_coin.y = alien.rect.centery
    self.gold_coins.add(gold_coin)

  def _update_aliens(self):
    """Update the positions of all aliens in the fleet"""
    self._check_fleet_edges()
    self.aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
      self._ship_hit()

    # Look for aliens hitting the bottom of the screen
    self._check_aliens_bottom()

  def _update_gold_coins(self):
    """Update the positions of gold coins"""
    self.gold_coins.update()

    # Get rid of gold coins that have left the screen
    for gold_coin in self.gold_coins.copy():
      if gold_coin.rect.bottom <= 0:
        self.gold_coins.remove(gold_coin)

    # Look for gold-ship collisions
    collision = pygame.sprite.spritecollide(self.ship, self.gold_coins, True)
    if collision:
      for gold in collision:
        self.stats.gold += 1
        self.scoreboard.prep_gold()

  def _end_wave(self):
    """End the current wave and enter the shop"""
    self.bullets.empty()
    self.gold_coins.empty()
    self.shop_active = True
    self.game_active = False
    pygame.mouse.set_visible(True)

  def _start_wave(self):
    """Start next wave"""
    self._create_fleet()
    self.settings.increase_speed()
    
    self.stats.level += 1
    self.scoreboard.prep_level()
    self.shop_active = False
    self.game_active = True
    self.ship.center_ship()

    pygame.mouse.set_visible(False)

  def _ship_hit(self):
    """Respond to the ship being hit by an alien."""
    if self.stats.ships_left > 0:
      self.stats.ships_left -= 1
      self.scoreboard.prep_ships()

      self.bullets.empty()
      self.aliens.empty()
      self.gold_coins.empty()

      self._create_fleet()
      self.ship.center_ship()

      sleep(0.5)
    else:
      self.game_active = False
      pygame.mouse.set_visible(True)

  def _create_fleet(self):
    """Create the fleet of aliens"""
    # Create an alien and keep adding until there is no room left.
    # Spacing between aliens is one alient width and one alien height.
    alien = Alien(self)
    alien_width, alien_height = alien.rect.size

    current_x = alien_width
    for current_row in range(self.settings.max_fleet_rows):
      while current_x < (self.settings.screen_width - 2 * alien_width):
        self._create_alien(current_x, (current_row + 1) * alien_height)
        current_x += 2 * alien_width
      
      current_x = alien_width
  
  def _create_alien(self, x_position, y_position):
    """Create an alien and place it in the row"""
    new_alien = Alien(self)
    new_alien.x = x_position
    new_alien.rect.x = x_position
    new_alien.rect.y = y_position
    self.aliens.add(new_alien)
  
  def _check_fleet_edges(self):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break

  def _check_aliens_bottom(self):
    """Check if any aliens have reached the bottom of the screen"""
    for alien in self.aliens.sprites():
      if alien.rect.bottom >= self.settings.screen_height:
        # Treat this the same as the ship getting hit
        self._ship_hit()
        break

  def _change_fleet_direction(self):
    """Drop the entire fleet and change direction"""
    for alien in self.aliens.sprites():
      alien.rect.y += self.settings.fleet_drop_speed
    self.settings.fleet_direction *= -1

  def _update_screen(self):
    """Update images on the screen, and flip to the new screen"""
    self.screen.fill(self.settings.bg_color)
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    for gold_coin in self.gold_coins.sprites():
      gold_coin.draw_gold_coin()
    self.ship.blitme()
    self.aliens.draw(self.screen)

    self.scoreboard.show_score()

    if not self.game_active and not self.shop_active:
      self.play_button.draw_button()

    if self.shop_active:
      self._update_shop_screen()

    pygame.display.flip()

  def _update_shop_screen(self):
    """Update the screen with the shop"""
    self.shop.show_shop()

if __name__ == '__main__':
  # Make a game instance, and run the game
  ai = AlienInvasion()
  ai.run_game()