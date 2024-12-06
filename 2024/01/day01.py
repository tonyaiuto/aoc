#!/usr/bin/env python3
"AOC 2023: day 01"

from collections import defaultdict
import itertools
import math

from tools import aoc

class day01(aoc.aoc):

  def __init__(self):
    super(day01, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.left = []
    self.right = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    line = line.strip()
    if not line:
      return
    numbers = line.split(' ')
    self.left.append(int(numbers[0]))
    self.right.append(int(numbers[-1]))

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.left = sorted(self.left)
    self.right = sorted(self.right)
    ret = 0
    for i in range(len(self.left)):
      ret += abs(self.left[i] - self.right[i])
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    l_count = countem(self.left)
    r_count = countem(self.right)

    ret = 0
    for v in self.left:
      ret += v * r_count[v]
    return ret


def countem(values):
  ret = defaultdict(int)
  for v in values:
    ret[v] += 1
  return ret


day01.sample_test("""
3   4
4   3
2   5
1   3
3   9
3   3
""", expect1=11, expect2=31)


if __name__ == '__main__':
  day01.run_and_check('input.txt', expect1=1530215, expect2=26800609)
