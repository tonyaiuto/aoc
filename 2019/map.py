#!/usr/bin/env python3


def need_turn(from_pos, dir, to):
  dx = to[0] - from_pos[0]
  dy = to[1] - from_pos[1]
  if dy < 0:  # moving up
    new_dir = 0
  elif dy > 0:  # moving down
    new_dir = 2
  elif dx > 0:  # moving right
    new_dir = 1
  else:
    new_dir = 3
  if dx == 0 and dir in [1, 3]:
    # changing y but facing left or right
    if dy > 0:  # moving down
      if dir == 1:  # but facing right
        return 'R', new_dir
      else:
        return 'L', new_dir
    else:  # moving up
      if dir == 1:  # but facing right
        return 'L', new_dir
      else:
        return 'R', new_dir
  elif dy == 0 and dir in [0, 2]:
    if dx > 0:  # moving right
      if dir == 0:  # facing up
        return 'R', new_dir
      else:
        return 'L', new_dir
    else:  # moving left
      if dir == 0:  # facing up
        return 'L', new_dir
      else:
        return 'R', new_dir
  return None, new_dir

assert ('R', 1) == need_turn((0,6), 0, (1,6))
assert (None, 1) == need_turn((1,6), 1, (2,6))
assert (None, 3) == need_turn((4,6), 1, (3,6))

def X(pos):
  return pos[0]

def Y(pos):
  return pos[1]

def neighbors(pos):
  return [(pos[0], pos[1]-1), (pos[0], pos[1]+1),
          (pos[0]-1, pos[1]), (pos[0]+1, pos[1])]


class Map(object):

  def __init__(self):
    self.points = {}
    self.width = 0
    self.height = 0
    self.trace = False
    self.wall = '#'
    self.walls = set()

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
         if c == self.wall:
           self.walls.add((x, self.height))
         else:
           if c == '.':
             c = ' '
           self.points[(x, self.height)] = c
         x += 1
       if self.width == 0:
         self.width = x
       else:
         assert self.width == x
       self.height += 1

  def print(self):
    print('  ', ('0123456789' * (self.width // 10 + 1))[0:self.width])
    for y in range(self.height):
      line = [' '] * self.width
      for x in range(self.width):
        pos = (x, y)
        line[x] = self.wall if pos in self.walls else (
            self.points.get(pos) or '?')
      print('%2d' % y, ''.join(line))

  def close_dead_ends(self):
    # for _ in range(1):
    while True:
      new_walls = set()
      for pos, content in self.points.items():
        if content != ' ':
          continue
        n_walls = 0
        for neighbor in neighbors(pos):
          if neighbor in self.walls:
            n_walls += 1
            if neighbor in self.points and self.points[neighbor] != ' ':
              print("WTF", pos, neighbor, self.points[neighbor])
        if n_walls == 3:
          self.walls.add(pos)
          new_walls.add(pos)

      # print(new_walls)
      for pos in new_walls:
        del self.points[pos]
      if not new_walls:
        break
