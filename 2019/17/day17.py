#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import intcode



def need_turn(from_pos, dir, to):
  dx = to[0] - from_pos[0]
  dy = to[1] - from_pos[1]
  if dx == 0 and dir in [1, 3]:
    # changing y but facing left or right
    if dy > 0:  # moving down
      if dir == 1:  # but facing right
        return 'R', 2
      else:
        return 'L', 2
    else:  # moving up
      if dir == 1:  # but facing right
        return 'L', 0
      else:
        return 'R', 0
  elif dy == 0 and dir in [0, 2]:
    if dx > 0:  # moving right
      if dir == 0:  # facing up
        return 'R', 1
      else:
        return 'L', 1
    else:  # moving left
      if dir == 0:  # facing up
        return 'L', 3
      else:
        return 'R', 3
  return None, None

assert ('R', 1) == need_turn((0,6), 0, (1,6))
assert (None, None) == need_turn((1,6), 1, (2,6))

def X(pos):
  return pos[0]

def Y(pos):
  return pos[1]

def neighbors(pos):
  return [(pos[0], pos[1]-1), (pos[0], pos[1]+1),
          (pos[0]-1, pos[1]), (pos[0]+1, pos[1])]


class VacuumRobot(object):

  def __init__(self, mem):

    self.computer = intcode.IntCode(list(mem))
    self.width = 0
    self.height = 0
    self.scaffold = set()
    self.points = {}
    self.intersections = {}
    self.visited = set()
    self.pos = None
    self.dir = 0

    """
    self.display = None
    self.frame = 0
    self.capture_frames = True
    """

  def get_map(self):
    x = 0
    self.height = 0
    # line = ''
    while True:
      out = self.computer.run_until_output()
      if self.computer.is_halted:
        break
      c = chr(out)
      if c == '\n':
        self.height += 1
        x = 0
        # print(line)
        # line = ''
        continue
      # line += c
      self.points[(x, self.height)] = c
      if c == '#':
        self.scaffold.add((x, self.height))
      if c == '^':
        self.start = (x, self.height)
        self.visited.add(self.start)
      x += 1
      self.width = max(self.width, x)


  def load_sample_map(self, map):
    self.height = 0
    for line in textwrap.dedent(map).split('\n'):
      if line.strip():
        x = 0
        for c in line:
          self.points[(x, self.height)] = c
          if c == '#':
            self.scaffold.add((x, self.height))
          if c == '^':
            self.start = (x, self.height)
            self.visited.add(self.start)
          x += 1
          self.width = max(self.width, x)
        self.height += 1

  def compute_alignment(self):
    alignment = 0
    for pos in self.scaffold:
      is_intersection = True
      for neighbor in neighbors(pos):
        if not neighbor in self.scaffold:
          is_intersection = False
      if is_intersection:
        self.intersections[pos] = 'O'
        a = X(pos) * Y(pos)
        print('%s => %d' % (pos, a))
        alignment += a
    return alignment

  def find_paths(self, pos):
    paths = []
    for i_pos in self.intersections:
      self.points[i_pos] = 'O'
    for path in self.find_path(pos):
      if len(path) < len(self.scaffold) + len(self.intersections):
        continue
      # print('Complete path: ', len(path), path)
      code = self.path_to_code(path)
      print(len(code), code)
      paths.append(code)
    return paths

  def path_to_code(self, path):
    from_pos = self.start
    dir = 0
    ret = []
    dist = 0
    for pos in path:
      turn, new_dir = need_turn(from_pos, dir, pos)
      from_pos = pos
      if turn:
        if dist:
          ret.append(dist+1)
        ret.append(turn)
        dir = new_dir
        dist = 0
      else:
        dist += 1
    ret.append(dist+1)
    return ret


  def find_path(self, pos, visited=None, level=1):
    if not visited:
      visited = set()
    # print('finding path from', pos)
    visited.add(pos)
    path = []
    while True:
      moves = self.get_moves(pos, visited)
      # print('at', pos, 'moves', moves)
      if not moves:
        # print('Done at: ', pos)
        if pos == self.end:
          yield path
        return
      if len(moves) == 1:
        pos = moves[0]
        path.append(pos)
        visited.add(pos)
      else:
        break
    # At an intersection
    print('level', level, 'path so far', path, 'moves:', moves)
    for move in moves:
      for rest in self.find_path(move, visited=set(visited), level=level+1):
        if rest:
          # print('follow', move, 'rest:', rest)
          yield path + [move] + rest


  def get_moves(self, pos, visited):
    ret = []
    for neighbor in neighbors(pos):
      n = self.points.get(neighbor)
      if n in ('#', 'O'):
        if n == '#' and neighbor in visited:
          continue
        ret.append(neighbor)
    return ret


  def try_paths(self, paths):
    paths = sorted(paths, key=lambda x: len(x))
    lpath = len(path)
    a_len = 2
    for a_len in range(4, lpath/2, 2):
      a = path[0:alen]
      for more_a in range(alen, lpath, 2):
        if a == path[more_a:more_a+a_len]:
          print('found %s again at %d' % (a, more_a))



