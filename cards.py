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
  def __init__(self, idx, sides):
    self.idx = idx
    self.sides = [CardSymbol(side_info) for side_info in sides]

  @property
  def num(self):
    return self.idx + 1

  def get_side(self, side, rot):
    return self.sides[(side+rot)%4]

  def rotated(self, rot):
    return RotatedCard(self, rot)

  def short(self):
    return f"{self.num}"

  def __str__(self):
    return f"Card {self.short()}: {','.join([str(self.get_side(idx, 0)) for idx in range(0,4)])}"

  def __repr__(self):
    return f"<{str(self)}>"

class RotatedCard:
  def __init__(self, card, rot):
    self.card = card
    self.rot = rot % 4

  @property
  def ang(self):
    return f"{self.rot*90}°"

  def get_side(self, side):
    return self.card.get_side(side, self.rot)

  def find_valid_neighbors(self, side: int, pool: set[Card]):
    """Find all Cards in `pool` that can neighbor this card on the given side"""
    match_sym = self.get_side(side)
    # The other card needs to have it on the opposite side
    match_side = (side + 2) % 4
    for card in pool:
      for (target_side, sym) in enumerate(card.sides):
        if sym.matches(match_sym):
          # To get the rotation, subtract target side from unrotated side
          # So if we find it at the top (side 0) and need it at the left (side 3)
          # We need to rotate it 3 (3-0)
          yield RotatedCard(card, (target_side - match_side)%4)

  def short(self):
    return f"{self.card.num}@{self.ang}"

  def __str__(self):
    return f"Card {self.short()}: {','.join([str(self.get_side(idx)) for idx in range(0,4)])}"

  def __repr__(self):
    return f"<{str(self)}>"

  def __eq__(self, other):
    return self.card == other.card and self.rot == other.rot

  def __hash__(self):
    return hash((self.card, self.rot))

class CardRenderer:
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
      sides = [(str(card.get_side(n)), '═' if n%2 == 0 else '║') for n in range(4)]
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
