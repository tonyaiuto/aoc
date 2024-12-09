#!/usr/bin/env python3
"AOC 2023: day 04"

from collections import defaultdict

from tools import aoc
from tools import gridutils

XDIRS = [
    (-1,  0),  # UP
    (-1,  1),  # UP RIGHT
    ( 0,  1),  # RIGHT
    ( 1,  1),  # DOWN RIGHT
    ( 1,  0),  # DOWN
    ( 1, -1),  # DOWN LEFT
    ( 0, -1),  # LEFT 
    (-1, -1),  # LEFT UP
]
DIRS=gridutils.DIRS8

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
    self.grid = gridutils.Grid()
    self.rows = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)
    self.rows += 1

  def post_load(self):
    # called after all input is read
    # self.grid.print()
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    found = 0
    for y in range(self.rows+1):
      for x in range(self.grid.width+1):
        if self.grid.get(x, y) == 'X':
          for nx, ny in DIRS:
             if self.dir_find(x, y, nx, ny, ['M', 'A', 'S']):
               found += 1
    return found

  def dir_find(self, x, y, nx, ny, more):
    # Find remaining letters in a given direction
    if not more:
      return 1
    if self.grid.get(x+nx, y+ny) == more[0]:
      return self.dir_find(x+nx, y+ny, nx, ny, more[1:])

  def pattern_find(self, row, col, more):
    if not more:
      return 1
    ret = 0
    for r, c in gridutils.coords8(row, col):
      if self.grid.get(r, c) == more[0]:
        # print("%s found %s at %d,%d" % ("  " * (4 - len(more)), more[0], r, c))
        ret += self.pattern_find(r, c, more[1:])
    return ret

  def part1_any_dir(self):
    print('===== Start part 1 any dir')
    self.reset()
    found = 0
    for row in range(self.rows):
      for col in range(self.grid.width):
        if self.grid.get(row, col) == 'X':
          n = self.pattern_find(row, col, ['M', 'A', 'S'])
          # print("X at %d, %d => %d" % (row, col, n))
          found += n
    return found

  def part2_try1(self):
    print('===== Start part 2')
    self.reset()
    got = defaultdict(int)
    for y in range(self.rows+1):
      for x in range(self.grid.width+1):
        if self.grid.get(x, y) == 'M':
          for dir_i, (inc_x, inc_y) in enumerate(DIRS):
             if self.dir_find(x, y, inc_x, inc_y, ['A', 'S']):
               # assert A at row+inc_r, col+inc_c
               a_x = x + inc_x
               a_y = y + inc_y
               if self.grid.get(a_x, a_y) != 'A':
                 print("FAIL: expect A at %d,%d got %s" % (
                        a_x, a_y, self.grid.get(a_x, a_y)))
                 return -1
               # get alternate corners
               dir_90 = DIRS[(dir_i + 2) % len(DIRS)]
               dir_180 = DIRS[(dir_i + 6) % len(DIRS)]
               c1 = self.grid.get(a_x + dir_90[0], a_y + dir_90[1])
               c2 = self.grid.get(a_x + dir_180[0], a_y + dir_180[1])
               if (c1 == 'M' and c2 == 'S') or (c1 == 'S' and c2 == 'M'):
                 sig = (a_x, a_y, dir_i % 2)
                 got[sig] += 1
                 print("X-MAS at %d, %d, dir %d" % (a_x, a_y, dir_i))

    for sig, count in got.items():
      if count != 2:
        print("what", sig, count)
    # 2039 low for part 2
    # 2067 high for part 2
    # return found // 2
    return len(got)

  def part2(self):
    print('===== Start part 2')
    self.reset()
    got = defaultdict(int)
    found = 0
    for y in range(self.rows+1):
      for x in range(self.grid.width+1):
        if self.grid.get(x, y) == 'A':
          c1 = self.grid.get(x - 1, y - 1)
          c2 = self.grid.get(x + 1, y + 1)
          if (c1 == 'M' and c2 == 'S') or (c1 == 'S' and c2 == 'M'):
            c1 = self.grid.get(x + 1, y - 1)
            c2 = self.grid.get(x - 1, y + 1)
            if (c1 == 'M' and c2 == 'S') or (c1 == 'S' and c2 == 'M'):
              found += 1

          c1 = self.grid.get(x - 1, y)
          c2 = self.grid.get(x + 1, y)
          if (c1 == 'M' and c2 == 'S') or (c1 == 'S' and c2 == 'M'):
            c1 = self.grid.get(x, y - 1)
            c2 = self.grid.get(x, y + 1)
            if (c1 == 'M' and c2 == 'S') or (c1 == 'S' and c2 == 'M'):
              found += 1

    # 2039 low for part 2
    # 2067 high for part 2
    return found



day04.sample_test("""
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""", expect1=18, expect2=9)


if __name__ == '__main__':
  day04.run_and_check('input.txt', expect1=2718, expect2=2000)
