#!/usr/bin/env python3
"AOC 2021: day 20"

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



class day20(aoc.aoc):

  def __init__(self):
    super(day20, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.initial = []
    self.at = {}
    self.values = set()

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    v = int(line)
    self.initial.append(v)
    self.at[v] = len(self.initial) - 1
    assert v not in self.values
    self.values.add(v)

  def post_load(self):
    # called after all input is read
    print(self.initial)
    print(self.at)
    self.size = len(self.initial)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    b = list(self.initial)
    self.mix(b)
    return 42

  def mix(self, b):
    order = self.at

    print('order', order)
    for v in self.initial:
      if v == 0:
        continue

      print('order', order)
      pos = order[v]

      if pos + v == 0:
        n_pos = self.size - 1
      else:
        n_pos = (pos + self.size + v) % self.size
      print('move', v, 'from', pos, 'to', n_pos)

      # compute range to decrement or increment
      if pos < n_pos:
        disp = -1
        r_low = pos + 1
        r_high = n_pos - 1
      else:
        disp = 1
        r_low = n_pos
        r_high = pos
 
      res = {v: n_pos}
      for ov, opos in order.items():
        if ov == v:
          continue
        if opos >= r_low and opos <= r_high:
          order[ov] = opos + disp

      order = res

        """
        #  a x b  => x a b
        npos = opos
        if opos > pos:  # b
          npos -= 1
        if opos > n_pos:
          npos += 1
        print('   ', ov, 'from', opos, 'to', npos)
        res[ov] = npos
        """

      plist = sorted([(pos, v) for v, pos in res.items()])
      print([v[1] for v in plist])

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day20.sample_test("""
1
2
-3
3
-2
0
4
""", expect1=3, expect2=None)


if __name__ == '__main__':
  day20.run_and_check('input.txt', expect1=None, expect2=None)
