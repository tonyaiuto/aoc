#!/usr/bin/env python3
"AOC 2023: day 25"

from collections import defaultdict

from tools import aoc
from tools import gridutils


def calc_sig(grid):
  sig = [-1] * 5
  for x in range(5):
    for y in range(7):
      c = grid.get(x, y)
      if c == '#':
        sig[x] += 1
  return tuple(sig)


class day25(aoc.aoc):

  def __init__(self):
    super(day25, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.keys = []
    self.key_sigs = []
    self.locks = []
    self.lock_sigs = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    grid = gridutils.Grid(ignore='.')
    for row in line:
      grid.add_row(row)
    sig = calc_sig(grid)
    if line[0][0] == '#':
      self.locks.append(grid)
      self.lock_sigs.append(sig)
    else:
      self.keys.append(grid)
      self.key_sigs.append(sig)

  def post_load(self):
    if self.doing_sample:
      print("keys")
      for key in self.keys:
        key.print()
      print(self.key_sigs)
      print("locks")
      for lock in self.locks:
        lock.print()
      print(self.lock_sigs)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    would_fit_keys = []
    for col in range(5):
      would_fit_keys.append(defaultdict(set))
    for i, ks in enumerate(self.key_sigs):
      for col in range(5):
        room_in_col = 5 - ks[col]
        for r in range(0, room_in_col+1):
          would_fit_keys[col][r].add(i)
          # print(ks, 'col', col, 'fits', r)

    ret = 0
    for ls in self.lock_sigs:
      for col in range(5):
        l_height = ls[col] 
        to_check = would_fit_keys[col][l_height]
        if col == 0:
          good = set(to_check)
        else: 
          good = good.intersection(to_check)
        print('lock', ls, 'col', col, 'checking', to_check)
      ret += len(good)
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day25.sample_test("""
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""", expect1=3, expect2=None)


if __name__ == '__main__':
  day25.run_and_check('input.txt', expect1=3201, expect2=None)
