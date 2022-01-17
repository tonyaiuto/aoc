#!/usr/bin/env python3
"AOC 2021: day 19"

from collections import defaultdict
import math

from tools import aoc
from tools import memoized

import rotate

X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2


def pdiff(a, b):
  return (b[0]-a[0], b[1]-a[1], b[2]-a[2]) 


class Scanner(object):

  def __init__(self, inp):
    assert inp[0].startswith('--- scanner ')
    t = inp[0][12:].split(' ')
    self.n = int(t[0])
    self.b = []
    self.rotation = -1
    for line in inp[1:]:
      if not line: 
        continue
      x = tuple([int(n) for n in line.split(',')])
      if x == (-618, -824, -621):
        print('Got the 618')
      # XXX x.append(int(math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2])))
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


class BeaconList(object):

  def __init__(self, scanner, axis, rotation):
    self.scanner = scanner
    self.axis = axis
    self.rotation = rotation
    rf = rotate.rot_func[rotation]
    rotated = [rf(pos) for pos in scanner.b]
    # first = rotated[0]
    # self.positions = [pdiff(first, pos) for pos in rotated]
    self.positions = rotated
    self.bingod = None

    # compute all the deltas
    lp = len(self.positions)
    deltas = {}
    for fp in range(0, lp):
      fpos = self.positions[fp]
      if fpos == (-618, -824, -621):
        print('Got the 618', fpos)
      for tp in range(fp+1, lp):
        tpos = self.positions[tp]
        delta = pdiff(fpos, tpos)
        if delta == (68, -1246, -43):
          print('============================ BINGO')
        if fpos[0] == -618 and tpos[0] == -537:
          print('============================ BINGO', fpos, tpos, delta)
          self.bingod = delta
        if tpos[0] == -618 and fpos[0] == -537:
          print('============================ RBINGO', fpos, tpos, delta)
          self.bingod = delta
        if delta in deltas:
          print("FUCK, do it the hard way")
          print(deltas)
          sys.exit(1)
        deltas[delta] = (fpos, tpos)
    self.deltas = deltas
    assert len(self.deltas) == lp * (lp - 1) // 2


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
    ns = len(self.scanners)

    #for s in self.scanners:
    #  s.pdeltas()
    
    for s in self.scanners:
       s.beacons = BeaconList(s, X_AXIS, 0)

    for i_s, s in enumerate(self.scanners):
      s_beacons = s.beacons
      deltas = s_beacons.deltas
      deltas = self.scanners[i_s].beacons.deltas
      for i_t in range(i_s+1, ns):
        n_match = 0
        other_beacons = self.scanners[i_t].beacons
        other_deltas = other_beacons.deltas
        for d in other_deltas:
          if d in deltas:
            if d == s_beacons.bingod:
              print('got the bingod')
            if d == other_beacons.bingod:
              print('got the Rbingod')
            f1,f2 = deltas[d]
            t1,t2 = other_deltas[d]
            print('s %2d %2d:' % (i_s, i_t), d, f1, f2, '...', t1, t2)
            n_match += 1

        if n_match >= 11:
          print('You sunk my battleship', i_s, i_t)

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

day19.sample_test('sample.txt', is_file=True, expect1=42, expect2=None)
# day19.sample_test('input.txt', is_file=True, expect1=22, expect2=None)


if __name__ == '__main__':
  # day19.run_and_check('input.txt', expect1=None, expect2=None)
  pass
