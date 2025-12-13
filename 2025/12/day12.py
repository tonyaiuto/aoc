#!/usr/bin/env python3
"AOC 2025: day 12"

from collections import defaultdict
from collections import namedtuple

from tools import aoc
from tools import gridutils

Region = namedtuple("Region", "width,  length, ngifts")

class Present(object):

  def __init__(self, spec):
    self.number = int(spec[0].rstrip(':'))
    self.shape = spec[1:]

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(f"{self.number}: {self.shape}")



class day12(aoc.aoc):

  def __init__(self):
    super(day12, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.presents = []
    self.regions = []

  def reset(self):
    # for future use
    pass

  def do_line(self, group):
    if group[0].endswith(':'):
      p = Present(group)
      assert p.number == len(self.presents)
      self.presents.append(p)
      return
    for line in group:
      parts = line.split(':')
      width, length = parts[0].split('x')
      r = Region(int(width), int(length), [int(n) for n in parts[1].strip().split(' ')])
      self.regions.append(r)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.doing_sample:
      print(self.presents)
      print(self.regions)

    return 42


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day12.sample_test("""
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""", expect1=2, expect2=None)


if __name__ == '__main__':
  day12.run_and_check('input.txt', expect1=None, expect2=None)
