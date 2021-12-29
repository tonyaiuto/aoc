#!/usr/bin/env python3
"AOC 2021: day 19"

from collections import defaultdict
import math

from tools import aoc
from tools import memoized

X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2

class Scanner(object):

  def __init__(self, inp):
    assert inp[0].startswith('--- scanner ')
    t = inp[0][12:].split(' ')
    self.n = int(t[0])
    self.b = []
    for line in inp[1:]:
      if not line: 
        continue
      x = [int(n) for n in line.split(',')]
      x.append(int(math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2])))
      self.b.append(x)

    # print(self)
    self.x_deltas = [i for i in self.deltas(X_AXIS)]
    self.y_deltas = [i for i in self.deltas(Y_AXIS)]
    self.z_deltas = [i for i in self.deltas(Z_AXIS)]

  def __str__(self):
    return 'scr:%d, %s' % (self.n, self.b)

  def deltas(self, axis):
    positions = sorted([pos[axis] for pos in self.b])
    last = positions[0]
    for pos in positions:
      yield pos - last
      last = pos

  def pdeltas(self):
    print('%2d' % self.n, ','.join(['%3d' % i for i in self.x_deltas]))
    # print('  ', ','.join(['%3d' % i for i in self.y_deltas]))
    # print('  ', ','.join(['%3d' % i for i in self.z_deltas]))


class day19(aoc.aoc):

  def __init__(self):
    super(day19, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.scanners = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.scanners.append(Scanner(line))

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    for s in self.scanners:
      s.pdeltas()
    return 42

   


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


"""
--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8
"""

# day19.sample_test('sample.txt', is_file=True, expect1=42, expect2=None)
day19.sample_test('input.txt', is_file=True, expect1=22, expect2=None)


if __name__ == '__main__':
  day19.run_and_check('input.txt', expect1=None, expect2=None)
