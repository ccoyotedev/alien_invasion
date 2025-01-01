from button import Button
from shop_item import ShopItem

class Shop:
  """A class to represent the shop"""

  def __init__(self, ai_game):
    """Initalize shop attributes"""
    self.ai_game = ai_game
    self.screen = ai_game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = ai_game.settings
    self.stats = ai_game.stats

    self.shop_items = []

    self._prep_resume_button()
    self.prep_shop_cards()

  def prep_shop_cards(self):
    """Prepares UI for the shop items"""
    for card_no in range(3):
      shop_item = ShopItem(self.ai_game, f"Card {card_no}", "Description on card", card_no + 1)
      x_coord_start = self.screen_rect.centerx - shop_item.width - 12
      x_coord = x_coord_start + card_no * ( shop_item.width + 12 )
      shop_item.position_card(x_coord, self.screen_rect.centery)
      self.shop_items.append(shop_item)

  def _prep_resume_button(self):
    """Prepares UI of the Resume button"""
    self.resume_button = Button(self.ai_game, "Resume")
    self.resume_button.position_button(self.screen_rect.centerx, self.screen_rect.bottom - self.resume_button.height / 2 - 32)

  def show_shop(self):
    """Display shop UI"""
    self.resume_button.draw_button()
    for shop_item in self.shop_items:
      if not shop_item.is_bought:
        shop_item.draw_card()