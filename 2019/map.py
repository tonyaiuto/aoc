#!/usr/bin/env python3

import textwrap

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

  def __init__(self, open=None, ignore=None, label_width=0):
    # core properties
    self.width = 0
    self.height = 0
    self.wall = '#'
    self.open = open or set(['.'])
    self.ignore = ignore or set()
    self.label_width = label_width
    self.filler = ' '
    # computed at load
    self.walls = set()
    self.points = {}
    self.portals = {}
    # transient
    self.trace = False

  def clone(self):
    ret = Map()
    ret.width = self.width
    ret.height = self.height
    ret.wall = self.wall
    ret.open = set(self.open)
    ret.ignore = set(self.ignore)
    ret.label_width = self.label_width
    ret.filler = self.filler
    ret.walls = set(self.walls)
    ret.points = dict(self.points)
    ret.portals = dict(self.portals)
    return ret

  def load(self, path):
    with open(path, 'r') as inp:
      self.load_from_string(inp.read(), dedent=False)

  def is_wall(self, pos):
    return pos in self.walls

  def cell(self, pos):
    return self.points.get(pos)

  def for_each_cell(self, func):
    for x in range(self.width):
      for y in range(self.height):
        pos = (x, y)
        func(pos, self.cell(pos))

  def neighbors(self, pos):
    x = X(pos)
    y = Y(pos)
    if x > 0:
      yield (x-1, y)
    if x < self.width-1:
      yield (x+1, y)
    if y > 0:
      yield (x, y-1)
    if y < self.height-1:
      yield (x, y+1)

  def load_from_string(self, s, dedent=True):
    self.positions = []
    self.is_occupied = set()
    self.height = -self.label_width
    self.width = 0
    last1 = None
    last2 = None
    last3 = None
    if dedent:
      s = textwrap.dedent(s)
    for line in s.split('\n'):
      if line == '':
        continue

      # rolling buffer for vertical labels
      last1 = last2
      last2 = last3
      last3 = line
      if self.height < 0:
        self.height += 1
        continue

      x = 0
      end_of_line = -self.label_width if self.label_width > 0 else None
      for c in line[self.label_width:end_of_line]:
        if c == self.wall:
          self.walls.add((x, self.height))
          self.width = max(self.width, x+1)
        else:
          if c in self.ignore:
            pass
          else:
            self.points[(x, self.height)] = c
        x += 1

      if self.label_width > 0 and self.height >= 0:
        self.extract_labels([last1, last2, last3], self.height)
      self.height += 1

    if self.label_width:
      self.height -= self.label_width


  def extract_labels(self, lines, y):
    # x includes the margins
    # y is the scan line, which is past height for bottom label print(lines)
    for x in range(self.width):
      x_i = self.label_width + x
      label = ''.join(lines[row][x_i] for row in range(self.label_width+1))
      # label = ''.join([c if c.isalpha() else ' ' for c in label])
      label = label.replace('#', ' ')
      if len(label.replace('.', '').strip()) > 1:
        # print(x, y, '|%s|' % label, label[:-self.label_width])
        if label[0] == '.':
          self.portals[(x, y-self.label_width)] = label[1:]
        elif label[self.label_width] == '.':
          self.portals[(x, y)] = label[0:self.label_width]
        else:
           # raise Exception('Bad label <%s> from lines: %s' % (label, lines))
           pass

    for x in range(self.width + self.label_width):
      label = lines[-1][x:x+self.label_width+1]
      if label[0] == '.' and label[1].isalpha() and label[2].isalpha():
        # .AB 
        # print('   ==>', label[1:])
        self.portals[(x-self.label_width, y)] = label[1:]
      elif label[2] in self.open and label[0].isalpha() and label[1].isalpha():
        # AB. 
        self.portals[(x, y)] = label[0:self.label_width]


  def print(self, print_portals=True, overlay=None):
    if print_portals and self.portals:
      print('Portals:')
      line = ''
      for i, pos in enumerate(sorted(self.portals)):
         line += '    (%2d, %2d) => %s' % (pos[0], pos[1], self.portals[pos])
         if i % 4 == 3:
           print(line)
           line = ''
      if line:
        print(line)

    margin = '  ' + ' ' * self.label_width
    print(margin + ' ',
          ''.join(['        %2d' % d for d in range(1, self.width // 10 + 1)]))
    print(margin, ('0123456789' * (self.width // 10 + 1))[0:self.width])
    if self.label_width > 0:
      line1, line2 = self._prep_labels(0)
      print('  ', ''.join(line1))
      print('  ', ''.join(line2))

    for y in range(self.height):
      #if self.label_width > 0:
      #  line1, line2 = self._prep_labels(y)
      annotation = '%2d ' % y
      if self.label_width > 0:
        label = self.portals.get((0, y)) or ' '
        annotation += '%*s' % (self.label_width, label)
      line = [' '] * self.width
      for x in range(self.width):
        pos = (x, y)
        cell = self.wall if pos in self.walls else (
            self.points.get(pos) or self.filler)
        if pos in self.portals:
          cell = '*'
        if cell == self.filler:
          portal = self.portals.get((x-2, y))
          if portal:
            line[x-1] = portal[0]
            cell = portal[1]
          portal = self.portals.get((x+2, y))
          if portal:
            cell = portal[0]
          portal = self.portals.get((x+1, y))
          if portal:
            cell = portal[1]

          portal = self.portals.get((x, y-1))
          if portal:
            cell = portal[0]
          portal = self.portals.get((x, y-2))
          if portal:
            cell = portal[1]

          portal = self.portals.get((x, y+2))
          if portal:
            cell = portal[0]
          portal = self.portals.get((x, y+1))
          if portal:
            cell = portal[1]

        if overlay:
          o_val = overlay.get(pos)
          if o_val:
            cell = o_val
        line[x] = cell

      trailer = ''
      if self.label_width > 0:
        trailer = self.portals.get((self.width-1, y)) or ' ' * self.label_width
      print(annotation + ''.join(line) + trailer, '%2d' % y)
    if self.label_width > 0:
      line1, line2 = self._prep_labels(self.height-1)
      print('  ', ''.join(line1))
      print('  ', ''.join(line2))
    print(margin + ' ',
          ''.join(['        %2d' % d for d in range(1, self.width // 10 + 1)]))
    print(margin, ('0123456789' * (self.width // 10 + 1))[0:self.width])

  def _prep_labels(self, y):
    # Does vertical labels
    # y is top line of label
    line1 = [' '] * (self.width + self.label_width*2)
    line2 = [' '] * (self.width + self.label_width*2)
    for x in range(self.width):
      label = self.portals.get((x, y))
      if label:
        line1[x+self.label_width] = label[0]
        line2[x+self.label_width] = label[1]
    return line1, line2


  def close_dead_ends(self):
    # for _ in range(1):
    while True:
      new_walls = set()
      for pos, content in self.points.items():
        if content not in self.open:
          continue
        n_walls = 0
        for neighbor in self.neighbors(pos):
          if neighbor in self.walls:
            n_walls += 1
            if neighbor in self.points and self.points[neighbor] in self.open:
              if neighbor not in new_walls:
                print("WTF", pos, neighbor, self.points[neighbor])
        if n_walls == 3:
          self.walls.add(pos)
          new_walls.add(pos)

      # print(new_walls)
      for pos in new_walls:
        del self.points[pos]
      if not new_walls:
        break

  def get_moves(self, pos, visited, dist=-1):
    ret = []
    # print('getmoves, visited', visited.keys())
    for neighbor in self.neighbors(pos):
      n = self.points.get(neighbor)
      if n and (neighbor not in self.walls):
        if dist >= 0:
          n_dist = visited.get(neighbor, dist+1)
          if n_dist > dist:
            ret.append(neighbor)
        else:
          if neighbor not in visited:
            ret.append(neighbor)
    return ret
