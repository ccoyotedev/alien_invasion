import pygame
from pygame.sprite import Sprite

class GoldCoin(Sprite):
  """A class to manage gold dropped from aliens"""

  def __init__(self, ai_game):
    """Create a gold object"""
    super().__init__()
    self.screen = ai_game.screen
    self.settings = ai_game.settings
    self.color = self.settings.gold_color

    self.rect = pygame.Rect(0, 0, self.settings.gold_radius * 2, self.settings.gold_radius * 2)

    # Store the gold's position as a float.
    self.y = float(self.rect.y)

  def update(self):
    """Move the gold down the screen"""
    self.y += self.settings.gold_drop_speed
    self.rect.y = self.y

  def draw_gold_coin(self):
    """Draw the gold to the screen"""
    center = (self.rect.centerx, self.rect.centery)
    pygame.draw.circle(self.screen, self.color, center, self.settings.gold_radius)