#!/usr/bin/env python3
"AOC 2025: day 05"

from bisect import bisect_left
from collections import defaultdict

from tools import aoc


class Foo(object):

  def __init__(self):
    pass

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.__dict__)



class day05(aoc.aoc):

  def __init__(self):
    super(day05, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.fresh = []
    self.available = []
    self.in_ranges = True

  def do_line(self, line):
    if not line:
      self.in_ranges = False
      return
    if self.in_ranges:
       low, high = line.split('-')
       self.fresh.append([int(low), int(high)])
    else:
       self.available.append(int(line))

  def post_load(self):
    # called after all input is read
    self.fresh = sorted(self.fresh)

  def is_fresh(self, ing):
    for f in self.fresh:
      if ing >= f[0]:
        if ing <= f[1]:
          return True
    return False

  def part1(self):
    print('===== Start part 1')
    ret = 0
    for i in self.available:
      if self.is_fresh(i):
        ret += 1
    return ret

  def part2(self):
    print('===== Start part 2')
    ret = 0
    # merge the spans.
    out = []
    cur = self.fresh[0]
    for nxt in self.fresh[1:]:
       low = cur[0]
       high = cur[1]
       assert nxt[0] >= low
       if nxt[0] > high + 1:
         out.append(cur)
         ret += high - low + 1
         print(cur, nxt, '=>', ret)
         cur = nxt
         continue
       assert low <= nxt[0]
       assert nxt[0] <= high + 1
       if nxt[1] > high:
         cur[1] = nxt[1]

    ret += cur[1] - cur[0] + 1
    return ret


day05.sample_test("""
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""", expect1=3, expect2=14)


if __name__ == '__main__':
  day05.run_and_check('input.txt', expect1=513, expect2=339668510830757)
