from typing import Self

class CardSymbol:
  """One of the half-symbols on the card"""
  def __init__(self, side_info: str):
    (sym, half) = side_info.split('_')
    self.sym = sym
    self.half = half

  def matches(self, other: Self) -> bool:
    """Is `other` the other half of this symbol?"""
    return (other.sym == self.sym and other.half != self.half)

  def __str__(self):
    return f"{self.sym}_{self.half}"

  def __repr__(self):
    return f"<{str(self)}>"

class Card:
  """Represents a non-played card, essentially just an index and an ordered set of symbols"""
  def __init__(self, idx, sides):
    self.idx = idx
    self.sides = [CardSymbol(side_info) for side_info in sides]
    self.num_sides = len(self.sides)

  @property
  def num(self) -> int:
    return self.idx + 1

  def get_side(self, side, rot) -> CardSymbol:
    return self.sides[(side+rot)%self.num_sides]

  def rotated(self, rot):
    return RotatedCard(self, rot)

  def short(self):
    return f"{self.num}"

  def __str__(self):
    return f"Card {self.short()}: {','.join([str(self.get_side(idx, 0)) for idx in range(self.num_sides)])}"

  def __repr__(self):
    return f"<{str(self)}>"

class RotatedCard:
  """A Card that has been positioned, and thus has a fixed rotation"""
  def __init__(self, card: Card, rot: int):
    self.card = card
    self.rot = rot % self.num_sides

  @property
  def ang(self):
    return f"{self.rot*90}°"

  @property
  def num_sides(self):
    return self.card.num_sides

  def get_side(self, side):
    return self.card.get_side(side, self.rot)

  def find_valid_neighbors(self, side: int, pool: set[Card]):
    """Find all Cards in `pool` that can neighbor this card on the given side"""
    match_sym = self.get_side(side)
    # The other card needs to have the matching symbol on the opposite side
    match_side = (side + self.num_sides//2) % self.num_sides
    for card in pool:
      for (cur_side, sym) in enumerate(card.sides):
        if sym.matches(match_sym):
          # To get the rotation, subtract target side from unrotated side
          # Ex: if we find a match at the top (side 0) and need it positioned
          # at the left (side 3) then we need to rotate it 3 (3-0)
          yield RotatedCard(card, (cur_side - match_side)%self.num_sides)

  def short(self):
    return f"{self.card.num}@{self.ang}"

  def __str__(self):
    return f"Card {self.short()}: {','.join([str(self.get_side(idx)) for idx in range(self.num_sides)])}"

  def __repr__(self):
    return f"<{str(self)}>"

  def __eq__(self, other):
    return self.card == other.card and self.rot == other.rot

  def __hash__(self):
    return hash((self.card, self.rot))

class CardRenderer:
  """Very silly renderer for cards and cardsets"""
  def __init__(self, sidelen: int):
    self.sidelen = sidelen
    self.prerendered = {}

  def renderCards(self, cards: list[RotatedCard]):
    for row in range(3):
      for line in range(self.sidelen):
        for col in range(3):
          try:
            print(self.render_line(cards[row*3+col], line), end="")
          except IndexError:
            pass
        print("")


  def borders(self, card):
    if card.card.num not in self.prerendered:
      pad = self.sidelen - 2
      sides = [(str(card.get_side(n)), '═' if n%2 == 0 else '║') for n in range(card.num_sides)]
      self.prerendered[card.card.num] = [f"{s:{char}^{pad}}" for (s, char) in sides]
    return self.prerendered[card.card.num]

  def render_line(self, card: RotatedCard, line: int):
    borders = self.borders(card)
    pad = self.sidelen - 2
    if line == 0:
      return f"╔{borders[0]}╗"
    if line == self.sidelen-1:
      return f"╚{borders[2]}╝"
    else:
      idx = line-1
      center = pad//2
      if idx == center:
        caption = f"Card {card.card.num}"
      elif idx == center+1:
        caption = f"Rot {card.ang}"
      else:
        caption = ""

      return f"{borders[3][idx]}{caption:^{pad}}{borders[1][idx]}"

  def render(self, card: RotatedCard):
    for idx in range(self.sidelen):
      print(self.render_line(card, idx))
