"""aoc 2018 day 16"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import re
import sys

_VERBOSE = 0

_PART2 = False

class Ground(object):

  def __init__(this):
    this.x_min = 500
    this.x_max = 500
    this.y_max = 0
    this.columns = {}
    this.Set(500, 0, '+')

  def Get(this, x, y):
    col = this.columns.get(x)
    if not col:
       col = ['.'] * 1900
       this.columns[x] = col
    return col[y]

  def Set(this, x, y, v):
    col = this.columns.get(x)
    if not col:
       col = ['.'] * 1900
       this.columns[x] = col
    col[y] = v

  def Add(this, scan):
    if scan.x_min == scan.x_max:
      for y in range(scan.y_min, scan.y_max+1):
        this.Set(scan.x_min, y, '#') 
    else:
      for x in range(scan.x_min, scan.x_max+1):
        this.Set(x, scan.y_min, '#') 
    if scan.y_max > this.y_max:
      this.y_max = scan.y_max
    if this.x_min > scan.x_min:
      this.x_min = scan.x_min
    if this.x_max < scan.x_max:
      this.x_max = scan.x_max

  def Print(this):
    print('%d' % (this.x_min-1))
    for y in range(0, this.y_max+1):
      l = '%4d ' % y
      for x in range(this.x_min-1, this.x_max+2):
        l += this.Get(x, y)
      print(l)


class Scan(object):

  X_RANGE_REGEXP = re.compile(r'y=([0-9]+), x=([0-9]+)\.\.([0-9]+)')
  Y_RANGE_REGEXP = re.compile(r'x=([0-9]+), y=([0-9]+)\.\.([0-9]+)')

  def __init__(this, x_min, x_max, y_min, y_max):
    this.x_min = x_min
    this.x_max = x_max
    this.y_min = y_min
    this.y_max = y_max

  def __str__(this):
    if this.x_min == this.x_max:
      return 'x=%d, y=%d..%d' % (this.x_min, this.y_min, this.y_max)
    return 'x=%d..%d, y=%d' % (this.x_min, this.x_max, this.y_min)


class Scan(object):

  X_RANGE_REGEXP = re.compile(r'y=([0-9]+), x=([0-9]+)\.\.([0-9]+)')
  Y_RANGE_REGEXP = re.compile(r'x=([0-9]+), y=([0-9]+)\.\.([0-9]+)')

  def __init__(this, x_min, x_max, y_min, y_max):
    this.x_min = x_min
    this.x_max = x_max
    this.y_min = y_min
    this.y_max = y_max

  def __str__(this):
    if this.x_min == this.x_max:
      return 'x=%d, y=%d..%d' % (this.x_min, this.y_min, this.y_max)
    return 'x=%d..%d, y=%d' % (this.x_min, this.x_max, this.y_min)

  @staticmethod
  def FromString(s):
    m = Scan.X_RANGE_REGEXP.match(s)
    if m:
      return Scan(int(m.group(2)), int(m.group(3)), int(m.group(1)), int(m.group(1)))
    m = Scan.Y_RANGE_REGEXP.match(s)
    if m:
      return Scan(int(m.group(1)), int(m.group(1)), int(m.group(2)), int(m.group(3)))
    raise ValueError('Unparseable line: %s' % s)


if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while len(sys.argv) > 1 and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      iarg += 1

  ground = Ground()
  with open(sys.argv[iarg]) as inp:
    for line in inp:
      ground.Add(Scan.FromString(line.strip()))

  ground.Print()

"""
You scan a two-dimensional vertical slice of the ground nearby and
discover that it is mostly sand with veins of clay. The scan only
provides data with a granularity of square meters, but it should
be good enough to determine how much water is trapped there. In the
scan, x represents the distance to the right, and y represents the
distance down. There is also a spring of water near the surface at
x=500, y=0. The scan identifies which square meters are clay (your
puzzle input).

For example, suppose your scan shows the following veins of clay:

x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
Rendering clay as #, sand as ., and the water spring as +, and with
x increasing to the right and y increasing downward, this becomes:

   44444455555555
   99999900000000
   45678901234567
 0 ......+.......
 1 ............#.
 2 .#..#.......#.
 3 .#..#..#......
 4 .#..#..#......
 5 .#.....#......
 6 .#.....#......
 7 .#######......
 8 ..............
 9 ..............
10 ....#.....#...
11 ....#.....#...
12 ....#.....#...
13 ....#######...
The spring of water will produce water forever. Water can move
through sand, but is blocked by clay. Water always moves down when
possible, and spreads to the left and right otherwise, filling space
that has clay on both sides and falling out otherwise.

For example, if five squares of water are created, they will flow
downward until they reach the clay and settle there. Water that has
come to rest is shown here as ~, while sand through which water has
passed (but which is now dry again) is shown as |:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
Two squares of water can't occupy the same location. If another
five squares of water are created, they will settle on the first
five, filling the clay reservoir a little more:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
Water pressure does not apply in this scenario. If another four
squares of water are created, they will stay on the right side of
the barrier, and no water will reach the left side:

......+.......
......|.....#.
.#..#.|.....#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
At this point, the top reservoir overflows. While water can reach
the tiles above the surface of the water, it cannot settle there,
and so the next five squares of water settle like this:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#...|.#...
....#...|.#...
....#~~~~~#...
....#######...
Note especially the leftmost |: the new squares of water can reach
this tile, but cannot stop there. Instead, eventually, they all
fall to the right and settle in the reservoir below.

After 10 more squares of water, the bottom reservoir is also full:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#~~~~~#...
....#~~~~~#...
....#~~~~~#...
....#######...
Finally, while there is nowhere left for the water to settle, it
can reach a few more tiles before overflowing beyond the bottom of
the scanned data:

......+.......    (line not counted: above minimum y value)
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
How many tiles can be reached by the water? To prevent counting
forever, ignore tiles with a y coordinate smaller than the smallest
y coordinate in your scan data or larger than the largest one. Any
x coordinate is valid. In this example, the lowest y coordinate
given is 1, and the highest is 13, causing the water spring (in row
0) and the water falling off the bottom of the render (in rows 14
through infinity) to be ignored.

So, in the example above, counting both water at rest (~) and other
sand tiles the water can hypothetically reach (|), the total number
of tiles the water can reach is 57.

How many tiles can the water reach within the range of y values in your scan?
"""
