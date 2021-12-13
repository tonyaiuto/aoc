#!/usr/bin/env python3
"AOC 2021: day 13"

import copy

from tools import aoc


class day13(aoc.aoc):

  def __init__(self):
    super(day13, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.dots = {}
    self.folds = []
    self.max_x = 0
    self.max_y = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    if not line:
      return
    if line.startswith('fold along'):
      dim, where = line[11:].split('=')
      self.folds.append((dim, int(where)))
    elif ',' in line:
      x,y = line.split(',')
      x = int(x)
      y = int(y) 
      self.max_x = max(self.max_x, x)
      self.max_y = max(self.max_y, y)
      self.dots[x, y] = 1
    else:
      raise Exception('bad input: ' + line)

  def post_load(self):
    # called after all input is read
    if self.trace_sample:
      print(self.dots)
      print(self.folds)

    self.grid = []
    for y in range(self.max_y+1):
      self.grid.append([' '] * (self.max_x+1))
    for x, y in self.dots:
      self.grid[y][x] = '#'
    if self.trace_sample:
      self.pgrid()

  def pgrid(self):
    for row in self.grid:
      segs = len(row) // 5
      print('   '.join([''.join(row[5*s:5*(s+1)]) for s in range(segs)]))


  def part1(self):
    print('===== Start part 1')
    self.reset()

    for f in self.folds[0:1]:
      if f[0] == 'x':
        self.foldx(f[1])
      else:
        self.foldy(f[1])

    ret = 0
    for row in self.grid:
      for c in row:
        if c == '#':
          ret += 1
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    print('grid len', len(self.grid))

    for f in self.folds:
      if f[0] == 'x':
        self.foldx(f[1])
      else:
        self.foldy(f[1])
      if self.trace_sample:
        self.pgrid()

    self.pgrid()
    return 0


  def foldx(self, where):
    if self.trace_sample:
      print('fold x at', where, 'max =', self.max_x)
    left = where

    for x in range(len(self.grid)):
      row = self.grid[x]
      # print('row', x, row)
      for i in range(left):
        # print('merge', where + 1 + i, where - 1 - i)
        if row[where+1+i] == '#':
          row[where-1-i] = '#'
      self.grid[x] = row[0:left+1]


  def foldy(self, where):
    if self.trace_sample:
      print('fold y at', where, 'max =', self.max_y, 'len:', len(self.grid))
    left = len(self.grid) // 2
    assert where == left

    for y_off in range(where):
      get_y = where + 1 + y_off
      to_y = where - 1 - y_off
      row = self.grid[get_y]
      fold_to = self.grid[to_y]
      if self.trace_sample:
        print('merge', get_y, to_y)
        print('    ', ''.join(row))
        print('    ', ''.join(fold_to))
      for i,c in enumerate(row):
        if c == '#':
          fold_to[i] = '#'
      self.grid[to_y] = fold_to
      if self.trace_sample:
        print('    ', ''.join(fold_to))

    self.grid = self.grid[0:left]


day13.sample_test("""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""", expect1=17, expect2=0)


if __name__ == '__main__':
  day13.run_and_check('input.txt', expect1=716, expect2=0, recreate=True)
