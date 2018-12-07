from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import sys

"""
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination
indeterminate. Chronal interference detected. Please specify new target
coordinates."

The device then produces a list of coordinates (your puzzle input). Are
they places it thinks are safe or dangerous? It recommends you check
manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the
coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each
coordinate by counting the number of integer X,Y locations that are
closest to that coordinate (and aren't tied in distance to any other
coordinate).

Your goal is to find the size of the largest area that isn't infinite. For
example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0
at the top left:
..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all
directions. Using the Manhattan distance, each location's closest
coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates,
and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite -
while not shown here, their areas extend forever outside the visible
grid. However, the areas of coordinates D and E are finite: D is closest
to 9 locations, and E is closest to 17 (both including the coordinate's
location itself). Therefore, in this example, the size of the largest
area is 17.

What is the size of the largest area that isn't infinite?
"""

class Point(object):

  id = 0

  def __init__(this, x, y):
    this.id = Point.id
    Point.id += 1
    this.x = x
    this.y = y
    this.size = 0
    this.infinite = False
    this.frontier = set()
    this.add_to_frontier(x,y)

  def __str__(this):
    ret = '%d: %d,%d, size:%d' % (this.id, this.x, this.y, this.size)
    if this.infinite:
      ret += '-infinite'
    return ret

  def add_to_frontier(this, x, y):
    this.frontier.add((x,y))


class Cell(object):

  def __init__(this, id, dist):
    this.id = id
    this.dist = dist

  def __str__(this):
    return 'C(#%d, %d)' % (this.id, this.dist)


class Grid(object):

  def __init__(this, max_x, max_y):
    this.grid = {}
    this.max_x = max_x
    this.max_y = max_y

  def at(this, x, y):
    return this.grid.get(y * this.max_x + x)

  def take(this, x, y, point, dist, cell=None):
    #if this.at(x, y):
    #   raise ValueError('point %d,%d already taken: %s' % (x, y, this.at(x,y)))
    # print('%s taking %d,%d' % (point, x, y))
    if not cell:
      this.grid[y * this.max_x + x] = Cell(point.id, dist)
    point.size += 1
    point.add_to_frontier(x,y)

  def untake(this, x, y, point, other):
    if not this.at(x, y):
      raise ValueError('point %d,%d already taken' % (x, y))
    print('%s giving up %d,%d because #%d' % (point, x, y, other))
    this.grid[y * this.max_x + x] = Cell(-1, -1)
    point.size -= 1
    point.frontier.remove((x,y))

  def expand(this, x, y, point, points, dist):
    expanded = False
    for delta in ((-1,0), (1,0), (0,-1), (0,1)):
      x1 = x + delta[0]
      y1 = y + delta[1]
      if x1 < 0 or y1 < 0 or x1 >= this.max_x or y1 >= this.max_y:
        point.infinite = True
        continue
      cell = this.at(x1, y1)
      if cell:
        if cell.dist < 0:  # equidistant
          continue
        # Cell taken in same distance round
        if cell.dist == dist and cell.id != point.id:
          this.untake(x1, y1, points[cell.id], point.id)
      else:
        this.take(x1, y1, point, dist)
        expanded = True
    return expanded

  def flood(this, x, y, point, dist):
    expanded = False
    for delta in ((-1,0), (1,0), (0,-1), (0,1)):
      x1 = x + delta[0]
      y1 = y + delta[1]
      if x1 < 0 or y1 < 0 or x1 >= this.max_x or y1 >= this.max_y:
        point.infinite = True
        continue
      cell = this.at(x1, y1)
      if cell:
        if cell.id != point.id:
          cell.id = point.id
          cell.dist += dist
          this.take(x1, y1, point, dist, cell=cell)
          # print('flooded %d,%d to %s' % (x1,y1, cell))
          if this.at(x1, y1) != cell:
            raise ValueError('foowey')
          expanded = True
      else:
        if point.id > 0:
          raise ValueError("WTF no cell at %d,%d" % (x,y))
        this.take(x1, y1, point, dist)
        expanded = True
    return expanded


def LoadPoints(inp):
  points = []
  for line in inp:
    x, y = line.split(',')
    x = int(x)
    y = int(y)
    points.append(Point(x,y))
  return points


def part1(points, g):
  for p in points:
    g.take(p.x, p.y, p, 0)
    # print(str(p))

  dist = 0
  while True:
    dist = dist + 1
    expanded = False
    for p in points:
      # Copy frontier first
      f = set(p.frontier)
      p.frontier = set()
      for x, y in f:
        expanded |= g.expand(x, y, p, points, dist)
    if not expanded:
      break

  for p in points:
    if not p.infinite:
      print('bounded: %s' % str(p))


"""
On the other hand, if the coordinates are safe, maybe the best you can
do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all
of the coordinates to be less than 32. For each location, add up the
distances to all of the given coordinates; if the total of those distances
is less than 32, that location is within the desired region. Using the
same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a
total distance to all given coordinates of less than 10000?
"""

def part2(points, g):
  for p in points:
    print('# Begin flood fill from %s' % p)
    g.take(p.x, p.y, p, 0, cell=g.at(p.x, p.y))
    dist = 0
    while True:
      dist = dist + 1
      expanded = False
      f = set(p.frontier)
      p.frontier = set()
      for x, y in f:
        expanded |= g.flood(x, y, p, dist)
      if not expanded:
        break
    print('# flood fill from %s: max distance %d' % (p, dist))

  for y in range(g.max_y):
    for x in range(g.max_x):
      cell = g.at(x, y)
      if cell.dist < 10000:
        print('cell: %d,%d: %d' % (x, y, dist))


if __name__ == '__main__':
  with open(sys.argv[1]) as inp:
    points = LoadPoints(inp)
  max_x = max_y = 0
  for p in points:
    max_x = max(max_x, p.x)
    max_y = max(max_y, p.y)

  # part1(points, Grid(max_x, max_y))
  part2(points, Grid(max_x, max_y))
