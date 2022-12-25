#!/usr/bin/env python3
"AOC 2021: day 25"

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



class day25(aoc.aoc):

  def __init__(self):
    super(day25, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    return 42


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day25.sample_test("""

""", expect1=None, expect2=None)


if __name__ == '__main__':
  day25.run_and_check('input.txt', expect1=None, expect2=None)
