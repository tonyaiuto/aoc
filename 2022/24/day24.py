#!/usr/bin/env python3
"AOC 2021: day 24"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Blizzard(object):

  def __init__(self, x, y, dir):
    self.x = x
    self.y = y
    self.dir = dir

  def __str__(self):
    return "(%d, %d, %c)" % (self.x, self.y, self.dir)

  def pos(self):
    return (self.x, self.y)

  def bounce(self):
    if self.dir == '<':
      self.dir = '>'
    elif self.dir == '>':
      self.dir = '<'
    elif self.dir == '^':
      self.dir = 'v'
    elif self.dir == 'v':
      self.dir = '^'
    else:
      assert self.dir == 42


class day24(aoc.aoc):

  def __init__(self):
    super(day24, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid()
    self.bliz = []
    self.n_rows = 0
    self.x = 1
    self.y = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)
    for i,c in enumerate(line):
      if c in ('<', '>', 'v', '^'):
        b = Blizzard(i, self.n_rows, c)
        self.bliz.append(b)
    self.n_rows += 1

  def post_load(self):
    # called after all input is read
    if self.trace_sample:
      self.grid.print()
    self.right = len(self.all_input[0]) - 1
    self.bottom = len(self.all_input) - 1
    print('loaded', len(self.bliz), 'blizzards')

  def show(self):
    g = gridutils.Grid()
    for b in self.bliz:
      c = g.get(b.x, b.y)
      v = b.dir
      if c != ' ':
        if c.isdigit():
          v = chr(ord(c) + 1)
        else:
          v = '2'
      g.set(b.x, b.y, v)
    g.print()

  def move_all(self):
    for b in self.bliz:
      if b.dir == '<':
        b.x -= 1
        if b.x == 0:
          b.x = self.right - 1
      elif b.dir == '>':
        b.x += 1
        if b.x == self.right:
          b.x = 1
      elif b.dir == '^':
        b.y -= 1
        if b.y == 0:
          b.y = self.bottom - 1
      elif b.dir == 'v':
        b.y += 1
        if b.y == self.bottom:
          b.y = 1

  def part1(self):
    print('===== Start part 1')
    self.reset()

    for i in range(5):
      self.move_all()
      self.show()

    return 42


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day24.sample_test("""
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""", expect1=18, expect2=None)


if __name__ == '__main__':
  day24.run_and_check('input.txt', expect1=None, expect2=None)
