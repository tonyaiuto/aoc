#!/usr/bin/env python3
"""Utilities for AoC puzzules.


"""

import sys


def check(tag, expect, got):
  if expect == got:
    print('PASS:', tag)
    return 0
  print('FAIL:', tag, ': expected', expect, 'got', got)
  return 1


def coords4(r, c, n_rows=0, n_cols=0):
  ret = []
  if r > 0:
    ret.append((r-1,c))
  if n_cols == 0 or c < n_cols - 2:
    ret.append((r,c+1))
  if n_rows == 0 or r < n_rows - 2:
    ret.append((r+1,c))
  if c > 0:
    ret.append((r,c-1))
  return ret

def coords8(r, c, n_rows=0, n_cols=0):
  ret = []
  do_c_plus = n_cols == 0 or c < n_cols - 2
  # go clockwise
  if r > 0:
    ret.append((r-1,c))
    if do_c_plus:
      ret.append((r-1,c+1))
  if do_c_plus:
    ret.append((r,c+1))
  if n_rows == 0 or r < n_rows - 2:
    if do_c_plus:
      ret.append((r+1,c+1))
    ret.append((r+1,c))
    if c > 0:
      ret.append((r+1,c-1))
  if c > 0:
    ret.append((r,c-1))
    if r > 0:
      ret.append((r-1,c-1))
  return ret


def neighbors4(grid, r, c, n_rows=0, n_cols=0):
  return [grid[r][c] for r,c in coords4(r, c, n_rows=n_rows, n_cols=n_cols)]

def neighbors8(grid, r, c, n_rows=0, n_cols=0):
  return [grid[r][c] for r,c in coords8(r, c, n_rows=n_rows, n_cols=n_cols)]

def check_neighbors():
   grid = [[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14]]
   errs = 0
   errs += check('coords4.upper_left',  [(0, 1), (1, 0)], coords4(0, 0))
   errs += check('coords4.upper_right', [(1, 4), (0, 3)], coords4(0, 4, n_cols=5))
   errs += check('coords4.middle',
                 [(0, 1), (1, 2), (2, 1), (1, 0)],
                 coords4(1, 1))
   errs += check('coords8.middle',
                 [(0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)],
                 coords8(1, 1))
   errs += check('coords8.left_edge',
                 [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)],
                 coords8(1, 0))
   errs += check('neighbors4', [1, 7, 11, 5], neighbors4(grid, 1, 1))
   errs += check('neighbors4', [1, 7, 11, 5], neighbors4(grid, 1, 1))
   errs += check('neighbors4', [1, 7, 11, 5], neighbors4(grid, 1, 1))
   errs += check('neighbors8', [1, 2, 7, 12, 11, 10, 5, 0], neighbors8(grid, 1, 1))
   return errs

""""

TODO

    sizes = []
    for r, c in self.minima:
      basin = set()
      self.expand_basin(basin, r, c)
      if self.trace_sample:
        print(basin) 
        print('basin size', len(basin))
      sizes.append(len(basin))
 
    b = sorted(sizes)[-3:]
    print(b)
    return b[0] * b[1] * b[2]

  def expand_basin(self, basin, r, c):
    basin.add(r*1000+c)
    to_visit = [(r+1,c), (r-1, c), (r, c+1), (r,c-1)]
    for r,c in to_visit:
      if r*1000+c in basin:
        continue
      if self.grid[r][c] >= 9:
        continue
      self.expand_basin(basin, r, c)
"""


def self_check():
  n_errs = 0
  n_errs += check_neighbors()
  return n_errs


if __name__ == '__main__':
  n_errs = self_check()
  if n_errs > 0:
    print('FAIL:', __file__)
    sys.exit(0)
  print('PASS:', __file__)
