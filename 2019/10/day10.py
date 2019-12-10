#!/usr/bin/env python3

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


  def blast(self, center):
    blasted = set()
    center_x = center[0]
    center_y = center[1]
    x = center_x
    y = center_y
    for edge_x, edge_y in self.gen_sweep(center):
      dx, dy = self.reduce(edge_x - center_x, edge_y - center_y)
      while True:
        x = x + dx
        y = y + dy
        if x < 0 or y < 0:
          break
        if x >= self.width or y >= self.height:
          break

        probe_pos = (x, y)
        if self.trace:
          print('probe:', probe_pos)
        if probe_pos in self.is_occupied and probe_pos != center:
          blasted.add(probe_pos)
          self.n_blasted += 1
          print('blast', self.n_blasted, probe_pos)
          break
    print("Blasted", len(blasted))
    self.is_occupied = self.is_occupied - blasted
    print("is_occ", len(self.is_occupied))


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

def test2():
  map = Map()
  map.load_from_string(TEST_BLAST)
  max_pos, max_vis = pick_best(map)
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (8, 3)
  map.trace = True
  for i in range(5):
    map.blast(max_pos)


def part2():
  map = Map()
  map.load('input_10.txt')
  best = (17, 22)
  n_edge = 0
  for x, y in map.gen_sweep(best):
    n_edge += 1
  assert n_edge == 30 * 4
  # map.trace = True
  while map.n_blasted < 200:
    map.blast(best)


test1()
part1()

test2()
# part2()
