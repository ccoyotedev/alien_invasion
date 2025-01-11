import pygame
import random
import math

from src.entities import GoldCoin, Bullet

class CollisionHandler:
    def __init__(self, game):
        self.game = game

    def check_bullet_alien_collisions(self):
        """Respond to bullet alien collisions"""
        collisions = pygame.sprite.groupcollide(
            self.game.bullets, self.game.aliens, False, True
        )
        if collisions:
            for bullet, aliens in collisions.items():
                self.game.stats.score += self.game.settings.alien_points * len(aliens)
                for alien in aliens:
                    self._handle_alien_hit(alien)

                bullet.health -= len(aliens)
                if bullet.health <= 0:
                    self.game.bullets.remove(bullet)

        self.game.scoreboard.prep_score()
        self.game.scoreboard.check_high_score()

        if not self.game.aliens:
            self.game.end_wave()

    def _handle_alien_hit(self, alien):
      """Handle what happens when an alien is hit"""
      gold_drop_roll = random.uniform(0, 1.0)
      if (gold_drop_roll <= self.game.settings.gold_drop_chance):
          self._drop_coin(alien)

          if (self.game.settings.shrapnel_chance > 0):
            shrapnel_roll = random.uniform(0, 1.0)
            if (shrapnel_roll <= self.game.settings.shrapnel_chance):
                self._fire_shrapnel(alien)

    def _drop_coin(self, alien):
      """Handle the dropping of coins"""
      gold_coin = GoldCoin(self.game)
      gold_coin.rect.centerx = alien.rect.centerx
      gold_coin.position.y, gold_coin.position.x = alien.rect.centery, alien.rect.centerx
      self.game.gold_coins.add(gold_coin)

    def _fire_shrapnel(self, alien):
      """Handle shrapnel"""
      shrapnel_bullet = Bullet(self.game)
      shrapnel_bullet.was_fired = False
      angle = 360 * random.uniform(0, 1.0)
      shrapnel_bullet.bullet_direction = angle
      shrapnel_bullet.velocity.x = self.game.settings.bullet_speed * math.sin(math.radians(angle))
      shrapnel_bullet.velocity.y = self.game.settings.bullet_speed * math.cos(math.radians(angle))
      shrapnel_bullet.position.y, shrapnel_bullet.position.x = alien.rect.centery, alien.rect.centerx
      self.game.bullets.add(shrapnel_bullet)