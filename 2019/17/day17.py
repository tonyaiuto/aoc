#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import intcode



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
    for pos in self.intersections:
      self.points[pos] = 'O'
    return alignment

  def find_paths(self, pos):
    for path in self.find_path(pos):
      if len(path) < len(self.scaffold) + len(self.intersections):
        continue
      print('Complete path: ', len(path), path)
      print(self.path_to_code(path))
    print('# scaffold', len(self.scaffold))


  def find_straighest_path(self, pos):
    print('finding straighest path from', pos)
    visited = set()
    visited.add(pos)
    path = []
    dir = 0
    while True:
      moves = self.get_moves(pos, visited)
      if not moves:
        # print('Done at: ', pos)
        if pos == self.end:
          break
        raise Exception('got to wrong end at', pos)

      if len(moves) == 1:
        move = moves[0]
        _, new_dir = need_turn(pos, dir, move)
        if new_dir is not None:
          # print('turning to', new_dir)
          dir = new_dir
      else:
        move = None
        # print('at', pos, 'dir:', dir, 'moves', moves)
        for m in moves:
          _, new_dir = need_turn(pos, dir, m)
          # print('    ', m, '=> dir', new_dir)
          if new_dir == dir:
            move = m
        assert move
      pos = move
      path.append(pos)
      visited.add(pos)

    # print('Complete straight path: ', len(path), path)
    # print(self.path_to_code(path))
    return path


  def path_to_code(self, path):
    #  80 [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (8, 7), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8), (14, 7), (14, 6), (14, 5), (14, 4), (14, 3), (14, 2), (14, 1), (14, 0), (13, 0), (12, 0), (11, 0), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (11, 4), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (11, 10), (10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (7, 8), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2)]
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
    # print('level', level, 'path so far', path, 'moves:', moves)
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
  # robot.find_paths(robot.start)
  path = robot.find_straighest_path(robot.start)
  print(robot.path_to_code(path))


def code_to_ascii(code):
  ret = []
  for word in code:
    if ret:
      ret.append(ord(','))
    if isinstance(word, str):
      ret.append(ord(word))
    else:
      if word > 10:
        ret.append(ord('1'))
      ret.append(ord(str(word % 10)))
  assert len(ret) <= 20
  ret.append(10)
  print(ret)
  return ret


def part2():
  mem = intcode.load_intcode('input_17.txt')
  robot = VacuumRobot(list(mem))
  robot.get_map()
  alignment = robot.compute_alignment()
  robot.end = (22, 14)
  path = robot.find_straighest_path(robot.start)
  move_program = robot.path_to_code(path)
  print(move_program)

  X = ['L', 4, 'L', 10, 'L', 6, 'L', 4, 'L', 10, 'L', 6, 'L', 6, 'L', 4, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8, 'L', 4, 'L', 10, 'L', 6, 'L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8, 'L', 6, 'L', 4, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8, 'L', 4, 'L', 10, 'L', 6, 'L', 6, 'L', 4, 'R', 8, 'R']

  A = ['L', 4, 'L', 10, 'L', 6]
  B = ['L', 6, 'L', 4, 'R', 8, 'R', 8]
  C = ['L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8]
  main_program = A + A + B + C + A + C + B + C + A + B
  assert move_program == main_program

  main_code = code_to_ascii(['A', 'A', 'B', 'C', 'A', 'C', 'B', 'C', 'A', 'B'])
  a_code = code_to_ascii(A)
  b_code = code_to_ascii(B)
  c_code = code_to_ascii(C)


  assert mem[0] == 1
  robot = VacuumRobot(list(mem))
  robot.computer.run()
  robot.computer.poke(0, 2)

  robot.computer.push_input(main_code)
  robot.computer.push_input(a_code)
  robot.computer.push_input(b_code)
  robot.computer.push_input(c_code)
  robot.computer.push_input([ord('n'), 10])

  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())

  out = robot.computer.run()
  print(out)
  print(''.join([chr(c) for c in out]))


if __name__ == '__main__':
  part1()
  test_part2()
  part2()

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
