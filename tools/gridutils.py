#!/usr/bin/env python3
"""Utilities for working with grids in AoC puzzules.

"""

import sys

verbose = False

def check(tag, expect, got):
  if expect == got:
    if verbose:
      print('PASS:', tag)
    return 0
  print('FAIL:', tag, ': expected', expect, 'got', got)
  return 1

def deltas4(r, c, span=1, n_rows=-1, n_cols=-1):
  ret = []
  do_right = n_cols <= 0 or (c + span) < n_cols
  do_down = n_rows <= 0 or (r + span) < n_rows
  if r >= span:
    ret.append((-span, 0))
  if do_right:
    ret.append((0, span))
  if do_down:
    ret.append((span, 0))
  if c >= span:
    ret.append((0, -span))
  return ret

def deltas8(r, c, span=1, n_rows=-1, n_cols=-1):
  ret = []
  do_right = n_cols <= 0 or (c + span) < n_cols
  do_down = n_rows <= 0 or (r + span) < n_rows
  # go clockwise
  if r >= span:
    ret.append((-span, 0))
    if do_right:
      ret.append((-span, span))
  if do_right:
    ret.append((0, span))
  if do_down:
    if do_right:
      ret.append((span, span))
    ret.append((span, 0))
    if c >= span:
      ret.append((span, -span))
  if c >= span:
    ret.append((0, -span))
    if r >= span:
      ret.append((-span, -span))
  return ret

def coords4(r, c, span=1, n_rows=0, n_cols=0):
  return [(r+d_r, c+d_c)
          for d_r, d_c in deltas4(r, c, span=span, n_rows=n_rows, n_cols=n_cols)]

def coords8(r, c, span=1, n_rows=0, n_cols=0):
  return [(r+d_r, c+d_c)
          for d_r, d_c in deltas8(r, c, span=span, n_rows=n_rows, n_cols=n_cols)]

def neighbors4(agrid, r, c, span=1, n_rows=0, n_cols=0):
  return [agrid[r][c] for r,c in coords4(r, c, span=span, n_rows=n_rows, n_cols=n_cols)]

def neighbors8(agrid, r, c, span=1, n_rows=0, n_cols=0):
  return [agrid[r][c] for r,c in coords8(r, c, span=span, n_rows=n_rows, n_cols=n_cols)]


def check_neighbors():
   grid = [[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14]]
   errs = 0
   errs += check('deltas4.upper_left', [(0, 1), (1, 0)], deltas4(0, 0))
   errs += check('deltas4.upper_right', [(1, 0), (0, -1)], deltas4(0, 4, n_cols=5))
   errs += check('deltas4.middle',
                 [(-1, 0), (0, 1), (1, 0), (0, -1)],
                 deltas4(2, 2))
   errs += check('deltas4.middle_span',
                 [(-2, 0), (0, 2), (2, 0), (0, -2)],
                 deltas4(7, 8, span=2))
   errs += check('deltas4.span_clip_up',
                 [(0, 5), (5, 0)],
                 deltas4(3, 3, span=5))
   errs += check('deltas4.span_col_boundary',
                 [(-2, 0), (2, 0), (0, -2)],
                 deltas4(3, 3, span=2, n_cols=5))
   errs += check('deltas8.clip_up',
                 [(0, 5), (5, 5), (5, 0), (5, -5), (0, -5)],
                 deltas8(3, 7, span=5))
   errs += check('deltas8.middle',
                 [(-3, 0), (-3, 3), (0, 3), (3, 3), (3, 0), (3, -3), (0, -3), (-3, -3)],
                 deltas8(42, 37, span=3))
   errs += check('deltas8.lower_right_ok',
                 [(-3, 0), (-3, 3), (0, 3), (3, 3), (3, 0), (3, -3), (0, -3), (-3, -3)],
                 deltas8(42, 37, span=3, n_rows=46, n_cols=41))
   errs += check('deltas8.lower_right_clip_right',
                 [(-3, 0), (3, 0), (3, -3), (0, -3), (-3, -3)],
                 deltas8(42, 37, span=3, n_rows=46, n_cols=40))
   errs += check('deltas8.lower_right_clip_down',
                 [(-3, 0), (-3, 3), (0, 3), (0, -3), (-3, -3)],
		 deltas8(42, 37, span=3, n_rows=45, n_cols=41))

   errs += check('coords4.upper_left',  [(0, 1), (1, 0)], coords4(0, 0))
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


def min_max(positions):
  min_a = None
  max_a = None
  min_b = None
  max_b = None
  for a,b in positions:
    min_a = min(min_a or a, a)
    max_a = max(max_a or a, a)
    min_b = min(min_b or b, b)
    max_b = max(max_b or b, b)
  return (min_a, max_a, min_b, max_b)
   


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
  verbose = True
  n_errs = self_check()
  if n_errs > 0:
    print('FAIL:', __file__)
    sys.exit(0)
  print('PASS:', __file__)
