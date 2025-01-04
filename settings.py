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

    # Alien settings
    self.fleet_drop_speed = 10
    self.max_fleet_rows = 8

    # Gold settings
    self.gold_color = (255, 255, 0)
    self.gold_radius = 8

    # How quickly the game speeds up
    self.speedup_scale = 1.15
    # How quickly the alien point values increase
    self.score_scale = 1.5

    self.initialize_dynamic_settings()

  def initialize_dynamic_settings(self):
    """Initialize settings that change throughout the game"""
    self.ship_speed = 2.5
    self.bullet_speed = 5
    self.bullet_width = 5
    self.bullets_allowed = 3

    self.alien_speed = 2.0
    self.fleet_rows = 2
    # fleet_direction of 1 represents right; -1 represents left
    self.fleet_direction = 1

    # Scoring settings
    self.alien_points = 50

    # Gold settings
    self.gold_drop_chance = 0.2
    self.gold_drop_speed = 2.5
    self.gold_pickup_radius = 100

  def increase_wave_difficulty(self):
    """Increase settings to make game harder"""
    self.alien_speed *= self.speedup_scale
    self.alien_points = int(self.alien_points * self.score_scale)
    self.fleet_rows = min(self.max_fleet_rows, self.fleet_rows + 1)