def part1():
  mem = intcode.load_intcode('input_17.txt')
  robot = VacuumRobot(list(mem))
  robot.get_map()
  img = ElfImage.fromPoints(robot.points)
  img.print(ruler=True)
  print('')
  alignment = robot.compute_alignment()
  img.update(robot.intersections)
  img.print(ruler=True)
  print('part1:', alignment)
  assert 3428 == alignment


def test_part2():
  mem = intcode.load_intcode('input_17.txt')
  robot = VacuumRobot(list(mem))
  robot.computer.poke(0, 2)
  robot.load_sample_map("""
      #######...#####
      #.....#...#...#
      #.....#...#...#
      ......#...#...#
      ......#...###.#
      ......#.....#.#
      ^########...#.#
      ......#.#...#.#
      ......#########
      ........#...#..
      ....#########..
      ....#...#......
      ....#...#......
      ....#...#......
      ....#####......
      """)
  img = ElfImage.fromPoints(robot.points)
  img.print(ruler=True)
  print('')
  print('robot start=', robot.start)
  alignment = robot.compute_alignment()
  img.update(robot.intersections)
  img.print(ruler=True)
  robot.end = (0, 2)
  print('robot start=', robot.start)
  paths = robot.find_paths(robot.start)
  # robot.try_paths(paths)



def func_to_cmd(f):
  ret = []
  for c in f:
    if isinstance(c, str):
      ret.append(ord(c))
    else:
      if c > 10:
        ret.append(ord('1'))
      c = c % 10
      ret.append(ord(str(c)))
    ret.append(ord(','))
  return ret + [10]


def part2():
  mem = intcode.load_intcode('input_17.txt')
  robot = VacuumRobot(list(mem))
  robot.get_map()
  alignment = robot.compute_alignment()
  robot.end = (22, 14)
  paths = robot.find_paths(robot.start)
  print(paths)


def p2x():
  A = ['L', 4, 'L', 10, 'L',  6]
  B = ['L', 6, 'L',  4, 'R',  8, 'R', 8]
  C = ['L', 6, 'R',  8, 'L', 10, 'L', 8, 'L', 8]

  robot.computer.poke(0, 2)
  main = 'A,A,B,C,A,C,B,C,A,B,B'
  cmd = [ord(c) for c in main] + [10]
  print(cmd)
  robot.computer.push_input(cmd)
  cmd = func_to_cmd(A)
  print('A:', A)
  print(cmd)
  robot.computer.push_input(cmd)
  cmd = func_to_cmd(B)
  print('B:', B)
  print(cmd)
  robot.computer.push_input(cmd)
  cmd = func_to_cmd(C)
  print('C:', C)
  print(cmd)
  robot.computer.push_input(cmd)


"""
A   L, 4, L, 10, L, 6,
    L, 4, L, 10, L, 6,  

B   L, 6, L 4, R, 8, R, 8,
C   L, 6, R, 8, L, 10, L, 8, L 8, 

    L, 4, L, 10, L, 6, 

    L, 6, R, 8, L, 10, L, 8, L, 8,

    L, 6, L, 4, R, 8, R, 8,
    L, 6, R, 8, L, 10, L, 8, L, 8,

    l, 4, l, 10, l, 6,

    l 6, l4, r 6, r8
    l 6, l4, r 8, r8
"""


if __name__ == '__main__':
  part1()
  test_part2()
  part2()
