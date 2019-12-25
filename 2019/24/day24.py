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

  def print(self):
    print('cycle', self.cycles, 'bio', self.bio)
    for y in range(self.margin, self.height+self.margin):
      x = y * (self.width + self.margin * 2) + self.margin
      print(''.join('#' if c == 1 else '.'
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

  def __init__(self):
    super(Eris2, self).__init__()
    self.cells = [0] * (self.height * self.width)
    self.ratings = set()
    self.inner = None
    self.outer = None

  def get_cell(self, cell_no):
    return -1

  def cycle(self):
    self.cycles += 1
    nxt = [0] * (self.height * self.width)
    up = self.outer_count(8)
    down = self.outer_count(18)
    left = self.outer_count(12)
    right = self.outer_count(14)

    # row 1
    for ci in range(25):
      # add left
      if ci % self.width == 0:
        nxt[x] += left
      elif ci != 14:
        nxt[x] += self.cells[ci - 1]
      else:
        print('tbd: do inner')

      # add right
      if ci % self.width == 4:
        nxt[x] += right
      elif ci != 12:
        nxt[x] += self.cells[ci + 1]
      else:
        print('tbd: do inner')

      # Add row above
      if ci < 5:
        nxt[x] += up
      elif ci != 18:
        nxt[x] += self.cells[x-self.width]
      else:
        print('tbd: do inner')

      # Add row below
      if ci >= 20:
        nxt[x] += up
      elif ci != 8:
        nxt[x] += self.cells[x+self.width]
      else:
        print('tbd: do inner')

      if self.cells[ci] == 1:
        nxt[ci] = 1 if nxt[base+c] == 1 else 0
      else:
        nxt[ci] = 1 if nxt[base+c] in [1, 2]  else 0

    self.outer.cycle()
    # self.inner.cycle()
    self.cells = nxt
    return self.calc_bio()

  def outer_count(self, cell):
    if not self.outer:
      return 0
    return self.outer.cells[cell]

  def inner_count(self, cell):
    if not self.inner:
      return 0
    return self.inner.cells[cell]

  def calc_bio(self):
    bio = 0
    for pos in range(self.height * self.width - 1, -1, -1):
      bio = bio * 2 + self.cells[pos]
    self.bio = bio
    if bio in self.ratings:
      print('======== bio appears twice', bio)
      return False
    self.ratings.add(bio)
    return True


def test_part2(quiet=True):
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
      cells.cycle2()
      cells.print()
  do_part2(cells)
  assert 2129920 == cells.bio


def part1():
  cells = Eris()
  cells.load('input_24.txt')
  cells.run()
  print('part1:', cells.bio)
  assert 30446641 == cells.bio


if __name__ == '__main__':
  test_part1(quiet=True)
  part1()
  # test_part2(quiet=False)

