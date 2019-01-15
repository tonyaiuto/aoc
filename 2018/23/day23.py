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


def cluster_step(low, high, n_buckets):
  step = int((high - low) / n_buckets)
  if step < 1:
    step = 1
  # print('cluster step from %d to %d by %d' % (low, high, step))
  for i in range(n_buckets):
    yield i, (low + step * i)


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

  def InRange(this, x, y, z):
    return (abs(x - this.x) + abs(y - this.y) + abs(z - this.z)) < this.radius


class Cave(object):

  def __init__(this, bots):
    this.bots = bots
    this.x_min = 0
    this.x_max = 0
    this.y_min = 0
    this.y_max = 0
    this.z_min = 0
    this.z_max = 0
    this.max_bots = 0
    this.n_at_max = 0
    this.max_pos = (0,0,0)

  def Print(this):
    print('%d cells are within range of %d bots' % (this.n_at_max, this.max_bots))
    print('max cell @ %d,%d,%d' % (this.max_pos[0], this.max_pos[1], this.max_pos[2]))
    print('x: %d-%d (%d)' % (this.x_min, this.x_max, this.x_span))
    print('y: %d-%d (%d)' % (this.y_min, this.y_max, this.y_span))
    print('z: %d-%d (%d)' % (this.z_min, this.z_max, this.z_span))
    sys.stdout.flush()

  @property
  def x_span(this):
    return this.x_max - this.x_min

  @property
  def y_span(this):
    return this.y_max - this.y_min

  @property
  def z_span(this):
    return this.z_max - this.z_min

  def ComputeBounds(this):
    # compute bounding box of search
    this.x_min = this.x_max = this.bots[0].x
    this.y_min = this.y_max = this.bots[0].y
    this.z_min = this.z_max = this.bots[0].z
    for b in this.bots:
      if b.x < this.x_min:
        this.x_min = b.x
      if b.x > this.x_max:
        this.x_max = b.x
      if b.y < this.y_min:
        this.y_min = b.y
      if b.y > this.y_max:
        this.y_max = b.y
      if b.z < this.z_min:
        this.z_min = b.z
      if b.z > this.z_max:
        this.z_max = b.z
    print('bounds = %d-%d, %d-%d, %d-%d' % (this.x_min, this.x_max,
                                            this.y_min, this.y_max,
                                            this.z_min, this.z_max))

  def SampleSpace(this, n_buckets):
    cells = []
    max_bots = 0
    max_pos = None
    for iz, z in cluster_step(this.z_min, this.z_max, n_buckets):
      rows = []
      for iy, y in cluster_step(this.y_min, this.y_max, n_buckets):
        row = [0] * (n_buckets + 1)
        for ix, x in cluster_step(this.x_min, this.x_max, n_buckets):
          for b in this.bots:
            if b.InRange(x, y, z):
              row[ix] += 1
              if row[ix] > max_bots:
                max_bots = row[ix]
                max_pos = (x, y, z)
        rows.append(row)
      cells.append(rows)
    if _VERBOSE:
      for iz, z in cluster_step(this.z_min, this.z_max, n_buckets):
        print('========== z: %d' % z)
        layer = cells[iz]
        for row in layer:
          print(row)
    print('max cell = %d at %d,%d,%d' % (max_bots, max_pos[0], max_pos[1], max_pos[2]))
    if max_bots < this.max_bots:
      raise ValueError('max cell reduced from previous of %d' % this.max_bots)
    if max_bots > this.max_bots:
      this.max_bots = max_bots 
    this.n_at_max = 0
    for layer in cells:
      for row in layer:
        this.n_at_max += sum([1 for c in row if c == this.max_bots])
    print('%d cells are at max' % this.n_at_max)
    this.max_pos = max_pos
    return max_pos

  def Reduce(this, max_pos):
    divisor = 5
    trim = int((this.x_max - this.x_min) / divisor)
    this.x_min = max_pos[0] - trim
    this.x_max = max_pos[0] + trim
    trim = int((this.y_max - this.y_min) / divisor)
    this.y_min = max_pos[1] - trim
    this.y_max = max_pos[1] + trim
    trim = int((this.z_max - this.z_min) / divisor)
    this.z_min = max_pos[2] - trim
    this.z_max = max_pos[2] + trim

def part2(cave):
  cave.ComputeBounds()
  n_buckets = 8
  max_pos = None
  while True:
    max_bots_before = cave.max_bots
    n_max_before = cave.n_at_max
    try:
      max_pos = cave.SampleSpace(n_buckets)
      cave.Reduce(max_pos)
    except ValueError as e:
      break
    if (max_bots_before == cave.max_bots
        and n_max_before == cave.n_at_max
        and max_bots_before > 900):
      break
    if (cave.x_span < 100
        or cave.y_span < 100
        or cave.z_span < 100):
      break
  cave.Print()

  closest = max_pos[0] + max_pos[1] + max_pos[2] + 500
  for z in range(max_pos[2]+100, 0, -1):
    print('Trying z=%d' % z)
    sys.stdout.flush()
    for y in range(max_pos[1]+100, 0, -1):
      print('Trying y=%d' % y)
      for x in range(max_pos[0]+100, 0, -1):
        dist = x + y + z
        if dist > closest:
          break
        in_range = 0
        for b in cave.bots:
          if b.InRange(x, y, z):
            in_range += 1
        if in_range > cave.max_bots:
          raise ValueError('!!!! Too many in range %d > %d' % (in_range, cave.max_bots))
        elif in_range == cave.max_bots:
          print('cell %d,%d,%d at distance %d' % (x, y, z, dist))
          sys.stdout.flush()
          if dist < closest:
            closest = dist
        else:
          break
 

def part2_b(cave):
  # x: 44229168-44229328 (160)
  # y: 43740050-43740180 (130)
  # z: 38782806-38782906 (100)
  cave.x_min -= 200
  cave.y_min -= 300
  cave.y_max -= 10 
  cave.z_min -= 500

  cave.Print()

  # layers = []
  closest = cave.x_max + cave.y_max + cave.z_max
  for z in range(cave.z_min, cave.z_max):
    # rows = []
    for y in range(cave.y_min, cave.y_max):
      # row = []
      for x in range(cave.x_min, cave.x_max):
        if x + y + z > closest:
          break
        in_range = 0
        for b in cave.bots:
          if b.InRange(x, y, z):
            in_range += 1
        if in_range > cave.max_bots:
          raise ValueError('!!!! Too many in range %d > %d' % (in_range, cave.max_bots))
        if in_range == cave.max_bots:
          dist = x + y + z
          print('cell %d,%d,%d at distance %d' % (x, y, z, dist))
          sys.stdout.flush()
          if dist < closest:
            closest = dist
          if x == cave.x_min or y == cave.y_min or z == cave.z_min:
            raise ValueError('Point too low: %d,%d,%d' % (x,y,z))
          if x == cave.x_max or y == cave.y_max or z == cave.z_max:
            raise ValueError('Point too high: %d,%d,%d' % (x,y,z))
        # row.append(in_range)
      # rows.append(row)
    # layers.append(rows)

def SelfCheck(bots):
  pass


def part1(cave):
  max_r = cave.bots[0]
  for b in bots:
    if b.radius > max_r.radius:
      max_r = b
  print('bot with max radius is %s' % max_r)
  n_close = 0
  for b in cave.bots:
    if max_r.dist(b) <= max_r.radius:
      n_close += 1
  print('%d bots are in range' % n_close)


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
  cave = Cave(bots)
  if dump:
    for b in cave.bots:
      print(b)

  part1(cave)
  if _PART2:
    part2(cave)

