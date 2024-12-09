#!/usr/bin/env python3
"AOC 2023: day 08"

from collections import defaultdict
import itertools

from tools import aoc
from tools import gridutils

ANT='0'

class Foo(object):

  def __init__(self):
    pass

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.__dict__)


def vector(a, b):
  return ((b[0] - a[0]), (b[1] - a[1]))


def add_vector(a, v):
  return (a[0]+v[0], a[1]+v[1])


def sub_vector(a, v):
  return (a[0]-v[0], a[1]-v[1])



class day08(aoc.aoc):

  def __init__(self):
    super(day08, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid(ignore='.')
    self.a_pos = defaultdict(list)

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    self.grid.add_row(line)
    for x, c in enumerate(line):
      if c != '.':
        self.a_pos[c].append((x, self.grid.max_y))

  def post_load(self):
    # called after all input is read
    # self.grid.print()
    # print(self.a_pos)
    pass

  def in_grid(self, pos):
    return (pos[0] >= 0 and pos[0] <= self.grid.max_x
            and pos[1] >= 0 and pos[1] <= self.grid.max_y)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    node_pos = set()
    for a, where in self.a_pos.items():
      for pair in itertools.combinations(where, 2):
        v = vector(pair[0], pair[1])
        np = sub_vector(pair[0], v)
        if self.in_grid(np):
          node_pos.add(np)
        np = add_vector(pair[1], v)
        if self.in_grid(np):
          node_pos.add(np)

    return len(node_pos)


  def part2(self):
    print('===== Start part 2')
    self.reset()
    node_pos = set()
    for a, where in self.a_pos.items():
      for pair in itertools.combinations(where, 2):
        v = vector(pair[0], pair[1])
        np = pair[0]
        while True:
          node_pos.add(np)
          np = sub_vector(np, v)
          if not self.in_grid(np):
            break
        np = pair[1]
        while True:
          node_pos.add(np)
          np = add_vector(np, v)
          if not self.in_grid(np):
            break
    return len(node_pos)


day08.sample_test("""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""", expect1=14, expect2=34)


if __name__ == '__main__':
  day08.run_and_check('input.txt', expect1=261, expect2=898)
