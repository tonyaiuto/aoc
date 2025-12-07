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
    self.b_splits = {self.start: 0}

  def reset(self):
    self.splits = 0
    self.beams = set()
    self.beams.add(self.start)
    self.b_splits = {self.start: 0}

  def turn(self):
    new_beams = set()
    osize = len(self.beams)
    for beam in self.beams:
      splits = self.b_splits[beam]
      below = Pos(beam.x, beam.y+1)
      cell_below = self.mani.get_pos(below)
      if cell_below == ' ':
        new_beams.add(below)
        self.b_splits[below] = splits
      elif cell_below == '^':
        left = Pos(below.x-1, below.y)
        self.b_splits[left] = splits + 1
        if left in new_beams:
          self.b_splits[left] += 1
        else:
          new_beams.add(left)
        right = Pos(below.x+1, below.y)
        self.b_splits[right] = splits + 1
        if right in new_beams:
          self.b_splits[right] += 1
        else:
          new_beams.add(right)
        self.splits += 1
    if self.doing_sample:
      print('>>>', self.splits, new_beams)
    self.beams = new_beams

  def turn2(self):
    new_beams = []
    for beam in self.beams:
      below = Pos(beam.x, beam.y+1)
      cell_below = self.mani.get_pos(below)
      if cell_below == ' ':
        new_beams.append(below)
      elif cell_below == '^':
        left = Pos(below.x-1, below.y)
        new_beams.append(left)
        right = Pos(below.x+1, below.y)
        new_beams.append(right)
        self.splits += 1
    if True or self.doing_sample:
      print('>>>', self.splits, len(new_beams))
    self.beams = new_beams

  def part1(self):
    print('===== Start part 1')
    for i in range(self.mani.n_rows+1):
       self.turn()
    for beam in self.beams:
      print('beam @', beam)
    return self.splits


  def part2(self):
    print('===== Start part 2')
    self.reset()
    for i in range(self.mani.n_rows):
       print("TURN", i)
       self.turn()
    for beam in self.beams:
      print('beam @', beam)
    return len(self.beams)


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
""", expect1=21, expect2=None)


if __name__ == '__main__':
  day07.run_and_check('input.txt', expect1=1590, expect2=40)
