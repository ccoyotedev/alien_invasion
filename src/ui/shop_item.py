from src.ui.card import Card

class ShopItem(Card):
  """A class to manage shop items"""

  def __init__(self, ai_game, name, description, cost, attributes):
    super().__init__(ai_game, name, description, f"Cost {cost}")

    self.ai_game = ai_game
    self.stats = ai_game.stats
    self.settings = ai_game.settings
    self.scoreboard = ai_game.scoreboard

    self.name = name
    self.cost = cost
    self.is_bought = False
    self.attributes = attributes

  def handle_purchase(self):
    """Method for handling purchase"""
    if self.is_bought:
      return
    
    if self.stats.gold < self.cost:
      print("Not enough gold")
      return
    
    self.is_bought = True
    self.stats.gold -= self.cost
    self.scoreboard.prep_gold()

    for attribute in list(self.attributes):
      attribute_value = self.attributes[attribute]
      current_value = getattr(self.settings, attribute)
      setattr(self.settings, attribute, current_value + attribute_value)

    print(f"Bought {self.name}")