from cards import Card, RotatedCard

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

def find_valid_corner(above_card: RotatedCard, left_card: RotatedCard, pool: set[Card]):
  valid_above = set(above_card.find_valid_neighbors(2, pool))
  valid_left = set(left_card.find_valid_neighbors(1, pool))
  yield from valid_above.intersection(valid_left)

def rc_to_idx(row, col):
  return row*3+col

def valid_next(chosen: list[RotatedCard], remaining: set[Card]):
  next_pos = len(chosen)
  row = next_pos // 3
  col = next_pos % 3

  if row == 0 and col == 0:
    # First card, all are possible
    for card in remaining:
      for rot in range(4):
        yield card.rotated(rot)
  elif row == 0:
    # First row, only constraint is left
    yield from chosen[rc_to_idx(row, col-1)].find_valid_neighbors(1, remaining)
  elif col == 0:
    # First col, only constraint is above
    yield from chosen[rc_to_idx(row-1, col)].find_valid_neighbors(2, remaining)
  else:
    # Two neighbors
    yield from find_valid_corner(
      chosen[rc_to_idx(row-1, col)],
      chosen[rc_to_idx(row, col-1)],
      remaining
    )

def find_valid_set(chosen, remaining, target):
  if(len(chosen) == target):
    yield chosen

  for candidate in valid_next(chosen, remaining):
    yield from find_valid_set(chosen + [candidate], remaining.difference([candidate.card]), target)

def find_remaining(chosen, pool, target):
  yield from find_valid_set(chosen, pool.difference([rc.card for rc in chosen]), target)

if __name__ == "__main__":
  set8 = find_valid_set([], set(cards), 8)

  for chosen in set8:
    print("Valid set of 8:")
    cardsize=15
    for row in range(3):
      for line in range(cardsize):
        for col in range(3):
          try:
            print(chosen[rc_to_idx(row, col)].render_line(cardsize, line), end="")
          except IndexError:
            pass
        print("")

    print("Valid 9th cards:")
    candidates = list(find_remaining(chosen, set(cards), 9))
    if(len(candidates) == 0):
      print("None")
    else:
      for c in candidates:
        c.render()
