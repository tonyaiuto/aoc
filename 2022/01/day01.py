#!/usr/bin/env python3
"AOC 2021: day 01"

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



class day01(aoc.aoc):

  def __init__(self):
    super(day01, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.elf = 0
    self.max = 0
    self.max_elf = -1
    self.calories = []

  def reset(self):
    # for future use
    self.elf = 0
    self.max = 0
    self.max_elf = -1
    self.calories = []
    pass

  def do_line(self, line):
    # called for each line of input
    self.elf += 1
    c = sum([int(x) for x in line])
    self.calories.append(c)
    if c > self.max:
      self.max = c
      self.max_elf = self.elf
      # print('max elf', self.max_elf, c)
    pass

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    # self.reset()
    print('elf', self.max_elf, 'has', self.max)
    return self.max


  def part2(self):
    print('===== Start part 2')
    # self.reset()

    # print(self.calories)
    ret = sum(sorted(self.calories)[-3:])
    # print(ret)
    return ret


day01.sample_test("""
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
""", expect1=24000, expect2=45000)


if __name__ == '__main__':
  day01.run_and_check('input.txt', expect1=74198, expect2=209914)
