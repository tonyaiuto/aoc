#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import map


class Path(object):

  def __init__(self, from_where, start, base_dist=0):
    self.from_where = from_where
    self.base_dist = base_dist
    self.dist = 0
    self.start = start
    self.visited = {}
    self.visited[from_where] = 1
    self.visited[start] = 0

    # distances to things
    self.locks = {}
    self.keys = {}
    self.stuff = []
    self.forks = []
    # print('Create path: start', self.start, 'visited', self.visited)

  def __str__(self):
    return '<Path from %s>' % str(self.start)

  def print(self, indent=0, forks=True):
    sp = '   ' * indent
    print(sp, 'Path from', self.start, '@', self.base_dist, self.stuff)
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

  def reachable_targets(self, dist_down_path, holding):
    reachable = []
    for content, dist in self.stuff:
      if content.islower():
        reachable.append((content, dist_down_path + dist))
        print('key', content, 'at', dist)
        holding.add(content)
      elif content.isupper():
        reachable.append((content, dist_down_path + dist))
        print('lock', content, 'at', dist)
        if content.lower() not in holding:
          return reachable
      else:
        print('stuff', content, 'at', dist)
    for fork in self.forks:
      reachable.extend(fork.reachable_targets(
          fork.base_dist+dist_down_path, set(holding)))
    return reachable

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
        path.stuff.append((content, path.dist))
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
        child_path = Path(from_where=pos, start=path_start, base_dist=path.dist)
        # Do not duplicate paths
        child_path.visited.update(self.path_heads)
        path.forks.append(child_path)
        self.walk_path(child_path)
      break
    # path.print()

  def do_it(self, start_path):
    reachable = start_path.reachable_targets(0, set())
    print(reachable)
      

    """
  keys:  
   forks:  <Path from (5, 3)>, <Path from (7, 3)>
    Path from (5, 3) @ 1
      locks:  C @ 23, D @ 25
      keys:  b @ 21, f @ 27
    Path from (7, 3) @ 1
      locks:  B @ 3, A @ 9, F @ 13
      keys:  a @ 1, c @ 5, d @ 7, e @ 11, g @ 15
    """

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
  #print('After dead end removal')
  #maze.close_dead_ends()

  maze.print()
  vault = Vault(maze)
  path = Path(from_where=(-1, -1), start=vault.start)
  vault.walk_path(path)
  print('========================================')
  path.print_tree()
  vault.do_it(path)

def test_part1_b():
  maze = map.Map()
  maze.load_from_string("""\
      #################
      #i.G..c...e..H.p#
      ########.########
      #j.A..b...f..D.o#
      ########@########
      #k.E..a...g..B.n#
      ########.########
      #l.F..d...h..C.m#
      #################
      """)
  # Shortest paths are 136 steps;
  # one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m
  maze.print()
  vault = Vault(maze)
  path = Path(from_where=(-1, -1), start=vault.start)
  vault.walk_path(path)
  print('========================================')
  path.print_tree()
  vault.do_it(path)


"""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h
"""


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
  test_part1_b()
  # part1()
