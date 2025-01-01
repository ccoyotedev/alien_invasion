from card import Card

class ShopItem(Card):
  """A class to manage shop items"""

  def __init__(self, ai_game, name, description, cost):
    super().__init__(ai_game, name, description, f"Cost {cost}")

    self.ai_game = ai_game
    self.stats = ai_game.stats
    self.scoreboard = ai_game.scoreboard

    self.name = name
    self.cost = cost
    self.is_bought = False

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
    print(f"Bought {self.name}")