#!/usr/bin/env python3

import textwrap

class Eris(object):

  bit_order = [
       8, 9, 10, 11, 12,
      15, 16, 17, 18, 19,
      22, 23, 24, 25, 26,
      29, 30, 31, 32, 33,
      36, 37, 38, 39, 40]
  bit_order.reverse()

  def __init__(self):
    self.width = 5
    self.height = 5
    self.cycles = 0
    self.ratings = set()
    self.bio = 0
    # print(Eris.bit_order)

  def load(self, path):
    with open(path, 'r') as inp:
      self.load_from_string(inp.read())

  def load_from_string(self, s):
    self.cells = [0] * 8
    for c in textwrap.dedent(s).strip():
      if c == '\n':
        self.cells.append(0)
        self.cells.append(0)
      elif c == '#':
        self.cells.append(1)
      else:
        self.cells.append(0)
    self.cells.append(0)
    for _ in range(7):
      self.cells.append(0)
    self.calc_bio()

  def print(self):
    print('cycle', self.cycles, 'bio', self.bio)
    for y in range(1, self.height+1):
      print(''.join('#' if c == 1 else '.'
          for c in self.cells[y*(self.width+2)+1:((y+1)*(self.width+2)-1)]))

  def cycle(self):
    # A bug dies (becoming an empty space) unless there is exactly one
    # bug adjacent to it.
    # An empty space becomes infested with a bug if
    # exactly one or two bugs are adjacent to it.
    # 01234
    # 56789
    pow = 1

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


def do_part1(cells):
  while cells.cycle():
    pass


def bio_test(expect, pattern, label=''):
  cells = Eris()
  cells.load_from_string(pattern)
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
  do_part1(cells)
  assert 2129920 == cells.bio


def part1():
  cells = Eris()
  cells.load('input_24.txt')
  do_part1(cells)
  print('part1:', cells.bio)
  assert 30446641 == cells.bio


if __name__ == '__main__':
  test_part1(quiet=True)
  part1()
