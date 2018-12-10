"""day10 puzzle"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import re
import sys


class Point(object):
  def __init__(this, x, y, vx, vy):
    this.start_x = x
    this.start_y = y
    this.vx = vx
    this.vy = vy
    this.x = x
    this.y = y

  def __str__(this):
    return '(%d,%d -> %d,%d)' % (this.x, this.y, this.vx, this.vy)

  def move(this, n_seconds):
    this.x = this.x + n_seconds * this.vx
    this.y = this.y + n_seconds * this.vy


def LoadPoints(inp):
  # position=< 9,  1> velocity=< 0,  2>
  pat = re.compile(
      r'position=< *([-0-9]*), *([-0-9]*)>'
      ' *velocity=< *([-0-9]*), *([-0-9]*)>.*')
  ret = []
  for l in inp:
    m = pat.match(l.strip())
    p = Point(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    ret.append(p)
  return ret

class Grid(object):

  def __init__(this):
    this.min_x = 0
    this.min_y = 0
    this.max_x = 0
    this.max_y = 0
    this.points = []
    this.time = 0

  def Add(this, point):
    this.points.append(point)

  def _Map(this, point):
    if point.x < this.min_x:
      this.min_x = point.x
    if point.y < this.min_y:
      this.min_y = point.y
    if point.x > this.max_x:
      this.max_x = point.x
    if point.y > this.max_y:
      this.max_y = point.y
    this.points[(point.x, point.y)] = point

  def Print(this):
    coord_map = {}
    print('=== t:%d' % this.time)
    for point in this.points:
      if point.x < this.min_x:
        this.min_x = point.x
      if point.y < this.min_y:
        this.min_y = point.y
      if point.x > this.max_x:
        this.max_x = point.x
      if point.y > this.max_y:
        this.max_y = point.y
      coord_map[(point.x, point.y)] = point

    for y in range(this.min_y, this.max_y+1):
      for x in range(this.min_x, this.max_x+1):
        p = coord_map.get((x, y))
        if p:
          sys.stdout.write('#')
        else:
          sys.stdout.write('.')
      sys.stdout.write('\n')

  def PassTime(this, seconds):
    this.time += seconds
    for point in this.points:
      point.move(seconds)


def sample(g):
  g.Print()
  g.PassTime(1)
  g.Print()
  g.PassTime(2)
  g.Print()


if __name__ == '__main__':
  verbose = False
  iarg = 1
  if sys.argv[iarg] == '-v':
    verbose = True
    iarg += 1
  with open(sys.argv[iarg]) as inp:
    points = LoadPoints(inp)

  g = Grid()
  for p in points:
    g.Add(p)
  sample(g)
