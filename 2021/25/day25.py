#!/usr/bin/env python3
"AOC 2021: day 25"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day25(aoc.aoc):

  def __init__(self):
    super(day25, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.east = []
    self.south = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    if not line:
      return
    e = [c == '>' for c in line]
    s = [c == 'v' for c in line]
    assert len(e) == len(s)
    self.east.append(e)
    self.south.append(s)

  def post_load(self):
    # called after all input is read
    self.w = max([len(e) for e in self.east])
    for e in self.east:
      assert self.w == len(e)
    self.h = len(self.east)

  def print(self, n):
    print('\nAfter', n)
    for row, east in enumerate(self.east):
      s = self.south[row]
      o = ''
      for col, e in enumerate(east):
        c = '>' if e else ('v' if s[col] else '.')
        o += c
      print(o)

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.print(0)
    self.step1()
    self.print(1)
    for i in range(2, 5):
      moved = self.step1()
      if not moved:
        return i
      if i < 10:
       self.print(i)
    
    return 42

  def step1(self):
    moved = False
    toset = -1
    for row, east in enumerate(self.east):
      s = self.south[row]
      for col, e in enumerate(east):
        right = (col + 1) % self.w
        # can I move?
        mv = e and not east[right] and not s[right]
        if toset >= 0:
          east[toset] = True
          toset = -1
        if mv:
          east[col] = False
          toset = right
          moved = True
          # print("SHOULD SET", row, right)
      if toset >= 0:
        moved = True
        east[toset] = True

    old_move = []
    for row in range(self.h):
      south = self.south[row]
      down = (row + 1) % self.h
      de = self.east[down]
      ds = self.south[down]
      to_move = [south[col] and not de[col] and not ds[col] for col in range(self.w)]
      if old_move:
        for col, mv in enumerate(old_move):
          if mv:
            moved = True
            self.south[row][col] = True
      for col, mv in enumerate(to_move):
        if mv:
          moved = True
          self.south[row][col] = False
          print('  moving down', row, col)
      old_move = copy.copy(to_move)
    if old_move:
      for col, mv in enumerate(old_move):
        if mv:
          self.south[0][col] = True
    return moved

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day25.sample_test("""
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""", expect1=58, expect2=None)


if __name__ == '__main__':
  day25.run_and_check('input.txt', expect1=None, expect2=None)
