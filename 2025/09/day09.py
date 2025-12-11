#!/usr/bin/env python3
"AOC 2025: day 09"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

def area(p1, p2):
  return abs(p1.x - p2.x +1) * abs(p1.y - p2.y +1)


class day09(aoc.aoc):

  def __init__(self):
    super(day09, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.reds = []
    self.by_x = defaultdict(set)
    self.by_y = defaultdict(set)

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    xy = [int(n) for n in line.split(',')]
    pos = gridutils.Pos(x=xy[0], y=xy[1])
    self.by_x[pos.x].add(pos)
    self.by_y[pos.y].add(pos)
    self.reds.append(pos)

  def post_load(self):
    self.hlines = []
    self.vlines = []
    first = self.reds[0]
    last = first
    for pos in self.reds[1:]:
      if last.x == pos.x:
        self.hlines.append(pos.x)
      else:
        assert last.y == pos.y
        self.vlines.append(pos.y)
      last = pos
    if first.x == last.x:
      self.hlines.append(first.x)
    else:
      self.vlines.append(first.y)
    self.hlines = sorted(self.hlines)
    self.vlines = sorted(self.vlines)


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.doing_sample:
      print(self.reds)
    max_area = -1
    for i, red in enumerate(self.reds):
      for other in self.reds[i+1:]:
        a = area(red, other)
        if a > max_area:
          max_area = a

    return max_area


  def part2(self):
    print('===== Start part 2')
    self.reset()
    if self.doing_sample:
      print("H lines", self.hlines)
      print("V lines", self.vlines)
    max_area = -1
    for corner in enumerate(self.reds):
      for samex
      for other in self.reds[i+1:]:
        a = area(red, other)
        if a > max_area:
          max_area = a

    return max_area


    return 42


day09.sample_test("""
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""", expect1=50, expect2=24)


if __name__ == '__main__':
  day09.run_and_check('input.txt', expect1=4777409595, expect2=None)
