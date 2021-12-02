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
    for pos in self.intersections:
      self.points[pos] = 'O'
    return alignment

  def find_paths(self, pos):
    paths = []
    for path in self.find_path(pos):
      if len(path) < len(self.scaffold) + len(self.intersections):
        continue
      # print('Complete path: ', len(path), path)
      code = self.path_to_code(path)
      print(len(code), code)
      paths.append(code)
    return paths


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
  path = robot.find_straighest_path(robot.start)
  print(robot.path_to_code(path))


def part2():
  mem = intcode.load_intcode('input_17.txt')

  robot = VacuumRobot(list(mem))
  robot.get_map()
  alignment = robot.compute_alignment()
  robot.end = (22, 14)
  # paths = robot.find_paths(robot.start)
  # print(paths)

  path = robot.find_straighest_path(robot.start)
  move_program = robot.path_to_code(path)
  print(move_program)

  SHOULD_BE = ['L', 4, 'L', 10, 'L', 6, 'L', 4, 'L', 10, 'L', 6, 'L', 6, 'L', 4, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8, 'L', 4, 'L', 10, 'L', 6, 'L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8, 'L', 6, 'L', 4, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8, 'L', 4, 'L', 10, 'L', 6, 'L', 6, 'L', 4, 'R', 8, 'R']

  # Found by hand
  A = ['L', 4, 'L', 10, 'L', 6]
  B = ['L', 6, 'L', 4, 'R', 8, 'R', 8]
  C = ['L', 6, 'R', 8, 'L', 10, 'L', 8, 'L', 8]
  main_program = A + A + B + C + A + C + B + C + A + B
  assert move_program == main_program

  main_code = intcode.code_to_ascii(
      ['A', 'A', 'B', 'C', 'A', 'C', 'B', 'C', 'A', 'B'])
  a_code = intcode.code_to_ascii(A)
  b_code = intcode.code_to_ascii(B)
  c_code = intcode.code_to_ascii(C)

  assert mem[0] == 1
  robot = VacuumRobot(list(mem))
  robot.computer.poke(0, 2)

  robot.computer.push_input(main_code)
  robot.computer.push_input(a_code)
  robot.computer.push_input(b_code)
  robot.computer.push_input(c_code)
  robot.computer.push_input([ord('n'), 10])

  print("Mode 2 run")
  out = robot.computer.run()
  print(out)
  print(''.join([chr(c) for c in out if c <= 255]))
  for c in out:
    if c > 255:
      print('Answer:', c)
      assert 779133 == c

  """
  # trying to get it to print
  print("Get prompts")
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())
  print(robot.computer.run_until_newline())

  print("Free run")
  out = robot.computer.run()
  print(out)
  print(''.join([chr(c) for c in out]))
  """

if __name__ == '__main__':
  part1()
  test_part2()
  part2()
