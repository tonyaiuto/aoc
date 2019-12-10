#!/usr/bin/env python3

def delta(p1, p2):
  return p2[0] - p1[0], p2[1] - p1[1]


class Map(object):

  def __init__(self):
    self.positions = []
    self.width = 0
    self.height = 0

  def load(self, path):
    self.positions = []
    self.is_occupied = set()
    self.height = 0
    self.width = 0
    with open(path, 'r') as inp:
      for line in inp:
         x = 0
         for c in line.strip():
           if c == '#':
             self.positions.append((x, self.height))
             self.is_occupied.add((x, self.height))
           x += 1
         if self.width == 0:
           self.width = x
         else:
           assert self.width == x
         self.height += 1

  def check_vis(self, my_pos):
    blocked = set()
    for p in self.positions:
      if p == my_pos:
        continue
      if p in blocked:
        continue
      x = p[0]
      y = p[1]
      dx = x - my_pos[0]
      dy = y - my_pos[1]
      # print('dx, dy=', dx, dy)
      while dx % 2 == 0 and dy % 2 == 0:
        dx = dx // 2
        dy = dy // 2
        # print('REDUCE dx, dy=', dx, dy)
      while True:
        x = x + dx
        y = y + dy
        if x < 0 or y < 0:
          break
        if x >= self.width or y >= self.height:
          break
        if (x, y) in self.is_occupied:
          print(my_pos, 'to', p, 'blocks', (x, y))
          blocked.add((x, y))
    return len(self.positions) - 1 - len(blocked)


def pick_best(path):
  map = Map()
  map.load(path)
  print(map.positions)
  max_vis = 0
  max_pos = None
  for pos in map.positions:
    n_vis = map.check_vis(pos)
    if max_vis < n_vis:
      max_vis = n_vis
      max_pos = pos
  return max_pos, max_vis


def test1():
  max_pos, max_vis = pick_best('day10_map_1.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (3, 4)
  assert max_vis == 8

  max_pos, max_vis = pick_best('day10_map_2.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (6, 3)
  assert max_vis == 41

  max_pos, max_vis = pick_best('day10_map_3.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (11, 13)
  assert max_vis == 210


test1()
