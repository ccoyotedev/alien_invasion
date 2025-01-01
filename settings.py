class Settings:
  """A class to store all settings for Alien Invasion"""

  def __init__(self):
    """Initialise the game settings"""
    # Screen settings
    self.screen_width = 1200
    self.screen_height = 800
    self.bg_color = (230, 230, 230)

    # Ship settings
    self.ship_limit = 3

    # Bullet settings
    self.bullet_height = 15
    self.bullet_color = (60, 60, 60)
    self.bullets_allowed = 5

    # Alien settings
    self.fleet_drop_speed = 10

    # Gold settings
    self.gold_color = (255, 255, 0)
    self.gold_radius = 8

    # How quickly the game speeds up
    self.speedup_scale = 1.5
    # How quickly the alien point values increase
    self.score_scale = 1.5

    self.initialize_dynamic_settings()

  def initialize_dynamic_settings(self):
    """Initialize settings that change throughout the game"""
    self.ship_speed = 2.0
    self.bullet_speed = 10
    self.bullet_width = 500
    self.alien_speed = 2.0
    self.max_fleet_rows = 3
    # fleet_direction of 1 represents right; -1 represents left
    self.fleet_direction = 1

    # Scoring settings
    self.alien_points = 50

    # Gold settings
    self.gold_drop_chance = 0.2
    self.gold_drop_speed = 2.5

  def increase_speed(self):
    """Increase speed settings."""
    self.ship_speed *= self.speedup_scale
    self.bullet_speed *= self.speedup_scale
    self.alien_speed *= self.speedup_scale
    self.alien_points = int(self.alien_points * self.score_scale)
