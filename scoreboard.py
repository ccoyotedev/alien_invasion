import pygame.font
from pygame.sprite import Group

from ship import Ship
from gold_coin import GoldCoin

class Scoreboard:
  """A class to report scoring information"""

  def __init__(self, ai_game):
    """Initalize scorekeeping attributes"""
    self.ai_game = ai_game
    self.screen = ai_game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = ai_game.settings
    self.stats = ai_game.stats

    # Font settings for scoring information.
    self.text_color = (30, 30, 30)
    self.font = pygame.font.SysFont(None, 48)

    # Prepare the initial score image.
    self.prep_score()
    self.prep_high_score()
    self.prep_level()
    self.prep_gold()
    self.prep_ships()

  def prep_score(self):
    """Turn the score into a rendered image"""
    rounded_score = round(self.stats.score, -1)
    score_str = f"{rounded_score:,}"

    self.score_image = self.font.render(
      score_str, True, self.text_color, self.settings.bg_color
    )

    # Display the score at the top right of the screen.
    self.score_rect = self.score_image.get_rect()
    self.score_rect.right = self.screen_rect.right - 20
    self.score_rect.top = 20

  def prep_high_score(self):
    """Turn the highscore into a rendered image"""
    high_score = round(self.stats.high_score, -1)
    score_str = f"{high_score:,}"
    self.high_score_image = self.font.render(
      score_str, True, self.text_color, self.settings.bg_color
    )

    # Center the score at the top center of the screen.
    self.high_score_rect = self.high_score_image.get_rect()
    self.high_score_rect.centerx = self.screen_rect.centerx
    self.high_score_rect.top = self.score_rect.top

  def prep_level(self):
    """Turn the level into a rendered image"""
    level_str = str(self.stats.level)
    self.level_image = self.font.render(
      level_str, True, self.text_color, self.settings.bg_color
    )

    # Position the level below the score
    self.level_rect = self.level_image.get_rect()
    self.level_rect.right = self.score_rect.right
    self.level_rect.top = self.score_rect.bottom + 12

  def prep_ships(self):
    """Show how many ships are left"""
    self.ships = Group()
    for ship_number in range(self.stats.ships_left):
      ship = Ship(self.ai_game)
      ship.rect.x = 12 + ship_number * ship.rect.width
      ship.rect.y = 12
      self.ships.add(ship)

  def prep_gold(self):
    """Show total gold"""
    gold_str = str(self.stats.gold)
    self.gold_text_image = self.font.render(
      gold_str, True, self.text_color, self.settings.bg_color
    )

    # Position the gold below the highscore
    self.gold_rect = self.gold_text_image.get_rect()
    self.gold_rect.centerx = self.screen_rect.centerx + 8
    self.gold_rect.top = self.high_score_rect.bottom + 12

    # Position gold coin next to score
    self.gold_image = GoldCoin(self.ai_game)
    self.gold_image.rect.right = self.gold_rect.left - 8
    self.gold_image.rect.centery = self.gold_rect.centery

  def _draw_gold(self):
    """Draw gold"""
    self.screen.blit(self.gold_text_image, self.gold_rect)
    self.gold_image.draw_gold_coin()

  def show_score(self):
    """Draw scores, level, ships and gold to the screen"""
    self.screen.blit(self.score_image, self.score_rect)
    self.screen.blit(self.high_score_image, self.high_score_rect)
    self.screen.blit(self.level_image, self.level_rect)
    self._draw_gold()
    self.ships.draw(self.screen)

  def check_high_score(self):
    """Check to see if there is a new high score."""
    if self.stats.score > self.stats.high_score:
      self.stats.high_score = self.stats.score
      self.prep_high_score()