#!/usr/bin/env python3
"AOC 2021: day 11"

from collections import defaultdict
import math

from tools import aoc
from tools import gridutils


class day11(aoc.aoc):

  def __init__(self):
    super(day11, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = []
    self.nrows = 0
    self.ncols = 10

  def do_line(self, line):
    # called for each line of input
    self.nrows += 1
    row = [int(h) for h in line]
    self.grid.append(row)

  def pgrid(self, step):
    print('after step', step)
    for row in range(10):
      print(' '.join([str(c) for c in self.grid[row]]))
 
  def step(self, inc=1):
    flashed = []
    toflash = []
    nflashed = 0

    # print('======================== step')
    for row in range(self.nrows):
      for col in range(self.ncols):
        # print(self.grid)
        # print(row, col)
        self.grid[row][col] += 1
        if self.grid[row][col] > 9:
          toflash.append((row, col))
          flashed.append((row, col))
  
    while len(toflash) > 0:
      nflash = []
      #if self.trace_sample:
      #  print('to flash', toflash)
      for row, col in toflash:
        to_inc = gridutils.coords8(row, col, n_rows=self.nrows, n_cols=self.ncols)
        #if self.trace_sample and row < 2:
        #  print("Flashed", row, col, 'must inc', to_inc)
        for r, c in to_inc:
          if self.grid[r][c] <= 9:
            self.grid[r][c] += 1
            if self.grid[r][c] > 9:
              nflash.append((r, c))
              flashed.append((r, c))
      toflash = nflash

    for r, c in flashed:
      self.grid[r][c] = 0
    # print(len(flashed), 'flashed this turn\n')
    return len(flashed)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.pgrid(0)

    ret = 0
    for step in range(100):
      flashed = self.step(1)
      ret += flashed
      if (step + 1) % 10 == 0:
        print('after step', step+1, ',', flashed, 'flashed,', ret, 'total')
      # self.pgrid(step+1)
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    ret = 0
    while True:
      ret += 1
      nflashed = self.step()
      # self.pgrid(ret)
      if nflashed == 100:
        # self.pgrid(ret)
        return ret



day11.sample_test("""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""", expect1=1656, expect2=None)


if __name__ == '__main__':
  day11.run_and_check('input.txt', expect1=1661, expect2=334)
  pass
