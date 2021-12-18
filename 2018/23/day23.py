"""aoc 2018 day 23"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import copy
import heapq
import sys

from tools import aoc

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

  def __init__(self, x, y, z, radius):
    self.x = x
    self.y = y
    self.z = z
    self.radius = radius
    self.mouth = (0,0)

  def __str__(self):
    return 'pos=<%d,%d,%d>, r=%d' % (self.x, self.y, self.z, self.radius)

  def __repr__(self):
    return str(self)

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

  def dist(self, b):
    return abs(b.x - self.x) + abs(b.y - self.y) + abs(b.z - self.z)

  def InRange(self, x, y, z):
    return (abs(x - self.x) + abs(y - self.y) + abs(z - self.z)) <= self.radius

  def ZRange(self, x, y):
    # returns range of z cells in range for an x, y coord
    xy_dist = abs(x - self.x) + abs(y - self.y)
    # inrange = xy_dist + abs(z - self.z)) < self.radius
    # inrange = abs(self.z - z)) < (self.radius - xy_dist)
    # inrange = self.z - Z < (self.radius - xy_dist)
    #       or  self.z + Z < (self.radius - xy_dist)
    delta = self.radius - xy_dist
    if delta < 0:
      return None
    return (self.z - delta, self.z + delta)


class Cave(object):

  def __init__(this, bots):
    this.bots = bots
    this.x_min = 0
    this.x_max = 0
    this.y_min = 0
    this.y_max = 0
    this.z_min = 0
    this.z_max = 0
    # current guess at maximum number of bots reachable from any cell
    this.max_bots = 0
    this.max_pos = (0,0,0)
    # transient for reduce phase
    this.n_at_max = 0
    this.ComputeBounds()
    this.closest = this.x_span + this.y_span + this.z_span
    this.ComputeBounds()

  def Print(this):
    print('%d cells are within range of %d bots' % (this.n_at_max, this.max_bots))
    print('max cell @ %d,%d,%d' % (this.max_pos[0], this.max_pos[1], this.max_pos[2]))
    print('x: %d-%d (%d)' % (this.x_min, this.x_max, this.x_span))
    print('y: %d-%d (%d)' % (this.y_min, this.y_max, this.y_span))
    print('z: %d-%d (%d)' % (this.z_min, this.z_max, this.z_span))
    sys.stdout.flush()

  @property
  def x_span(this):
    return this.x_max - this.x_min + 1

  @property
  def y_span(this):
    return this.y_max - this.y_min + 1

  @property
  def z_span(this):
    return this.z_max - this.z_min + 1

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

  def ZRange(this, bot, x, y):
    r = b.ZRange(x, y)
    if not r:
      return None
    z_from = max(this.z_min, r[0])
    z_to = min(this.z_max+1, r[1]+1)
    return (z_from, z_to)

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

  def Reduce(this, max_pos, percentage):
    # percentage to leave
    trim = int(this.x_span * percentage/2.0)
    this.x_min = max_pos[0] - trim
    this.x_max = max_pos[0] + trim
    trim = int(this.y_span * percentage/2.0)
    this.y_min = max_pos[1] - trim
    this.y_max = max_pos[1] + trim
    trim = int(this.z_span * percentage/2.0)
    this.z_min = max_pos[2] - trim
    this.z_max = max_pos[2] + trim

  def SearchRange(this, x_from, x_to, y_from, y_to, z_from, z_to):
    x_step = y_step = z_step = 1
    if x_from > x_to:
      x_step = -1
    if y_from > y_to:
      y_step = -1
    if z_from > z_to:
      z_step = -1
    for z in range(z_from, z_to, z_step):
      for y in range(y_from, y_to, y_step):
        for x in range(x_from, x_to, x_step):
          dist = x + y + z
          # print('  check: %d,%d,%d at distance %d' % (x, y, z, dist))
          if dist > this.closest:
            break
          in_range = 0
          for b in cave.bots:
            if b.InRange(x, y, z):
              in_range += 1
          if in_range > cave.max_bots:
            raise ValueError('!!!! Too many in range %d > %d' % (
                in_range, this.max_bots))
          elif in_range == cave.max_bots:
            print('..cell %d,%d,%d at distance %d' % (x, y, z, dist))
            sys.stdout.flush()
            if dist < this.closest:
              this.closest = dist
          else:
            # print('wandered out of region')
            break

  def FindTheMaximumRegion(this):
    global _VERBOSE

    n_buckets = 8
    max_pos = None
    n_passes_unchanged = 0
    reduce_factor = .50
    while True:
      max_bots_before = this.max_bots
      n_at_max_before = this.n_at_max
      try:
        print('== Trying sample and reduce: x_span=%d' % this.x_span)
        max_pos = this.SampleSpace(n_buckets)
        this.Reduce(max_pos, reduce_factor)
      except ValueError as e:
        break
      if this.n_at_max > 10:
        reduce_factor = .80
      # if this.n_at_max > 30:
      #   _VERBOSE = True
      if (max_bots_before == this.max_bots
          and n_at_max_before == this.n_at_max
          and max_bots_before > 900):
        n_passes_unchanged += 1
        print('  -> unchanged for %d passes' % n_passes_unchanged)
      else:
        n_passes_unchanged = 0
      if n_passes_unchanged > 4:
        print('  -> unchanged too long. done')
        break
      if (this.x_span < 100
          or this.y_span < 100
          or this.z_span < 100):
        print('  -> spans got smaller than 100')
        break
    this.max_pos = (int(this.max_pos[0] + this.x_span / n_buckets),
                    int(this.max_pos[1] + this.y_span / n_buckets),
                    int(this.max_pos[2] + this.z_span / n_buckets))


def part2_simple(cave):
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
  # part2_1(cave)


def part2_last_from_2018(cave):
  # cave.FindTheMaximumRegion()
  cave.max_bots = 936
  cave.max_pos = (44166763,43552646,38657871)
  cave.z_min = 38651590
  cave.z_max = 38665170
  cave.Print()
  part2_3(cave)


def part2_quick(cave):
  cave.x_min = 44229168
  cave.x_max = 44229328
  cave.y_min = 43740050
  cave.y_max = 43740180
  cave.z_min = 38782806
  cave.z_max = 38782906
  cave.max_pos = (44229250,43740238,38782982)
  cave.max_bots = 909
  part2_1(cave)

def part2_3(cave):
  cave.closest = cave.x_max + cave.y_max + cave.z_max
  x = cave.max_pos[0]
  y = cave.max_pos[1]

  NarrowFrom(cave, x, y, 10000)
  x = cave.last_x
  y = cave.last_y
  NarrowFrom(cave, x, y, 1000)
  x = cave.last_x
  y = cave.last_y
  NarrowFrom(cave, x, y, 100)
  x = cave.last_x
  y = cave.last_y
  NarrowFrom(cave, x, y, 10)
  x = cave.last_x
  y = cave.last_y
  NarrowFrom(cave, x, y, 1)


def NarrowFrom(cave, x, y, step):
  dec_x = True
  stale_count = 0
  while x > 0 and y > 0 and stale_count < 10:
    print('NarrowFrom @ %d,%d, zspan=%d' % (x, y, cave.z_span))
    col = [0] * (cave.z_span + 1)
    n_fails = 0
    for b in cave.bots:
      r = b.ZRange(x, y)
      if not r:
        n_fails += 1
        if n_fails > len(cave.bots) - cave.max_bots:
          print('=== easy skip')
          break
        continue
      z_from = max(cave.z_min, r[0])
      z_to = min(cave.z_max+1, r[1]+1)
      # print('  reaching z=%d-%d' % (z_from, z_to))
      for z in range(z_from, z_to):
        col[z - cave.z_min] += 1

    found_any = False
    for zi in range(cave.z_span+1):
      z = cave.z_min + zi
      in_range = col[zi]
      if in_range > cave.max_bots:
        print('!! Too many in range %d > %d' % (in_range, cave.max_bots))
        sys.stdout.flush()
        cave.closest = cave.x_max + cave.y_max + cave.z_max
        cave.max_bots = in_range
      elif in_range == cave.max_bots:
        found_any = True
        dist = x + y + z
        if dist < cave.closest:
          print('%d, cell %d,%d,%d new closest' % (dist, x, y, z))
          cave.closest = dist
      # else:
      #   print('cell %d,%d,%d not in range' % (x, y, z))
      sys.stdout.flush()
    if found_any:
      stale_count = 0
      print('Something at x,y=%d,%d' % (x, y))
      sys.stdout.flush()
      cave.last_x = x
      cave.last_y = y
    else:
      stale_count += 1
      print('nothing for %d,%d' % (x, y))
      sys.stdout.flush()

    # move left or right
    if dec_x:
      dec_x = False
      x -= step
    else:
      dec_x = True
      y -= step


def part2_2(cave):
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


def part2_1(cave):
  # x: 44229168-44229328 (160)
  # y: 43740050-43740180 (130)
  # z: 38782806-38782906 (100)
  #cave.x_min -= 200
  #cave.y_min -= 300
  #cave.y_max -= 10
  #cave.z_min -= 500

  cave.Print()

  for z in range(cave.z_min, cave.z_max):
    for y in range(cave.y_min, cave.y_max):
      for x in range(cave.x_min, cave.x_max):
        if x + y + z > cave.closest:
          break
        in_range = 0
        for b in cave.bots:
          if b.InRange(x, y, z):
            in_range += 1
        if in_range > cave.max_bots:
          raise ValueError('!!!! Too many in range %d > %d' % (in_range, cave.max_bots))
        elif in_range == cave.max_bots:
          dist = x + y + z
          print('cell %d,%d,%d at distance %d' % (x, y, z, dist))
          sys.stdout.flush()
          if dist < cave.closest:
            cave.closest = dist
            if x == cave.x_min:
              print('Point x too low : %d,%d,%d' % (x,y,z))
              cave.SearchRange(x, 0, y-1, y+1, z-1, z+1)
            if y == cave.y_min:
              print('Point y too low : %d,%d,%d' % (x,y,z))
              cave.SearchRange(x-1, x+1, y, 0, z-1, z+1)
            if z == cave.z_min:
              print('Point y too low : %d,%d,%d' % (x,y,z))
              cave.SearchRange(x, x, y, y, z, 0)
            if x == cave.x_max or y == cave.y_max or z == cave.z_max:
              raise ValueError('Point too high: %d,%d,%d' % (x,y,z))
        else:
          break

class Range(object):

   def __init__(self, pos, radius):
     self.low = pos - radius
     self.high = pos + radius
     self.nbots = 1

   def __str__(self):
     return '%d-%d(%d)' % (self.low, self.high, self.nbots)

   def __lt__(self, o):
     return self.low < o.low

   def intersect(self, r):
     return ((self.low <= r.low and r.low <= self.high) or
             (self.low <= r.high and r.high <= self.high) or
             (r.low <= self.low and self.low <= r.high) or
             (r.low <= self.high and self.high <= r.high) 
             )

   def combine(self, r):
     #  self:       sss
     #        1: rrr         ->  r, self
     #        2: rrrr        ->  r'(1), self(+1), self(short)
     #        3: rrrrrr      ->  r'(1), self(+1)
     #        4: rrrrrrrrr   ->  r'(1), self(+1), r''(1)
     obots = self.nbots + r.nbots
     if r.low < self.low:
        ret = [r, self]
        if r.high < self.low:  # case 1
          return ret
        rh = r.high                # clip r
        r.high = self.low - 1
        if rh < self.high:          # case 2, split s
          s2 = copy.copy(self)
          s2.low = self.high + 1
          # print("     ===> case2, made", s2)
          ret.append(s2)
        elif rh > self.high:   # case 4, clip r
          r2 = copy.copy(r)
          r2.low = self.high + 1
          r2.high = rh
          ret.append(r2)
          # print("     ===> case4, made", r2)
        self.nbots = obots
        return ret

     #  self:       sss
     #        5:    rrr      ->  self'(+1)
     #        6:    r        ->  r1, self'(+1)
     #        7:    rrrr     ->  self(+1), r'
     if r.low == self.low:
       self.nbots = obots
       if r.high == self.high:   # case 5
         return [self]
       if r.high < self.high:    # case 6 (s+ | r)
         if r.high == 15:
           self.low = r.high + 1
           print(' ==== change self to', self, 'r=', r)
           return [r, self]
       r.low = self.high + 1  # case 7
       return [self, r]

     #  self:      ssss
     #        8:    rr       ->  self(short), r1'(+1), self'(short)
     #        9:     rr      ->  self(short), r1'(+1)
     #       10:      rr     ->  self(short), r1'(+1), r1''short)
     if r.low <= self.high:
       old_s_high = self.high
       self.high = r.low - 1
       ret = [self, r]
       if r.high < old_s_high:    # case 8, split s
         r.nbots = obots
         s2 = copy.copy(self)
         s2.low = r.high + 1
         s2.high = old_s_high
         ret.append(s2)
       elif r.high == old_s_high: #  case 9
         r.nbots = obots
       else:                      # case 10
         r2 = copy.copy(r)
         r2.low = old_s_high + 1
         r.high = old_s_high
         r.nbots = obots
         ret.append(r2)
       return ret
     print("HELP", self, r)
     sys.exit(1)

class Spans(object):
  def __init__(self):
    self.spans = None

  def add(self, r):
    if not self.spans:
      self.spans = [r]
      return
    done = []
    nxt = 0
    retry = None
    while r and nxt < len(self.spans):
      s = self.spans[nxt]
      if s.low > r.high:
        # print('    break at', s)
        break
      nxt += 1
      # print('    check', s)
      if s.intersect(r):
        what = s.combine(r)
        # print('      split:', [str(x) for x in what])
        done.extend(what[0:-1])
        r = what[-1]
        # print('  re-add', r)
    if r:
      done.append(r)
    self.spans = done + self.spans[nxt:]

def part2(cave):
  print('--- start part 2')
  max_pos = None

  sx = Spans()
  i = 100
  for b in cave.bots:
    if i % 100 == 0:
      print(' === loop ', i)
    r = Range(b.x, b.radius)
    if _VERBOSE:
      print('add:', r)
    sx.add(r)
    if _VERBOSE:
      print('    =>', [str(r) for r in sx.spans])
  sy = Spans()
  for b in cave.bots:
    sy.add(Range(b.y, b.radius))
  sz = Spans()
  for b in cave.bots:
    sz.add(Range(b.z, b.radius))

  print('y   =>', [str(r) for r in sy.spans])
  print('z   =>', [str(r) for r in sz.spans])
  m = 0
  for r in sx.spans:
    if r.nbots > m:
      m = r.nbots
      x = r.low
  m = 0
  for r in sy.spans:
    if r.nbots > m:
      m = r.nbots
      y = r.low
  m = 0
  for r in sz.spans:
    if r.nbots > m:
      m = r.nbots
      z = r.low
  cave.point = (x, y, z)
  print('point', cave.point)
  return x + y + z

  """
  for x in range(cave.x_min, cave.x_max):
    for bot in range(
    this.x_min = 0
    this.x_max = 0
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
  """
  pass




def part1(cave):
  max_r = cave.bots[0]
  for b in cave.bots:
    if b.radius > max_r.radius:
      max_r = b
  print('bot with max radius is %s' % max_r)
  n_close = 0
  for b in cave.bots:
    if max_r.dist(b) <= max_r.radius:
      n_close += 1
  print('%d bots are in range' % n_close)
  return n_close


def bots_from_text(s):
  bots = []
  for line in s.split('\n'):
    l = line.strip()
    if l:
      bots.append(Bot.Parse(l))
  return bots


def SelfTest():
  print('== self test ==')
  bots = bots_from_text("""
      pos=<0,0,0>, r=4
      pos=<1,0,0>, r=1
      pos=<4,0,0>, r=3
      pos=<0,2,0>, r=1
      pos=<0,5,0>, r=3
      pos=<0,0,3>, r=1
      pos=<1,1,1>, r=1
      pos=<1,1,2>, r=1
      pos=<1,3,1>, r=1
      """)
  cave = Cave(bots)
  cave.Print()
  print('== self test part 1==')
  aoc.run_func(lambda: part1(cave), tag='self_test part1', expect = 7)


  # part2 test
  bots = bots_from_text("""
      pos=<10,12,12>, r=2
      pos=<12,14,12>, r=2
      pos=<16,12,12>, r=4
      pos=<14,14,14>, r=6
      pos=<50,50,50>, r=200
      pos=<10,10,10>, r=5
      """)
  cave = Cave(bots)
  cave.Print()
  assert cave.x_min == 10 and cave.x_max == 50
  assert cave.y_min == 10 and cave.y_max == 50
  assert cave.z_min == 10 and cave.z_max == 50

  # test range functions on bots
  for x in range(cave.x_min, cave.x_max+1):
    for y in range(cave.y_min, cave.y_max+1):
      # print('== %d,%d ==' % (x, y))
      for b in cave.bots:
        r = b.ZRange(x, y)
        if not r:
          # print('  %s: NIL' % b)
          continue
        # print('  %s: %d-%d' % (b, r[0], r[1]))
        for z in range(r[0], r[1]+1):
          if not b.InRange(x, y, z):
            print('  %s: %d-%d: %d,%d,%d should be in range, is not' % (
                b, r[0], r[1], x, y, z))
            return 1
        assert not b.InRange(x, y, r[0]-1)
        assert not b.InRange(x, y, r[1]+2)
  cells = []
  cave.max_bots = 0
  for x in range(cave.x_min, cave.x_max+1):
    y_vec = []
    for y in range(cave.y_min, cave.y_max+1):
      col = [0] * cave.z_span
      for b in cave.bots:
        r = b.ZRange(x, y)
        if not r:
          continue
        z_from = max(cave.z_min, r[0])
        z_to = min(cave.z_max+1, r[1]+1)
        for z in range(z_from, z_to):
          col[z - cave.z_min] += 1
          if cave.max_bots < col[z - cave.z_min]:
            cave.max_bots = col[z - cave.z_min]
      y_vec.append(col)
    cells.append(y_vec)

  # Brute force part2
  best_dist = cave.x_span + cave.y_span + cave.z_span
  for xi in range(cave.x_span):
    x_row = cells[xi]
    for yi in range(cave.y_span):
      z_col = x_row[yi]
      for zi in range(cave.z_span):
        assert z_col[zi] <= cave.max_bots
        if z_col[zi] == cave.max_bots:
          x = cave.x_min + xi
          y = cave.y_min + yi
          z = cave.z_min + zi
          print(' -> %d,%d,%d is at max' % (x, y, z))
          dist_from_origin = x + y + z
          if dist_from_origin < best_dist:
            best_dist = dist_from_origin
            best_pos = (x,y,z)
  # print(best_pos)

  global _VERBOSE
  _VERBOSE = 1
  aoc.run_func(lambda: part2(cave), tag='self_test part2', expect = 36)
  expect = (12, 12, 12)
  if expect != cave.point:
    print('FAIL: self_test part2: wrong point. expected', expect, 'got', cave.point)
    sys.exit(1)
  _VERBOSE = 0
  return 0


if __name__ == '__main__':
  iarg = 1
  dump = False
  tests = False
  while iarg < len(sys.argv) and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      _VERBOSE += 1
      iarg += 1
    if sys.argv[iarg] == '-d':
      dump = True
      iarg += 1
    if sys.argv[iarg] == '-t':
      tests = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      iarg += 1

  if tests:
    sys.exit(SelfTest())

  bots = []
  with open(sys.argv[iarg]) as inp:
    for l in inp:
      bots.append(Bot.Parse(l.strip()))
  cave = Cave(bots)
  if dump:
    for b in cave.bots:
      print(b)

  aoc.run_func(lambda: part1(cave), tag='self_test part1', expect = 297)

  if _PART2:
    # part2_quick(cave)
    # part2(cave)
    res = part2(cave)
