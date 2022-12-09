#!/usr/bin/env python3
"AOC 2021: day 08"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



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
    self.rows = []
    self.counted = set()

  def reset(self):
    # for future use
    self.counted = set()

  def do_line(self, line):
    # called for each line of input
    self.rows.append([int(c) for c in line])

  def post_load(self):
    # called after all input is read
    # print(self.rows[0:4])
    self.nrows = len(self.rows)
    self.ncols = len(self.rows[0])
    print('nr/nc', self.nrows, self.ncols)


  def part1(self):
    print('===== Start part 1')
    self.reset()

    ret = 0
    for ri in range(self.nrows):
      row = self.rows[ri]
      ret += self.n_row_vis(row, ri)
      # print('got', ret, 'row', row)

    for ci in range(self.ncols):
      ret += self.n_col_vis(ci)

    return ret

  def n_col_vis(self, ci):
    ret = 0
    at = -1
    for ri in range(self.nrows):
      height = self.rows[ri][ci]
      if at < height:
        if not (ri, ci) in self.counted:
          self.counted.add((ri, ci))
          ret += 1
          # print('add', ri, ci)
        #else:
        #  print('skip', ri, ci)
        at = height

    at = -1
    for ri in range(self.nrows-1, -1, -1):
      height = self.rows[ri][ci]
      if at < height:
        if not (ri, ci) in self.counted:
          self.counted.add((ri, ci))
          ret += 1
        at = height
    return ret

  def n_row_vis(self, row, ri):
    ret = 0
    at = -1
    lr = len(row)
    for ci in range(lr):
      height = row[ci]
      if at < height:
        if not (ri, ci) in self.counted:
          self.counted.add((ri, ci))
          ret += 1
        at = height
      #else:
      #  break
  
    at = -1
    for ci in range(lr-1, -1, -1):
      height = row[ci]
      if at < height:
        if not (ri, ci) in self.counted:
          self.counted.add((ri, ci))
          ret += 1
        at = height
      #else:
      #  break
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for ri in range(self.nrows):
      for ci in range(self.ncols):
        ret = max(ret, self.comp_vd(ri, ci))

    #for ci in range(self.ncols):
    #  ret += self.n_col_vis(ci)

    return ret

  def comp_vd(self, ri, ci):
    my_height = self.rows[ri][ci]
    vu = ri
    for n in range(ri-1, -1, -1):
      if self.rows[n][ci] >= my_height:
        vu = abs(n - ri)
        break
    vd = self.nrows - ri - 1
    for n in range(ri+1, self.nrows):
      if self.rows[n][ci] >= my_height:
        vd = abs(n - ri)
        break
    vl = ci
    for n in range(ci-1, -1, -1):
      if self.rows[ri][n] >= my_height:
        vl = abs(n - ci)
        break
    vr = self.ncols - ci - 1
    for n in range(ci+1, self.ncols):
      if self.rows[ri][n] >= my_height:
        vr = abs(n - ci)
        break
    ret = vl * vr * vu * vd
    # print(ri, ci, 'h=', my_height, '->', ret, ',', vl, vr, vu, vd)
    return ret
 
    


day08.sample_test("""
30373
25512
65332
33549
35390
""", expect1=21, expect2=8)


if __name__ == '__main__':
  day08.run_and_check('input.txt', expect1=1814, expect2=330786)
