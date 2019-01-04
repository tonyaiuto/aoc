"""aoc 2018 day 22"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import sys

from memoized import memoized

_VERBOSE = 0
_PART2 = False


class Cave(object):

  ROCKY = 0
  WET = 1
  NARROW = 2

  def __init__(this, depth=1, target_x=0, target_y=0):
    this.depth = depth
    this.target_x = target_x
    this.target_y = target_y
    this.mouth = (0,0)

  def __str__(this):
    return 'Cave(depth=%d, target=%d,%d)' % (this.depth, this.target_x,
                                             this.target_y)

  @staticmethod
  def Load(inp):
    ret = Cave()
    for l in inp:
      if l.startswith('depth:'):
        ret.depth = int(l[6:].strip())
      elif l.startswith('target:'):
        xy = [int(v) for v in l[7:].strip().split(',')]
        ret.target_x = xy[0]
        ret.target_y = xy[1]
    return ret

  def Print(this):
    pass

  def geologic_index(this, x, y):
    # The man explains that due to the unusual geology in the area, there
    # is a method to determine any region's type based on its erosion
    # level. The erosion level of a region can be determined from its
    # geologic index. The geologic index can be determined using the first
    # rule that applies from the list below:

    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    # If the region's Y coordinate is 0, the geologic index is its X coordinate
    # times 16807.
    if y == 0:
      return x * 16807
    # If the region's X coordinate is 0, the geologic index is its Y coordinate
    # times 48271.
    if x == 0:
      return y * 48271
    # Otherwise, the region's geologic index is the result of multiplying the
    # erosion levels of the regions at X-1,Y and X,Y-1.
    if x == this.target_x and y == this.target_y:
      return 0
    return this.erosion(x-1, y) * this.erosion(x, y-1)

  @memoized
  def erosion(this, x, y):
    # A region's erosion level is its geologic index plus the cave system's
    # depth, all modulo 20183. Then:
    return (this.geologic_index(x, y) + this.depth) % 20183

  def type(this, x, y):
    # If the erosion level modulo 3 is 0, the region's type is rocky.
    # If the erosion level modulo 3 is 1, the region's type is wet.
    # If the erosion level modulo 3 is 2, the region's type is narrow.
    return this.erosion(x, y) % 3

  def TotalRisk(this):
    ret = 0
    for y in range(this.target_y + 1):
      for x in range(this.target_x + 1):
        ret += this.type(x, y)
    return ret

  @staticmethod
  def TypeName(int):
    return ['ROCKY', 'WET', 'NARROW'][int]

def SelfCheck():
  # For example, suppose the cave system's depth is 510 and the target's
  # coordinates are 10,10. Using % to represent the modulo operator,
  # the cavern would look as follows:
  cave = Cave(depth=510, target_x=10, target_y=10)

  # At 0,0, the geologic index is 0. The erosion level is (0 + 510)
  # % 20183 = 510. The type is 510 % 3 = 0, rocky.
  assert cave.type(0, 0) == Cave.ROCKY

  # At 1,0, because the Y coordinate is 0, the geologic index is 1
  # * 16807 = 16807. The erosion level is (16807 + 510) % 20183 =
  # 17317. The type is 17317 % 3 = 1, wet.
  assert cave.type(1, 0) == Cave.WET

  # At 0,1, because the X coordinate is 0, the geologic index is 1
  # * 48271 = 48271. The erosion level is (48271 + 510) % 20183 =
  # 8415. The type is 8415 % 3 = 0, rocky.
  assert cave.type(0, 1) == Cave.ROCKY

  # At 1,1, neither coordinate is 0 and it is not the coordinate
  # of the target, so the geologic index is the erosion level of 0,1
  # (8415) times the erosion level of 1,0 (17317), 8415 * 17317 =
  # 145722555. The erosion level is (145722555 + 510) % 20183 = 1805.
  # The type is 1805 % 3 = 2, narrow.
  assert cave.type(1, 1) == Cave.NARROW
  assert cave.type(0, 1) == Cave.ROCKY

  # At 10,10, because they are the target's coordinates, the geologic
  # index is 0. The erosion level is (0 + 510) % 20183 = 510. The type
  # is 510 % 3 = 0, rocky.
  assert cave.geologic_index(10, 10) == 0
  assert cave.erosion(10, 10) == 510
  assert cave.type(10, 10) == Cave.ROCKY

  # In the cave system above, because the mouth is at 0,0 and the target
  # is at 10,10, adding up the risk level of all regions with an X
  # coordinate from 0 to 10 and a Y coordinate from 0 to 10, this total
  # is 114.
  assert cave.TotalRisk() == 114

"""
Drawing this same cave system with rocky
as ., wet as =, narrow as |, the mouth as M, the target as T, with
0,0 in the top-left corner, X increasing to the right, and Y
increasing downward, the top-left corner of the map looks like this:

M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||
Before you go in, you should determine the risk level of the area.
For the rectangle that has a top-left corner of region 0,0 and a
bottom-right corner of the region containing the target, add up the
risk level of each individual region: 0 for rocky regions, 1 for
wet regions, and 2 for narrow regions.


What is the total risk level for the smallest rectangle that includes
0,0 and the target's coordinates?
"""


if __name__ == '__main__':
  iarg = 1
  dump = False
  while iarg < len(sys.argv) and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      _VERBOSE += 1
      iarg += 1
    if sys.argv[iarg] == '-d':
      dump = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      iarg += 1

  with open(sys.argv[iarg]) as inp:
    cave = Cave.Load(inp)
  if dump:
    print(cave)
  SelfCheck()

  # part1
  print('risk: %d' % cave.TotalRisk())
  
