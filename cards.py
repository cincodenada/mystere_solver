import typing

class CardSymbol:
  def __init__(self, side_info):
    (sym, half) = side_info.split('_')
    self.sym = sym
    self.half = half

  def matches(self, other):
    return (other.sym == self.sym and other.half != self.half)

  def __str__(self):
    return f"{self.sym}_{self.half}"

  def __repr__(self):
    return f"<{str(self)}>"

class Card:
  def __init__(self, num, sides):
    self.num = num
    self.sides = [CardSymbol(side_info) for side_info in sides]

  def get_side(self, side, rot):
    return self.sides[(side+rot)%4]

  def rotated(self, rot):
    return RotatedCard(self, rot)

  def __str__(self):
    return f"Card {self.num}: {','.join([str(self.get_side(idx, 0)) for idx in range(0,4)])}"

  def __repr__(self):
    return f"<{str(self)}>"

class RotatedCard:
  def __init__(self, card, rot):
    self.card = card
    self.rot = rot

  def get_side(self, side):
    return self.card.get_side(side, self.rot)

  def find_valid_neighbors(self, side: int, pool: set[Card]):
    match_sym = self.get_side(side)
    # The other card needs to have it on the opposite side
    match_side = (side + 2) % 4
    for card in enumerate(pool):
      for (target_side, sym) in enumerate(card.sides):
        if sym.matches(match_sym):
          # To get the rotation, subtract target side from unrotated side
          # So if we find it at the top (side 0) and need it at the left (side 3)
          # We need to rotate it 3 (3-0)
          yield RotatedCard(card, (match_side - target_side)%4)

  def __str__(self):
    return f"Card {self.card.num}@{self.rot}: {','.join([str(self.get_side(idx)) for idx in range(0,4)])}"

  def __repr__(self):
    return f"<{str(self)}>"
