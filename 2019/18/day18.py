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
     # distances to things
     self.locks = {}
     self.keys = {}
     self.forks = []
     # print('Create path: start', self.start, 'visited', self.visited)

   def __str__(self):
     return '<Path from %s>' % str(self.start)

   def print(self):
     print('Path from', self.start)
     print('  locks: ',
           ', '.join(['%c @ %d' % (k, v) for k, v in self.locks.items()]))
     print('  keys: ',
           ', '.join(['%c @ %d' % (k, v) for k, v in self.keys.items()]))
     print('  forks: ',
           ', '.join([str(f) for f in self.forks]))


class Vault(object):

  def __init__(self, maze):
    self.maze = maze
    self.set_start()

  def set_start(self):
    self.start = None
    for pos, c in self.maze.points.items():
      if c == '@':
        self.start = pos
        return

  def walk_path(self, path):
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
      for f in moves:
        child_path = Path(from_where=pos, start=f)
        child_path.visited[f] = 1
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

  # print('part1:', alignment)
  # assert 3428 == alignment



if __name__ == '__main__':
  test_part1()
