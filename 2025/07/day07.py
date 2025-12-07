#!/usr/bin/env python3
"AOC 2025: day 07"

from collections import defaultdict

from tools import aoc
from tools import gridutils

Pos = gridutils.Pos

class day07(aoc.aoc):

  def __init__(self):
    super(day07, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.mani = gridutils.Grid(ignore='.')
    self.beams = set()
    self.splits = 0
    self.b_splits = {}

  def do_line(self, line):
    # called for each line of input
    self.mani.add_row(line)
    x = line.find('S')
    if x >= 0:
      self.start = Pos(x, self.mani.n_rows-1)
      self.beams.add(self.start)

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      self.mani.print()
      print('beam @', self.beams, self.mani.get_pos(self.start))
    self.b_splits = {self.start: 1}

  def reset(self):
    self.splits = 0
    self.beams = set()
    self.beams.add(self.start)
    self.b_splits = {self.start: 1}

  def turn(self):
    new_beams = set()
    new_splits = defaultdict(int)
    for beam in self.beams:
      splits = self.b_splits[beam]
      below = Pos(beam.x, beam.y+1)
      cell_below = self.mani.get_pos(below)
      if cell_below == ' ':
        new_splits[below] += splits
        new_beams.add(below)
      elif cell_below == '^':
        left = Pos(below.x-1, below.y)
        new_splits[left] += splits
        new_beams.add(left)
        right = Pos(below.x+1, below.y)
        new_splits[right] += splits
        new_beams.add(right)
        self.splits += 1
    if self.doing_sample:
      print('>>>', self.splits, new_beams)
    self.beams = new_beams
    self.b_splits = new_splits

  def part1(self):
    print('===== Start part 1')
    for i in range(self.mani.n_rows+1):
       self.turn()
    if self.doing_sample:
      for beam in self.beams:
        print('beam @', beam)
    return self.splits


  def part2(self):
    print('===== Start part 2')
    self.reset()
    for i in range(self.mani.n_rows):
       self.turn()
    if self.doing_sample:
      print(self.b_splits)
    return sum(self.b_splits.values())


day07.sample_test("""
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""", expect1=21, expect2=40)


if __name__ == '__main__':
  day07.run_and_check('input.txt', expect1=1590, expect2=20571740188555)
