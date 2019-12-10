#!/usr/bin/env python3

import math

class Map(object):

  def __init__(self):
    self.positions = []
    self.width = 0
    self.height = 0
    self.trace = False
    self.n_blasted = 0

  def load(self, path):
    with open(path, 'r') as inp:
      self.load_from_string(inp.read())

  def load_from_string(self, s):
    self.positions = []
    self.is_occupied = set()
    self.height = 0
    self.width = 0
    for line in s.strip().split('\n'):
       x = 0
       for c in line.strip():
         if c == '#' or c == 'X':
           self.positions.append((x, self.height))
           self.is_occupied.add((x, self.height))
         x += 1
       if self.width == 0:
         self.width = x
       else:
         assert self.width == x
       self.height += 1

  def reduce(self, dx, dy):
    # Reduce a slope to the smallest factor
    odx = dx
    ody = dy
    if dx == 0:
      dy = 1 if dy > 0 else -1
    elif dy == 0:
      dx = 1 if dx > 0 else -1
    else:
      did_reduce = True
      while did_reduce:
        did_reduce = False
        for factor in [2, 3, 5, 7, 11, 13, 17]:
          while dx % factor == 0 and dy % factor == 0:
            did_reduce = True
            msg = 'REDUCE dx,dy=%d,%d by %d' % (dx, dy, factor)
            dx = dx // factor
            dy = dy // factor
            # print(msg, 'to', dx, dy)
    if self.trace and (odx != dx or ody != dy):
      print('REDUCE %d,%d  to  %d,%d' % (odx, ody, dx, dy))
    return dx, dy


  def check_vis(self, my_pos):
    blocked = set()
    blocked.add(my_pos)
    for p in self.positions:
      if p in blocked:
        continue
      x = p[0]
      y = p[1]
      dx = x - my_pos[0]
      dy = y - my_pos[1]

      dx, dy = self.reduce(dx, dy)

      if self.trace and (odx != dx or ody != dy):
        print('REDUCE %d,%d  to  %d,%d' % (odx, ody, dx, dy))

      while True:
        x = x + dx
        y = y + dy
        if x < 0 or y < 0:
          break
        if x >= self.width or y >= self.height:
          break
        test_pos = (x, y)
        if self.trace:
          print('probe:', test_pos)
        if test_pos in self.is_occupied and test_pos != my_pos:
          if self.trace:
            print(my_pos, 'to', p, 'blocks', test_pos)
          blocked.add(test_pos)
    return len(self.positions) - len(blocked)


  def gen_sweep(self, center):
    center_x = center[0]
    for x in range(center_x, self.width):
      yield x, 0
    for y in range(1, self.height):
      yield self.width-1, y
    for x in range(self.width-2, -1, -1):
      yield x, self.height-1
    for y in range(self.height-2, -1, -1):
      yield 0, y
    for x in range(1, center_x):
      yield x, 0


  def to_polar(self, center, pos):
    """
     -x -y    |  +x -y
       -L  4  |    +L    1
    ----------|-------------
     -x +y    |  +x +y
       -H  3  |    +H    2
    
    atan2(y, x)
    -x +y +H 2   |  +x +y   +L   1
    ------------------------------- 
    -x +y -H 3   |  +x +y   -L   4

    """
    center_x = center[0]
    center_y = center[1]
    dist_x = pos[0] - center_x
    dist_y = pos[1] - center_y
    dist = abs(dist_x) + abs(dist_y)
    dx, dy = self.reduce(dist_x, dist_y)
    theta = math.atan2(dx, -dy)
    if theta < 0:
       theta = 2 * math.pi + theta
    if dx >= 0 and dy <= 0:
      if theta < 0:
         print(dx, dy, theta, 'expected positive theta')
      assert theta >= 0
    elif dx >= 0 and dy >= 0:
      assert theta >= math.pi / 2
      if theta < 0:
         print(dx, dy, theta, 'expected positive theta')
    elif dx < 0 and dy >= 0:
      assert theta > math.pi 
    else:
      assert dx < 0 and dy < 0
      assert theta > math.pi * 3 / 2
    return theta, dist


  def blast(self, center, stop_at=0):
    blasted = set()
    tmp = []
    for pos in self.is_occupied:
      if pos == center:
        continue
      theta, dist = self.to_polar(center, pos)
      # print('%s -> %s = %f, %d' % (center, pos, theta, dist))
      tmp.append((theta, dist, pos))

    s = sorted(tmp, key=lambda x: x[1])
    s = sorted(s, key=lambda x: x[0])
    last_theta = -1111
    for p in s:
      theta = p[0]
      pos = p[2]
      if last_theta != theta:
        last_theta = theta
        blasted.add(pos)
        self.n_blasted += 1
        print('blast', self.n_blasted, pos)
        if stop_at > 0 and self.n_blasted >= stop_at:
          break
      #else:
      #  print('NO blast:', pos)
    self.is_occupied = self.is_occupied - blasted


def load_and_pick_best(path):
  map = Map()
  map.load(path)
  return pick_best(map)


def pick_best(map):
  # print(map.positions)
  max_vis = 0
  max_pos = None
  for pos in map.positions:
    n_vis = map.check_vis(pos)
    # print('check_vis: %s sees %d others' % (pos, n_vis))
    if max_vis < n_vis:
      max_vis = n_vis
      max_pos = pos
  return max_pos, max_vis


def test1():
  max_pos, max_vis = load_and_pick_best('day10_map_1.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (3, 4)
  assert max_vis == 8

  max_pos, max_vis = load_and_pick_best('day10_map_2.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (6, 3)
  assert max_vis == 41

  max_pos, max_vis = load_and_pick_best('day10_map_2a.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (1, 2)
  assert max_vis == 35

  max_pos, max_vis = load_and_pick_best('day10_map_3.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (11, 13)
  # assert max_vis == 210


def part1():
  max_pos, max_vis = load_and_pick_best('input_10.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (17, 22)
  assert max_vis == 288



TEST_BLAST="""
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##
"""

def test_to_polar():
  map = Map()
  map.load('day10_map_3.txt')
  max_pos, max_vis = pick_best(map)
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (11, 13)

  last_theta = -0.0001
  for pos in [(11, 4), (14, 4), (15, 13),
              (15, 15), (14, 15), (11, 15)]:
    theta, dist = map.to_polar(max_pos, pos)
    assert theta > last_theta
    last_theta = theta
    if pos == (11, 4):
      assert theta == 0 and dist == 9

  pos = (10, 15)
  theta, dist = map.to_polar(max_pos, pos)
  if theta <= last_theta:
    print('%s -> %s = %f, %d' % (max_pos, pos, theta, dist))
  assert theta > last_theta
  last_theta = theta

  #while map.n_blasted < 20:
  #  map.blast(max_pos)


def test2():
  test_to_polar()
  map = Map()
  map.load_from_string(TEST_BLAST)
  max_pos, max_vis = pick_best(map)
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (8, 3)
  map.trace = True
  for i in range(10):
    map.blast(max_pos)

def test_gen_sweep():
  map = Map()
  map.load('input_10.txt')
  best = (17, 22)
  n_edge = 0
  for x, y in map.gen_sweep(best):
    n_edge += 1
  assert n_edge == 30 * 4


def part2():
  map = Map()
  map.load('input_10.txt')
  best = (17, 22)
  # map.trace = True
  while map.n_blasted < 200:
    map.blast(best, stop_at=200)
  # Expect: blast 200 (6, 16)


test1()
part1()

test2()
part2()
