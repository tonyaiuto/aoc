#!/usr/bin/env python3
"AOC 2025: day 04"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

class day04(aoc.aoc):

  def __init__(self):
    super(day04, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.wall = gridutils.Grid(ignore='.')

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    self.wall.add_row(line)

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()
    # self.wall.print()
    ret = 0
    for r,c in self.wall.live_cells():
      n = 0
      for ri, ci in gridutils.DIRS8:
        if '@' == self.wall.get(r+ri, c+ci):
          n += 1
          if n >= 4:
            break
      if n < 4:
        ret += 1
        # print(r, c)
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    found_one = True
    while found_one:
      found_one = False
      for x, y in list(self.wall.live_cells()):
        n = 0
        for xi, yi in gridutils.DIRS8:
          # print(x+xi, y+yi, self.wall.get(x+xi, y+yi))
          if '@' == self.wall.get(x+xi, y+yi):
            n += 1
            if n >= 4:
              break
        if n < 4:
          ret += 1
          found_one = True
          self.wall.unset(x, y)
    return ret


day04.sample_test("""
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""", expect1=13, expect2=43)


if __name__ == '__main__':
  day04.run_and_check('input.txt', expect1=1457, expect2=8310)
