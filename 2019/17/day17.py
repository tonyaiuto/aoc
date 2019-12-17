#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import intcode


def move_pos(pos, dir):
  if dir == 1:
    return (pos[0], pos[1]-1)
  elif dir == 2:
    return (pos[0], pos[1]+1)
  elif dir == 3:
    return (pos[0]-1, pos[1])
  elif dir == 4:
    return (pos[0]+1, pos[1])
  else:
    raise Exception('invalid direction: %d' % dir)


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
    self.droid_pos = (0,0)
    self.no_go = set()
    self.oxygen = None
    self.last_dir = 0
    self.span = 0
    self.dist_to_here = {}
    self.min_x = 0
    self.max_x = 0
    self.min_y = 0
    self.max_y = 0

    self.display = None
    self.frame = 0
    self.capture_frames = True
    self.visited.add((0,0))
    self.dist_to_here[(0,0)] = 0
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
    for pos in self.intersections:
      self.points[pos] = 'O'
    for path in self.find_path(pos):
      if len(path) < len(self.scaffold):
        continue
      print('Complete path: ', len(path), path)
    print('# scaffold', len(self.scaffold))

  def path_to_code(self, path):
    pass
    

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
          print('follow', move, 'rest:', rest)
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
  alignment = robot.compute_alignment()
  img.update(robot.intersections)
  img.print(ruler=True)
  robot.end = (0, 2)
  robot.find_paths(robot.start)




def part2():
  mem = intcode.load_intcode('input_17.txt')
  robot = VacuumRobot(list(mem))
  robot.computer.poke(0, 2)
  robot.get_map()
  robot.end = (22, 14)

if __name__ == '__main__':
  part1()
  test_part2()
  # part2()

"""
   0123456789012345678901234567890123456
 0 ..........................#######....
 1 ..........................#.....#....
 2 ..........................#.####O####
 3 ..........................#.#...#...#
 4 ..........................#.#...#...#
 5 ..........................#.#...#...#
 6 ..........................##O##.#...#
 7 ............................#.#.#...#
 8 ............................#.#.#...#
 9 ............................#.#.#...#
10 ............................##O##...#
11 ..............................#.....#
12 ............................##O######
13 ............................#.#......
14 ......................######O##......
15 ............................#........
16 ............................#........
17 ............................#........
18 ....####^...........#########........
19 ....#...............#................
20 ....#...............#................
21 ....#...............#................
22 ....#...............#................
23 ....#...............#................
24 ####O######.....####O######..........
25 #...#.....#.....#...#.....#..........
26 #...#.####O####.#...#####.#..........
27 #...#.#...#...#.#.......#.#..........
28 #...##O####...#.#.......#.#..........
29 #.....#.......#.#.......#.#..........
30 #######.......#.#.......#.#..........
31 ..............#.#.......#.#..........
32 ..............#.#########.#######....
33 ..............#.................#....
34 ..............#######.#########.#....
35 ....................#.#.......#.#....
36 ....................#.#.......#.#....
37 ....................#.#.......#.#....
38 ....................#.########O##....
39 ....................#.........#......
40 ....................#.........#......
41 ....................#.........#......
42 ....................###########......
"""
