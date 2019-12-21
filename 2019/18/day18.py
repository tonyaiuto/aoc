#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import map


class Path(object):

  def __init__(self, from_where, start):
    self.from_where = from_where
    self.dist = 0
    self.start = start
    self.visited = {}
    self.visited[from_where] = 1
    self.visited[start] = 0

    # distances to things
    self.locks = {}
    self.keys = {}
    self.forks = []
    # print('Create path: start', self.start, 'visited', self.visited)

  def __str__(self):
    return '<Path from %s>' % str(self.start)

  def print(self, indent=0, forks=True):
    sp = '   ' * indent
    print(sp, 'Path from', self.start)
    print(sp, '  locks: ',
          ', '.join(['%c @ %d' % (k, v) for k, v in self.locks.items()]))
    print(sp, '  keys: ',
          ', '.join(['%c @ %d' % (k, v) for k, v in self.keys.items()]))
    if self.forks:
      print(sp, '  forks: ', ', '.join([str(f) for f in self.forks]))

  def print_tree(self, level=0):
    self.print(indent=level, forks=False)
    for fork in self.forks:
      fork.print_tree(level=level+1)


class Vault(object):

  def __init__(self, maze):
    self.maze = maze
    self.set_start()
    self.path_heads = {}

  def set_start(self):
    self.start = None
    for pos, c in self.maze.points.items():
      if c == '@':
        self.start = pos
        return

  def walk_path(self, path):
    self.path_heads[path.start] = -1
    pos = path.start
    while True:
      path.visited[pos] = path.dist
      content = self.maze.cell(pos)
      if content.isalpha():
        if content.islower():
          path.keys[content] = path.dist
        else:
          path.locks[content] = path.dist

      # now move on
      moves = self.maze.get_moves(pos, path.visited)
      # print('at', pos, 'moves', moves)
      if not moves:
        break
      path.dist += 1
      if len(moves) == 1:
        pos = moves[0]
        continue
      # a fork!!
      for path_start in moves:
        path.visited[path_start] = path.dist 

      for path_start in moves:
        child_path = Path(from_where=pos, start=path_start)
        # Do not duplicate paths
        child_path.visited.update(self.path_heads)
        path.forks.append(child_path)
        self.walk_path(child_path)
      break
    path.print()



def test_part1():
  maze = map.Map()
  maze.load_from_string("""\
      ########################
      #...............b.C.D.f#
      #.######################
      #.....@.a.B.c.d.A.e.F.g#
      ########################
      """)
  # Shortest path is 132 steps: b, a, c, d, f, e, g
  maze.print()
  vault = Vault(maze)
  path = Path(from_where=(-1, -1), start=vault.start)
  vault.walk_path(path)


def part1():
  maze = map.Map()
  maze.load('input_18.txt')
  maze.print()
  print()
  print('After dead end removal')
  maze.close_dead_ends()
  maze.print()

  vault = Vault(maze)
  path = Path(from_where=(-1, -1), start=vault.start)
  vault.walk_path(path)

  print('========================================')
  path.print_tree()

  # print('part1:', alignment)
  # assert 3428 == alignment


if __name__ == '__main__':
  test_part1()
  part1()
