"""aoc 2018 day 23"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import sys

# from memoized import memoized

_VERBOSE = 0
_PART2 = False


class Bot(object):

  def __init__(this, x, y, z, radius):
    this.x = x
    this.y = y
    this.z = z
    this.radius = radius
    this.mouth = (0,0)

  def __str__(this):
    return 'pos=<%d,%d,%d>, r=%d' % (this.x, this.y, this.z, this.radius)

  @staticmethod
  def Parse(l):
    # pos=<1,3,1>, r=1
    if not l.startswith('pos=<'):
      raise ValueError('expected pos=< in "%s"' % l)
    close_b = l.find('>')
    coords = [int(c) for c in l[5:close_b].split(',')]
    r_pos = l.find('r=')
    radius = int(l[r_pos+2:])
    return Bot(coords[0], coords[1], coords[2], radius)

  def dist(this, b):
    return abs(b.x - this.x) + abs(b.y - this.y) + abs(b.z - this.z) 


def SelfCheck(bots):
  pass


def part1(bots):
  max_r = bots[0]
  for b in bots:
    if b.radius > max_r.radius:
      max_r = b
  print('bot with max radius is %s' % max_r)
  n_close = 0
  for b in bots:
    if max_r.dist(b) <= max_r.radius:
      n_close += 1
  print('%d bots are in range' % n_close)


def part2(bots):
  # compute bounding box of search
  x_min = x_max = bots[0].x
  y_min = y_max = bots[0].y
  z_min = z_max = bots[0].z
  for b in bots:
    if b.x < x_min:
      x_min = b.x
    if b.x > x_max:
      x_max = b.x
    if b.y < y_min:
      y_min = b.y
    if b.y > y_max:
      y_max = b.y
    if b.z < z_min:
      z_min = b.z
    if b.z > z_max:
      z_max = b.z
  print('bounds = %d-%d, %d-%d, %d-%d' % (x_min, x_max, y_min, y_max,
                                          z_min, z_max))

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

  bots = []
  with open(sys.argv[iarg]) as inp:
    for l in inp:
      bots.append(Bot.Parse(l.strip()))
  if dump:
    for b in bots:
      print(b)
  SelfCheck(bots)

  part1(bots)
  part2(bots)

