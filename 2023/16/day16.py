#!/usr/bin/env python3
"AOC 2023: day 16"

from collections import defaultdict

from tools import aoc
from tools import gridutils

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

SPLIT_LR = 4
SPLIT_UP = 5

NEW_DIR = [
{'\\': LEFT,  '/': RIGHT, '|': UP,       '-': SPLIT_LR},
{'\\': DOWN,  '/': UP,    '|': SPLIT_UP, '-': RIGHT},
{'\\': RIGHT, '/': LEFT,  '|': DOWN,     '-': SPLIT_LR},
{'\\': UP,    '/': DOWN,  '|': SPLIT_UP, '-': LEFT},
]

class day16(aoc.aoc):

  def __init__(self):
    super(day16, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid()
    self.n_rows = 0

  def do_line(self, line):
    # called for each line of input
    for x, c in enumerate(line):
      if c != 'x':  # Should be .
        self.grid.set(x, self.n_rows, c)
    self.n_rows += 1

  def part1(self):
    print('===== Start part 1')
    print("max x, y", self.grid.max_x, self.grid.max_y)
    return self.run_from(0, 0, RIGHT)

  def run_from(self, x, y, dir):
    self.energized = defaultdict(set)
    self.beams = [(x, y, dir)]
    while len(self.beams) > 0:
      # print('===== new pass: beams', self.beams)
      beam = self.beams[0]
      self.beams = self.beams[1:]
      self.beam_to_end(beam[0], beam[1], beam[2])
    return len(self.energized)

  def beam_to_end(self, x, y, dir):
    # 0=up, 1 = right, 2=down, 3=left
    # x,y is cur pos

    while True:
      cell = self.grid.get(x, y)
      if cell != '.':
        # print('NEW_DIR', x, y, dir, cell)
        dir = NEW_DIR[dir][cell]
        if dir == SPLIT_LR:
          dir = LEFT
          self.beams.append((x, y, RIGHT))
        elif dir == SPLIT_UP:
          dir = UP
          self.beams.append((x, y, DOWN))

      ener = self.energized.get((x, y)) or set()
      if dir in ener:
        # print('been at', x, y, dir)
        break
      if x >= 0 and x <= self.grid.max_x and y >= 0 and y <= self.grid.max_y:
        self.energized[(x, y)].add(dir)

      x, y = self.new_pos(x, y, dir)
      if x < 0 or x > self.grid.max_x:
        break
      if y < 0 or y > self.grid.max_y:
        break

  def new_pos(self, x, y, dir):
    if dir == UP:
      return x, y-1
    elif dir == RIGHT:
      return x+1, y
    elif dir == DOWN:
      return x, y+1
    elif dir == LEFT:
      return x-1, y

  def part2(self):
    print('===== Start part 2')

    most_energized = 0
    for y in range(self.grid.max_y):
      n_e = self.run_from(0, y, RIGHT)
      most_energized = max(most_energized, n_e)
      n_e = self.run_from(self.grid.max_x, y, LEFT)
      most_energized = max(most_energized, n_e)

    for x in range(1, self.grid.max_x):
      n_e = self.run_from(x, 0, DOWN)
      most_energized = max(most_energized, n_e)
      n_e = self.run_from(x, self.grid.max_y, UP)
      most_energized = max(most_energized, n_e)

    print("part2", most_energized)
    return most_energized


day16.sample_test(r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""", expect1=46, expect2=51)


if __name__ == '__main__':
  day16.run_and_check('input.txt', expect1=6902, expect2=7697)
