import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
  """A class to manage bullets fired from the ship"""

  def __init__(self, ai_game):
    """Create a bullet object at the ship's current position."""
    super().__init__()
    self.screen = ai_game.screen
    self.settings = ai_game.settings
    self.color = self.settings.bullet_color
    self.bullet_direction = 0
    self.was_fired = True

    self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
    self.rect.midtop = ai_game.ship.rect.midtop

    self.bullet_speed = self.settings.bullet_speed
    # Store the bullet's position as a vector.
    self.position = pygame.Vector2(float(self.rect.x), float(self.rect.y))
    self.velocity = pygame.Vector2(0, -self.bullet_speed)

    self.health = self.settings.bullet_piercing

  def update(self):
    """Move the bullet"""
    self.position += self.velocity
    self.rect.x = self.position.x
    self.rect.y = self.position.y

  def draw_bullet(self):
    """Draw the bullet to the screen"""
    image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height))
    transformed_image = pygame.transform.rotate(image, self.bullet_direction)
    self.screen.blit(transformed_image, self.rect)
    