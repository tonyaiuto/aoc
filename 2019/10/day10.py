#!/usr/bin/env python3

class Map(object):

  def __init__(self):
    self.positions = []
    self.width = 0
    self.height = 0
    self.trace = False

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
    blocked.add(my_pos)
    for p in self.positions:
      if p in blocked:
        continue
      x = p[0]
      y = p[1]
      dx = x - my_pos[0]
      dy = y - my_pos[1]

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
        # if test_pos in self.is_occupied and test_pos != my_pos:
        if test_pos in self.positions and test_pos != my_pos:
          if self.trace:
            print(my_pos, 'to', p, 'blocks', test_pos)
          blocked.add(test_pos)
    return len(self.positions) - len(blocked)


def pick_best(path):
  map = Map()
  map.load(path)
  print(map.positions)
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
  max_pos, max_vis = pick_best('day10_map_1.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (3, 4)
  assert max_vis == 8

  max_pos, max_vis = pick_best('day10_map_2.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (6, 3)
  assert max_vis == 41

  max_pos, max_vis = pick_best('day10_map_2a.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (1, 2)
  assert max_vis == 35

  max_pos, max_vis = pick_best('day10_map_3.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_pos == (11, 13)
  # assert max_vis == 210


test1()

def part1():
  max_pos, max_vis = pick_best('input_10.txt')
  print('%s sees %d others' % (max_pos, max_vis))
  assert max_vis == 288
  assert max_vis < 300

def part2():
  pass

part1()
part2()
