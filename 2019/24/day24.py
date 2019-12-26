#!/usr/bin/env python3

import textwrap

class Grid(object):

  def __init__(self):
    self.width = 5
    self.height = 5
    self.cells = []
    self.cycles = 0
    self.bio = 0
    self.margin = 0
    self.depth = 0
    self.in_cycle = False

  def load(self, path):
    with open(path, 'r') as inp:
      self.load_from_string(inp.read())

  def load_from_string(self, s):
    self.cells = [0] * (self.margin * (self.width + 3))
    for c in textwrap.dedent(s).strip():
      if c == '\n':
        for _ in range(self.margin * 2):
          self.cells.append(0)
      elif c == '#':
        self.cells.append(1)
      else:
        self.cells.append(0)
    self.cells.extend([0] * (self.margin * (self.width + 3)))
    self.calc_bio()

  def print(self, indent=0):
    sp = ' ' * indent
    print(sp + 'cycle', self.cycles, 'bio', self.bio, 'depth', self.depth)
    for y in range(self.margin, self.height+self.margin):
      x = y * (self.width + self.margin * 2) + self.margin
      print(sp + ''.join('#' if c == 1 else '.'
          for c in self.cells[x:(x + self.width - self.margin)]))

  def run(self):
    while self.cycle():
      pass



class Eris(Grid):
  # part 1

  bit_order = [
       8, 9, 10, 11, 12,
      15, 16, 17, 18, 19,
      22, 23, 24, 25, 26,
      29, 30, 31, 32, 33,
      36, 37, 38, 39, 40]
  bit_order.reverse()

  def __init__(self):
    super(Eris, self).__init__()
    self.margin = 1
    self.ratings = set()

  def cycle(self):
    # A bug dies (becoming an empty space) unless there is exactly one
    # bug adjacent to it.
    # An empty space becomes infested with a bug if
    # exactly one or two bugs are adjacent to it.
    # 01234
    # 56789
    self.cycles += 1
    nxt = [0] * 49
    for y in range(1, self.height+1):
      base = y * 7 + 1
      for c in range(5):
        nxt[base+c] = (self.cells[base+c-1] + self.cells[base+c+1] +
                       self.cells[base+c-7] + self.cells[base+c+7])
        if self.cells[base+c] == 1:
          nxt[base+c] = 1 if nxt[base+c] == 1 else 0
        else:
          nxt[base+c] = 1 if nxt[base+c] in [1, 2]  else 0
    self.cells = nxt
    return self.calc_bio()

  def calc_bio(self):
    bio = 0
    for i, bit in enumerate(Eris.bit_order):
      bio = bio * 2 + self.cells[bit]
      # print(25-i, bit, self.cells[bit], bio)
    self.bio = bio
    if bio in self.ratings:
      print('======== bio appears twice', bio)
      return False
    self.ratings.add(bio)
    return True


def bio_test(expect, pattern, label=''):
  cells = Eris()
  cells.load_from_string(pattern)
  cells.print
  if expect != cells.bio:
    print('expect', expect, 'got', cells.bio, label)
  assert expect == cells.bio

  cells = Eris2()
  cells.load_from_string(pattern)
  cells.print
  if expect != cells.bio:
    print('expect', expect, 'got', cells.bio, label)
  assert expect == cells.bio



def test_part1(quiet=True):
  bio_test(1, """\
      #....
      .....
      .....
      .....
      .....
      """)
  bio_test(17, """\
      #...#
      .....
      .....
      .....
      .....
      """)
  bio_test(49, """\
      #...#
      #....
      .....
      .....
      .....
      """)
  bio_test(2 ** 10 + 1, """\
      #....
      .....
      #....
      .....
      .....
      """, label='2**10+1')
  bio_test(2 ** 14 + 1, """\
      #....
      .....
      ....#
      .....
      .....
      """, label='2**14+1')
  bio_test(2 ** 15 + 1, """\
      #....
      .....
      .....
      #....
      .....
      """, label='2**15+1')
  bio_test(2 ** 18 + 1, """\
      #....
      .....
      .....
      ...#.
      .....
      """, label='2**18+1')
  bio_test(2 ** 20 + 1, """\
      #....
      .....
      .....
      .....
      #....
      """, label='2**20+1')
  bio_test(2 ** 21 + 1, """\
      #....
      .....
      .....
      .....
      .#...
      """, label='2**21+1')
  bio_test(2129920, """\
      .....
      .....
      .....
      #....
      .#...
      """)
  bio_test(2 ** 24 + 2, """\
      .#...
      .....
      .....
      .....
      ....#
      """, label='2**24+2')

  cells = Eris()
  cells.load_from_string("""\
      ....#
      #..#.
      #..##
      ..#..
      #....
      """)
  if not quiet:
    cells.print()
    for _ in range(4):
      cells.cycle()
      cells.print()
  cells.run()
  assert 2129920 == cells.bio


