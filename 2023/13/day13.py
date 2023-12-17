#!/usr/bin/env python3
"AOC 2023: day 13"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

def find_reflection(values):
  l = len(values)
  best_match = -1
  best_center = -1
  centers = []
  i = 0
  while i < l-1:
    if values[i] == values[i+1]:
      # possible center line
      # print("Maybe center at", i, values[i])
      centers.append(i+1)
      lmatch = 1
      for j in range(1, l - i - 1):
        if i - j < 0:
          break
        if values[i-j] == values[i+1+j]:
          lmatch += 1
        else:
          break
      #   012345
      # x abbad
      # y abccb
      # z abcdd
      # print('  m', i, lmatch, i + 1 - lmatch, i + 1 + lmatch, l)
      if (0 == i + 1 - lmatch) or (i + 1 + lmatch) >= l:
        best_match = lmatch
        best_center = i + 1
        # print('update center', best_center)
      i += lmatch + 1
    else:
      i += 1
  # print(best_center, centers)
  # return sum(centers)
  return best_center


def best_variation(vals, skip):
  # [109, 12, 30, 30, 76, 97, 30, 30, 115]
  l = len(vals)
  bit = 1
  v2 = list(vals)
  most = max(vals) * 2
  reflect = -1
  n_reflect = 0
  print(vals, 'start best variation')
  while bit < most:
    for vi, v in enumerate(vals):
      if vals[vi] & bit:
        v2[vi] = v & ~bit
      else:
        v2[vi] = v | bit
      # print(v2, 'bit', bit)
      r = find_reflection(v2)
      v2[vi] = v
      if r >= 0 and r != skip:
        # print('got new reflect at', r)
        if reflect != r:
          reflect = r
          n_reflect += 1
          assert n_reflect < 2
    bit <<= 1
  return reflect


class day13(aoc.aoc):

  def __init__(self):
    super(day13, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.sum_vr = 0
    self.sum_hr = 0
    self.sum_vr2 = 0
    self.sum_hr2 = 0

  def do_line(self, map):
    # called for each line of input
    print("===============")
    nc = len(map[0])
    cols = [0] * nc
    rows = []
    for row in map:
      rv = 0
      for col, c in enumerate(row):
        cols[col] *= 2
        rv *= 2
        if c == '#':
           cols[col] += 1
           rv += 1
      rows.append(rv)
      print('%5d' % rv, row)
    print(cols) 
    vr = find_reflection(cols)
    if vr > 0:
      self.sum_vr += vr
    hr = find_reflection(rows)
    # assert vr >= 0 or hr >= 0
    if hr > 0:
      self.sum_hr += hr
    print(vr, hr)

    vr = best_variation(cols, skip=vr)
    if vr > 0:
      self.sum_vr2 += vr
    hr = best_variation(rows, skip=hr)
    if hr > 0:
      self.sum_hr2 += hr
    print(vr, hr)

  def part1(self):
    print('===== Start part 1')
    ret = self.sum_vr + 100 * self.sum_hr
    print('part1', ret)
    return ret

  def part2(self):
    print('===== Start part 2')
    ret = self.sum_vr2 + 100 * self.sum_hr2
    if ret <= 33703:
      print("TOO LOW")
    print('part2', ret)
    return ret


day13.sample_test("""
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""", expect1=405, expect2=400)


if __name__ == '__main__':
  day13.run_and_check('input.txt', expect1=34821, expect2=None)
