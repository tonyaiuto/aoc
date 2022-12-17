#!/usr/bin/env python3
"AOC 2021: day 17"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

SHAPES = """
0123
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


class Rock(object):

  def __init__(self, id, height, width, coords):
    self.id = id
    self.height = height
    self.width = width
    self.coords = coords
    pass

  def __str__(self):
    return str(self)

ROCKS = [
    Rock(id='line',  height=1, width=4, coords=[(0,0), (1,0), (2,0), (3,0)]),
    Rock(id='cross', height=3, width=3, coords=[(1,0), (0,-1), (1,-1), (2,-1), (1,-2)]),
    Rock(id='L',     height=3, width=3, coords=[(2,0), (2,-1), (0,-2), (1,-2), (2,-2)]),
    Rock(id='bar',   height=4, width=1, coords=[(0,0), (0,-1), (0, -2), (0, -3)]),
    Rock(id='box',   height=2, width=2, coords=[(0,0), (1,0), (0,-1), (1,-1)]),
]


class day17(aoc.aoc):

  def __init__(self):
    super(day17, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.rock = 0
    self.grid = gridutils.Grid(default_cell='.')
    self.top = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    self._puffs = self.all_input[0]
    self._next_puff = 0

  def get_puff(self):
    ret = self._puffs[self._next_puff]
    self._next_puff = (self._next_puff + 1) % len(self._puffs)
    return ret

  def show_grid(self, rock, x, y):
    start = max(y, self.top+3)
    for row in aoc.visit_range(start, 0):
      rc = [self.grid.get(x, row) for x in range(7)]
      if row <= y and row > y-rock.height:
        # maybe splice in some of the rock
        rock_row = y - row
        for c in rock.coords:
          if c[1] == -rock_row:
            while x + c[0] >= len(rc):
              rc.append('x')
            rc[x + c[0]] = '@'
      print('%3d |%s|' % (row, ''.join(rc)))

  def part1(self):
    print('===== Start part 1')
    self.reset()

    n_rocks = 0
    for i in range(20):  # 2022
      rock, y = self.drop_rock()
      x = 2
      print('----- new rock', rock.id)
      self.show_grid(rock, x, y)

      while True:
        puff = self.get_puff()
        x, y = self.puff_rock(puff, rock, x, y)
        self.show_grid(rock, x, y)

        # drop it
        if self.collision(rock, x, y-1):
          self.place_rock(rock, x, y)
          self.show_grid(rock, x, y)
          break
        y = y - 1
        #if y - rock.height < 0:
        #  self.place_rock(rock, x, y)
        #  self.show_grid(rock, x, y)
        #  break
        print('drop')
        self.show_grid(rock, x, y)

    return 42

  def puff_rock(self, puff, rock, x, y):
    # Puffs rock and returns new x, y
    print('puff', puff, 'at', x, y, rock.id)
    if puff == '<':
      if x == 0 or self.collision(rock, x-1, y):
        return x, y
      return x-1, y

    assert puff == '>'
    if x + rock.width >= 7 or self.collision(rock, x+1, y):
        return x, y
    return x+1, y

  def place_rock(self, rock, x, y):
    for c in rock.coords:
      self.grid.set(x + c[0], y + c[1], '#')
    self.top = y + 1

  def collision(self, rock, x, y):
    if y - rock.height + 1 < 0:
      print("BOTTOM", y, rock.height)
      return True
    for c in rock.coords:
      if self.grid.get(x + c[0], y + c[1]) == '#':
        print("COLLIDE")
        return True
    return False

  def drop_rock(self):
    rock = ROCKS[self.rock]
    self.rock = (self.rock + 1) % 4
    # rock & 
    return rock, self.top + 3 + rock.height - 1


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day17.sample_test("""
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""", expect1=3068, expect2=None)


if __name__ == '__main__':
  day17.run_and_check('input.txt', expect1=None, expect2=None)
