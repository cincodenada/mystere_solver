from cards import Card, RotatedCard, CardRenderer

# Cards, with sides clockwise from top
sidelist = [
  [ 'trapese_a', 'hair_a', 'bug_a', 'flower_b' ],
  [ 'bug_b', 'trapese_a', 'hair_b', 'flower_b' ],
  [ 'trapese_a', 'hair_a', 'flower_a', 'bug_a' ],
  [ 'flower_b', 'hair_a', 'trapese_a', 'bug_a' ],
  [ 'hair_b', 'trapese_a', 'bug_b', 'flower_a' ],
  [ 'trapese_b', 'hair_a', 'bug_a', 'trapese_a' ],
  [ 'trapese_b', 'bug_a', 'bug_b', 'flower_a' ],
  [ 'hair_a', 'bug_b', 'flower_a', 'hair_b' ],
  [ 'flower_a', 'trapese_b', 'flower_a', 'hair_b' ]
]

# Split them for easier handling
cards = [Card(num, sides) for num, sides in enumerate(sidelist)]

def rc_to_idx(row, col):
  """Helper to map a row/col to a linear (flat) array index"""
  return row*3+col

def find_valid_corner(above_card: RotatedCard, left_card: RotatedCard, pool: set[Card]):
  """Find all valid cards in `pool` that fit both below `above_card` and to the right of `left_card`"""
  valid_above = set(above_card.find_valid_neighbors(2, pool))
  valid_left = set(left_card.find_valid_neighbors(1, pool))
  yield from valid_above.intersection(valid_left)

def valid_next(chosen: list[RotatedCard], remaining: set[Card]):
  """Find all valid cards for the 'next' slot (left-to-right, top-to-bottom)

  chosen -- List of previously-chosen RotatedCards for this branch
  remaining -- Set of cards not yet chosen
  """

  next_pos = len(chosen)
  row = next_pos // 3
  col = next_pos % 3

  if row == 0 and col == 0:
    # First card, all rotations of all cards are possible
    for card in remaining:
      for rot in range(4):
        yield card.rotated(rot)
  elif row == 0:
    # First row, only constraint is to our left
    yield from chosen[rc_to_idx(row, col-1)].find_valid_neighbors(1, remaining)
  elif col == 0:
    # First col, only constraint is above us
    yield from chosen[rc_to_idx(row-1, col)].find_valid_neighbors(2, remaining)
  else:
    # Elsewise, we have two known neighbors, so use our helper method
    yield from find_valid_corner(
      chosen[rc_to_idx(row-1, col)],
      chosen[rc_to_idx(row, col-1)],
      remaining
    )

def find_valid_set(chosen, remaining, target):
  """Recursively find all valid sets of `target` cards

  chosen -- List of RotatedCards already chosen
  remaining -- Set of Cards not yet chosen
  target -- Number of cards to choose
  """
  if(len(chosen) == target):
    yield chosen

  for candidate in valid_next(chosen, remaining):
    yield from find_valid_set(chosen + [candidate], remaining.difference([candidate.card]), target)

def find_remaining(chosen, pool, target):
  """Wrapper for resuming a partially-completed search without having to manually winnow `pool`"""
  yield from find_valid_set(chosen, pool.difference([rc.card for rc in chosen]), target)

if __name__ == "__main__":
  sets = list(find_valid_set([], set(cards), 9))

  for chosen in sets:
    for row in range(3):
      print(', '.join([c.short() for c in chosen[row*3:(row+1)*3]]))
    print("")

  for chosen in sets:
    print("Valid set of 9:")
    renderer = CardRenderer(15)
    renderer.renderCards(chosen)
