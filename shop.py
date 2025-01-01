from button import Button

class Shop:
  """A class to represent the shop"""

  def __init__(self, ai_game):
    """Initalize shop attributes"""
    self.ai_game = ai_game
    self.screen = ai_game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = ai_game.settings
    self.stats = ai_game.stats

    self._prep_resume_button()

  def _prep_resume_button(self):
    """Prepares UI of the Resume button"""
    self.resume_button = Button(self.ai_game, "Resume")
    self.resume_button.position_button(self.screen_rect.centerx, self.screen_rect.bottom - 32)
    

  def show_shop(self):
    """Display shop UI"""
    self.resume_button.draw_button()