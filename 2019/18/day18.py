#!/usr/bin/env python3

from collections import namedtuple
import sys
import textwrap

from elf_image import ElfImage
import map
from memoized import memoized


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
    self.start = start
    self.parent = parent

    self.dist = 0
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

  def __repr__(self):
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

  def drop_key(self, key_name):
    del self.keys[key_name]
    self.stuff = [keylock for keylock in self.stuff
                  if keylock.name != key_name]


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

  @memoized
  def route_to(self, path):
    # find paths I can reach going out
    return self.outward_route_to(path)

  def outward_route_to(self, path):
    if self == path:
      return [self]
    for fork in self.forks:
      r = fork.outward_route_to(path)
      if r:
        return [self] + r
    return None


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
    self.ploc()
    key_name = keyloc[0]
    to_path = keyloc[2]
    route = self.cur_path.route_to(to_path)
    if to_path in route:
      print('can move out to', to_path, route)
      self.traverse_to(to_path, key_name, route)
    self.ploc()

  def ploc(self):
    print('now at path', self.cur_path, 'dist', self.cur_dist,
          'holding', self.holding)

    
  def traverse_to(self, to_path, key_name, route):
    # move from current pos to the new place
    dist = 0
    while True:
      print('loop to, route', to_path, route)
      nxt = route[0]
      route = route[1:]
      if nxt == self.cur_path:
        continue
      if self.cur_path.parent == nxt:
        print("Up not implemented")
        break
      else:
        dist_to_path = nxt.base_dist - self.cur_dist
        dist += dist_to_path
        self.cur_path = nxt
        self.cur_dist = 0
      if to_path == self.cur_path:
        break
    # now we are at the right path, move to the key
    key_dist = to_path.keys[key_name]
    dist += key_dist
    self.cur_dist = key_dist
    self.pick_up(key_name)
    print('travese_to: moved', dist)
    return dist

  def pick_up(self, key_name):
    self.holding.add(key_name)
    self.cur_path.drop_key(key_name)


  def do_it(self, start_path):
    self.cur_loc = start_path
    self.holding = set()
    self.do_round()
    self.do_round()


  def do_round(self):
    best_action = self.find_best_action(self.cur_loc)
    print('best_action', best_action)
    self.move_to(best_action[2])


def test_part1():
  maze = map.Map()
      #0123456789 123456789 12
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
