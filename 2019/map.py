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

  def __init__(self, open=None, ignore=None, label_width=0):
    # core properties
    self.width = 0
    self.height = 0
    self.wall = '#'
    self.open = open or set(['.'])
    self.ignore = ignore or set()
    self.label_width = label_width
    self.filler = '_'
    # computed at load
    self.walls = set()
    self.points = {}
    self.edge_portals = {}
    self.interior_portals = {}
    self.portals = {}
    # transient
    self.trace = False

  def load(self, path):
    with open(path, 'r') as inp:
      self.load_from_string(inp.read())

  def is_wall(self, pos):
    return pos in self.walls

  def cell(self, pos):
    return self.points.get(pos)

  def for_each_cell(self, func):
    for x in range(self.width):
      for y in range(self.height):
        pos = (x, y)
        func(pos, self.cell(pos))

  def load_from_string(self, s):
    self.positions = []
    self.is_occupied = set()
    self.height = -self.label_width
    self.width = 0
    pre_lines = [None]
    last1 = None
    last2 = None
    last3 = None
    for line in s.split('\n'):
      if line == '':
        continue
      x = 0
      if self.height < 0:
        # pre_lines.append(line[self.label_width:-self.label_width])
        pre_lines.append(line)
        self.height += 1
        continue

      last1 = last2
      last2 = last3
      last3 = line
      if self.label_width > 0 and self.height >= self.label_width:
        self.extract_labels([last1, last2, last3], self.height)
      for c in line[self.label_width:-self.label_width]:
        if c == self.wall:
          self.walls.add((x, self.height))
          self.width = max(self.width, x+1)
        else:
          if c in self.ignore:
            pass
          else:
            self.points[(x, self.height)] = c
        x += 1
      self.height += 1

    # get the top and bottom labels
    if self.label_width:
      pre_lines[0] = ' ' * (self.width + self.label_width * 2)
      self.extract_labels(pre_lines, -1)
      self.extract_labels(
          [last2, last3, ' ' * (self.width + self.label_width * 2)],
          self.height-1)
      self.height -= self.label_width

    # fix the right edge portals
    for pos in list(self.portals):
      if pos[0] == -1:
        label = self.portals[pos]
        del self.portals[pos]
        pos = (self.width, pos[1])
        self.portals[pos] = label
        if label in self.edge_portals:
          self.edge_portals[label] = pos
        if label in self.interior_portals:
          self.interior_portals[label] = pos

    print(self.portals)


  def extract_labels(self, lines, y):
    # Note that y is the scan line, which is past height for bottom label
    # print(lines)
    for x in range(self.width):
      label = ''.join(lines[row][x] for row in range(self.label_width+1))
      # label = ''.join([c if c.isalpha() else ' ' for c in label])
      label = label.replace('#', ' ')
      if len(label.replace('.', '').strip()) > 1:
        # print(x, y, '|%s|' % label, label[:-self.label_width])
        if label[0] == ' ':
          self.portals[(x-self.label_width, y+1)] = label[1:].strip()
        elif label[self.label_width] == ' ':
          self.portals[(x-self.label_width, y-self.label_width)] = label[0:self.label_width].strip()
        else:
           # raise Exception('Bad label <%s> from lines: %s' % (label, lines))
           pass

    for x in range(self.width + self.label_width):
      label = lines[-1][x:x+self.label_width+1]
      if y == 8:
        print('XXXXX |%s|' % label)
      if label[0] in self.open and label[1].isalpha() and label[2].isalpha():
        # .AB 
        # print('   ==>', label[1:])
        self.portals[(x-self.label_width, y)] = label[1:]
      elif label[2] in self.open and label[0].isalpha() and label[1].isalpha():
        # AB. 
        self.portals[(x, y)] = label[0:self.label_width]


  def print(self):
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
        line[x] = self.wall if pos in self.walls else (
            self.points.get(pos) or self.filler)
      trailer = ''
      if self.label_width > 0:
        trailer = self.portals.get((self.width, y)) or ''
      print(annotation + ''.join(line) + trailer)
    if self.label_width > 0:
      line1, line2 = self._prep_labels(self.height-1)
      print('  ', ''.join(line1))
      print('  ', ''.join(line2))

  def _prep_labels(self, y):
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
        for neighbor in neighbors(pos):
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

  def get_moves(self, pos, visited):
    ret = []
    # print('getmoves, visited', visited.keys())
    for neighbor in neighbors(pos):
      n = self.points.get(neighbor)
      if (n
          and (neighbor not in self.walls)
          and (neighbor not in visited.keys())):
        ret.append(neighbor)
    return ret
