#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import map


class Grid(object):

  def __init__(self):

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
  maze = map.Map()
  maze.load('input_18.txt')
  maze.print()
  print()
  print('After dead end removal')
  maze.close_dead_ends()
  maze.print()

  # print('part1:', alignment)
  # assert 3428 == alignment



if __name__ == '__main__':
  part1()
