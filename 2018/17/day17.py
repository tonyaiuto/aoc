"""aoc 2018 day 17"""

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
    this.gen = 0
    this.x_min = 500
    this.x_max = 500
    this.y_max = 0
    this.columns = {}

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

  def nWet(this):
    ret = 0
    for x, col in this.columns.iteritems():
      for cell in col:
        if cell == '~' or cell == '|':
          ret += 1
    return ret - 1

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
    print('gen:%d, x:%d' % (this.gen, this.x_min-1))
    n_wet = 0
    for y in range(0, this.y_max+1):
      l = '%4d ' % y
      for x in range(this.x_min-1, this.x_max+2):
        if y == 0 and x == 500:
          l += '+'
        else:
          v = this.Get(x, y)
          l += v
          if v == '~' or v == '|':
            n_wet += 1
      print(l)
    print('%d tiles are wet' % n_wet)

  def Fall(this, x, y):
    # Returns the line you are on when blocked or -1 if off edge
    for y in range(y, this.y_max+1):
      v = this.Get(x, y)
      if v == '.' or v == '|':
        if v == '.':
          this.Set(x, y, '|')
      else:
        return y-1
    return -1

  def CanFall(this, x, y):
    v = this.Get(x, y+1)
    return (v == '.' or v == '|')

  def HasWall(this, x_range, y):
    for x in x_range:
      if this.CanFall(x, y):
        return False
      tile = this.Get(x, y)
      if tile == '#':
        return True
    return False

  def InWell(this, from_x, y):
    if not this.HasWall(range(from_x, this.x_min-1, -1), y):
      return False
    return this.HasWall(range(from_x, this.x_max+1), y)


  def FloodRange(this, x_range, y, in_well):
    if _VERBOSE > 1:
      print('Flood %s for y:%d x:%s' % (
         'in well' if in_well else 'plain', y, x_range[0:10]))
    # Move in range.
    # fill with ~ and return position when done
    # else return -1 if blocked
    last_x = -1
    # last_x = x_range[0]
    # tile = this.Get(last_x, y)

    for x in x_range:
      tile = this.Get(x, y)
      # Hit a hard edge
      if tile == '#' or tile == '~':
        if last_x > 0:
          if _VERBOSE > 0 and in_well:
            print('= set %d,%d = %c' % (last_x, y, '~' if in_well else '|'))
          this.Set(last_x, y, '~' if in_well else '|')
          return in_well
        return False
      if this.CanFall(x, y):
        return this.Drop(x, y)
      if tile == '.':
        this.Set(x, y, '|')
        last_x = x
      if tile == '|':
        last_x = x
    return False

  def Drop(this, from_x, from_y):
    y = this.Fall(from_x, from_y)
    if y < 0:
      return False
    in_well = this.InWell(from_x, y)
    if this.FloodRange(range(from_x-1, this.x_min-1, -1), y, in_well):
      return True
    if this.FloodRange(range(from_x, this.x_max+1), y, in_well):
      return True
    # return this.FloodRange(range(from_x, from_x+1), y, in_well)
    return False

  def NewDrop(this):
    global _VERBOSE
    this.gen += 1
    #if this.gen > 26:
    #  _VERBOSE = 2
    return this.Drop(500, 0)


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


def Sample(ground):
  ground.Print()
  for i in range(5):
    ground.NewDrop()
  ground.Print()
  for i in range(5):
    ground.NewDrop()
  ground.Print()
  for i in range(4):
    ground.NewDrop()
  ground.Print()
  for i in range(13):
    ground.NewDrop()
  for i in range(3):
    ground.NewDrop()
    ground.Print()


def part1(ground):
  # ground.Print()
  while True:
    if not ground.NewDrop():
      break


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

  if sys.argv[iarg] == 'sample.txt':
    Sample(ground)
    sys.exit(0)

  part1(ground)
  print('%d tiles are wet' % ground.nWet())


"""
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
