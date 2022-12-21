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
    if v in self.values:
      print("Duplicate", v)
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
    order = self.mix(b)
    plist = sorted([(pos, v) for v, pos in order.items()])
    res = [v[1] for v in plist]
    print('final', res)

    zero_pos = order[0]
    a = res[(zero_pos + 1000) % self.size]
    b = res[(zero_pos + 2000) % self.size]
    c = res[(zero_pos + 3000) % self.size]
    print('a b c', a, b, c)
    return a + b + c

    """
Then, the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th is 2; adding these together produces 3.
"""

  def mix(self, b):
    order = self.at

    print('order', order)
    for v in self.initial:
      if v == 0:
        continue

      # print('order', order)
      # print('')
      pos = order[v]
      if v > 0:
        np = pos + v
        if np >= self.size:
          np += 1
        n_pos = np % self.size
      else:
        #if pos + v == 0:
        # we should be at the end
        n_pos = (pos + v - 1) % self.size
      # print('  move %3d' % v, 'from', pos, 'to', n_pos)

      # compute range to decrement or increment
      if pos < n_pos:
        disp = -1
        r_low = pos + 1
        r_high = n_pos
      else:
        disp = 1
        r_low = n_pos
        r_high = pos
      # print("  adjust range:", r_low, r_high, disp)
 
      # res = {v: n_pos}
      order[v] = n_pos
      for ov, opos in order.items():
        if ov == v:
          continue
        if opos >= r_low and opos <= r_high:
          order[ov] = opos + disp
        #print('    ', '%3d' % ov, 'from', opos, 'to', order[ov])

      # plist = sorted([(pos, v) for v, pos in order.items()])
      # print([v[1] for v in plist])
    return order

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
