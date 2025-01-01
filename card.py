import pygame.font

class Card:
  """A class to build cards for the game"""

  def __init__(self, ai_game, title, description):
    """Initialize card attributes"""
    self.screen = ai_game.screen
    self.screen_rect = self.screen.get_rect()

    self.width, self.height = 250, 375
    self.card_color = (255, 255, 255)
    self.text_color = (0, 0, 0)

    title_size = 32
    description_size = 24
    self.title_font = pygame.font.SysFont(None, title_size)
    self.description_font = pygame.font.SysFont(None, description_size)

    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.center = self.screen_rect.center

    self._prep_text(title, description)

  def _prep_text(self, title, description):
    """Turn text into a rendered image and center text on the card"""
    self.title_image = self.title_font.render(title, True, self.text_color, self.card_color)
    self.title_image_rect = self.title_image.get_rect()
    
    self.description_image = self.description_font.render(description, True, self.text_color, self.card_color)
    self.description_image_rect = self.description_image.get_rect()
    
    self._position_text()


  def _position_text(self):
    """Position text on the card"""
    self.title_image_rect.centerx = self.rect.centerx
    self.title_image_rect.top = self.rect.top + 16
    self.description_image_rect.center = self.rect.center


  def draw_card(self):
    """Draw blank card and then draw text"""
    self.screen.fill(self.card_color, self.rect)
    self.screen.blit(self.title_image, self.title_image_rect)
    self.screen.blit(self.description_image, self.description_image_rect)

  def position_card(self, x_coord, y_coord):
    """Position card on screen"""
    self.rect.centerx = x_coord
    self.rect.centery = y_coord

    self._position_text()