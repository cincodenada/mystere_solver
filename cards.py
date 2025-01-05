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

  def __str__(self):
    return f"Card {self.num}: {','.join([str(self.get_side(idx, 0)) for idx in range(0,4)])}"

  def __repr__(self):
    return f"<{str(self)}>"

class RotatedCard:
  def __init__(self, card, rot):
    self.card = card
    self.rot = rot % 4
    self.rendered = None
    self.sidelen = None

  @property
  def ang(self):
    return f"{self.rot*90}°"

  def get_side(self, side):
    return self.card.get_side(side, self.rot)

  def find_valid_neighbors(self, side: int, pool: set[Card]):
    match_sym = self.get_side(side)
    # The other card needs to have it on the opposite side
    match_side = (side + 2) % 4
    for card in pool:
      for (target_side, sym) in enumerate(card.sides):
        if sym.matches(match_sym):
          # To get the rotation, subtract target side from unrotated side
          # So if we find it at the top (side 0) and need it at the left (side 3)
          # We need to rotate it 3 (3-0)
          yield RotatedCard(card, (match_side - target_side)%4)

  def render_line(self, sidelen, line):
    borders = self.borders(sidelen)
    pad = sidelen - 2
    if line == 0:
      return f"╔{borders[0]}╗"
    if line == sidelen-1:
      return f"╚{borders[2]}╝"
    else:
      idx = line-1
      caption = f"Card {self.card.num}" if idx == pad//2 else ""
      return f"{borders[3][idx]}{caption:^{pad}}{borders[1][idx]}"

  def borders(self, sidelen):
    if self.sidelen != sidelen or self.rendered is None:
      self.sidelen = sidelen
      pad = self.sidelen - 2
      sides = [(str(self.get_side(n)), '═' if n%2 == 0 else '║') for n in range(4)]
      self.rendered = [f"{s:{char}^{pad}}" for (s, char) in sides]
    return self.rendered

  def render(self, sidelen, offset=0):
    for idx in range(sidelen):
      print(self.render_line(sidelen, idx))

  def __str__(self):
    return f"Card {self.card.num}@{self.ang}: {','.join([str(self.get_side(idx)) for idx in range(0,4)])}"

  def __repr__(self):
    return f"<{str(self)}>"

  def __eq__(self, other):
    return self.card == other.card and self.rot == other.rot

  def __hash__(self):
    return hash((self.card, self.rot))