class Eris2(Grid):

  def __init__(self, depth=0, inner=None, outer=None):
    super(Eris2, self).__init__()
    self.cells = [0] * (self.height * self.width)
    self.depth = depth
    self.inner = inner
    self.outer = outer

  def get_cell(self, cell_no):
    return -1

  def cycle(self):
    if self.in_cycle:
      return
    self.in_cycle = True
    self.cycles += 1
    nxt = [0] * (self.height * self.width)

    # row 1
    for ci in range(25):
      # add left
      if ci % self.width == 0:
        nxt[ci] += self.outer_count(11)
      elif ci == 13:
        nxt[ci] += self.inner_count(13)
      else:
        nxt[ci] += self.cells[ci - 1]

      # add right
      if ci % self.width == 4:
        nxt[ci] += self.outer_count(13)
      elif ci == 11:
        nxt[ci] += self.inner_count(11)
      else:
        nxt[ci] += self.cells[ci + 1]

      # Add row above
      if ci < 5:
        nxt[ci] += self.outer_count(7)
      elif ci == 17:
        nxt[ci] += self.inner_count(17)
      else:
        nxt[ci] += self.cells[ci-self.width]

      # Add row below
      if ci >= 20:
        nxt[ci] += self.outer_count(17)
      elif ci == 7:
        nxt[ci] += self.inner_count(7)
      else:
        nxt[ci] += self.cells[ci+self.width]

      if self.cells[ci] == 1:
        nxt[ci] = 1 if nxt[ci] == 1 else 0
      else:
        nxt[ci] = 1 if nxt[ci] in [1, 2]  else 0
    nxt[12] = 0

    self.provisonal_innner()
    self.provisonal_outer()
    self.cells = nxt
    # self.calc_bio()
    self.in_cycle = False

  def outer_count(self, cell):
    if not self.outer:
      return 0
    return self.outer.cells[cell]

  def inner_count(self, cell):
    if not self.inner:
      return 0
    return self.inner.count_inner_edge(cell)

  def count_inner_edge(self, cell):
    if cell == 7:
      # top row
      return sum(self.cells[0:5])
    elif cell == 11:
      # left col
      return sum(self.cells[ci] for ci in [0, 5, 10, 15, 20])
    elif cell == 13:
      # right col
      return sum(self.cells[ci] for ci in [4, 9, 14, 19, 24])
    elif cell == 17:
      # bottom row
      return sum(self.cells[20:25])
    else:
      raise Exception('asked for wrong innter count %d' % cell)

  def provisonal_innner(self):
    if not self.inner:
      for cell in (7, 11, 13, 17):
        if self.cells[cell]:
           self.inner = Eris2(depth=self.depth+1, outer=self)
           # print('\nMaking inner from this:')
           # self.print(indent=4)
           break
    if self.inner and not self.inner.in_cycle:
      self.inner.cycle()
      # self.inner.print(indent=7)

  def provisonal_outer(self):
    if not self.outer:
      for cell in (7, 11, 13, 17):
        n_live = self.count_inner_edge(cell)
        if n_live in (1, 2):
           self.outer = Eris2(depth=self.depth-1, inner=self)
           # print('\nMaking outer for form')
           # self.print(indent=4)
           break
    if self.outer and not self.outer.in_cycle:
      self.outer.cycle()
      # self.outer.print(indent=8)

  def count_bugs(self):
    bugs = 0
    if self.depth >= 0 and self.inner:
      bugs += self.inner.count_bugs()
    if self.depth <= 0 and self.outer:
      bugs += self.outer.count_bugs()
    bugs += sum([c for c in self.cells])
    return bugs

  def calc_bio(self):
    bio = 0
    for pos in range(self.height * self.width - 1, -1, -1):
      bio = bio * 2 + self.cells[pos]
    self.bio = bio
    """
    if bio in self.ratings:
      print('======== bio appears twice', bio)
      return False
    self.ratings.add(bio)
    """
    return True


def test_part2(quiet=True):
  cells = Eris2()
  cells.load_from_string("""\
      ....#
      #..#.
      #..##
      ..#..
      #....
      """)
  if not quiet:
    cells.print()
    for _ in range(10):
      cells.cycle()
      cells.print()
  bugs = cells.count_bugs()
  print('bugs', bugs)
  assert 99 == bugs


def part1():
  cells = Eris()
  cells.load('input_24.txt')
  cells.run()
  print('part1:', cells.bio)
  assert 30446641 == cells.bio

def part2():
  cells = Eris2()
  cells.load('input_24.txt')
  for _ in range(200):
    cells.cycle()
  bugs = cells.count_bugs()
  print('part2, bugs', bugs)
  # 2057 is too high

if __name__ == '__main__':
  test_part1(quiet=True)
  part1()
  test_part2(quiet=False)
  part2()

