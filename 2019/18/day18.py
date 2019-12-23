#!/usr/bin/env python3

from collections import namedtuple
import sys
import textwrap

from elf_image import ElfImage
import map


KeyLock = namedtuple('KeyLock', 'name dist path')

def _keylock__str__(self):
  return '(%s, %d)' % (self.name, self.dist)
  #return '(%s, %d, path@%d,%d)' % (self.name, self.dist,
  #    self.path.start[0], self.path.start[1])

def _keylock__repr__(self):
  return '(%s, %d, path@%d,%d)' % (self.name, self.dist,
      self.path.start[0], self.path.start[1])

KeyLock.__str__ = _keylock__str__
KeyLock.__repr__ = _keylock__repr__


class Path(object):

  def __init__(self, from_where, start, parent=None, base_dist=0):
    self.from_where = from_where
    self.base_dist = base_dist
    self.dist = 0
    self.start = start
    self.parent = parent

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
    print(sp, 'Path from', self.start, '@', self.base_dist,
        ', '.join(['(%s,%d)' % (k.name, k.dist) for k in self.stuff]))
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
    reachable = {}
    for keylock in self.stuff:
      if keylock.name.isalpha():
        reachable[keylock.name] = KeyLock(
            keylock.name, dist_down_path + keylock.dist, keylock.path)
        if keylock.name.islower():
          print('key', keylock.name, 'at', keylock.dist)
          holding.add(keylock.name)
        else:
          print('lock', keylock.name, 'at', keylock.dist)
          if keylock.name.lower() not in holding:
            return reachable
      else:
        print('stuff', keylock.name, 'at', keylock.dist)
    for fork in self.forks:
      reachable.update(fork.reachable_targets(
          fork.base_dist+dist_down_path, set(holding)))
    return reachable


class Vault(object):

  def __init__(self, maze):
    self.maze = maze
    self.set_start()
    self.path_heads = {}
    self.top = Path(from_where=(-1, -1), start=self.start)
    self.cur_path = self.top
    self.cur_dist = 0


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
        path.stuff.append(KeyLock(content, path.dist, path))
        if content.islower():
          path.keys[content] = path.dist
        else:
          path.locks[content] = path.dist
        print(path.stuff)

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
      for path_start in moves:  # prevent other forks from backtracking
        path.visited[path_start] = path.dist
      for path_start in moves:
        child_path = Path(parent=path, from_where=pos, start=path_start,
                          base_dist=path.dist)
        # Do not duplicate paths
        child_path.visited.update(self.path_heads)
        path.forks.append(child_path)
        self.walk_path(child_path)
      break
    # path.print()

  def find_best_action(self, start_path):
    reachable = start_path.reachable_targets(0, set())
    print(reachable)
    best_door = None
    for content, thing in reachable.items():
      dist = thing[1]
      if content.isupper():
        key = reachable.get(content.lower())
        if key:
          if best_door == None or dist < best_door[1]:
            best_door = (content, dist, key)
    return best_door

  def move_to(self, keyloc):
    key_name = keyloc[0]
    dist = keyloc[1]
    path = keyloc[2]


  def do_it(self, start_path):
    best_action = self.find_best_action(start_path)
    print('best_action', best_action)
    self.move_to(best_action[2])


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
  vault.walk_path(vault.top)
  print('========================================')
  vault.top.print_tree()
  vault.do_it(vault.top)


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
  # test_part1_b()
  # part1()
