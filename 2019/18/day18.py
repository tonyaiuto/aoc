#!/usr/bin/env python3

from collections import namedtuple
import sys
import textwrap

from elf_image import ElfImage
import map
from memoized import memoized


def P(key_set):
  return ','.join(sorted(key.name for key in key_set))


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


class Key(object):

  def __init__(self, name, path, dist_from_root, blocked_by=None,
               upstream_keys=None):
    self.name = name
    self.path = path
    self.dist_from_root = dist_from_root
    self.blocked_by = blocked_by
    self.upstream_keys = upstream_keys
    self.blocks = []
    self.dists = {}

  def __str__(self):
    return 'Key<%s, %d>' % (self.name, self.dist_from_root)

  def __repr__(self):
    return 'Key<%s, %d>' % (self.name, self.dist_from_root)

  def print(self):
    print('Key:%s, dist:%d, upstream:%s' % (
        self.name, self.dist_from_root, P(self.upstream_keys)))

  def path_from_root(self):
    ret = []
    path = self.path
    while path:
      ret.append(path)
      path = path.parent
    ret.reverse()
    return ret

  def is_reachable(self, holding, reachable):
    for key in self.upstream_keys:
      if key in holding:
        continue
      if key.name.islower() and key in reachable:
        continue
      return False
    return True


class Path(object):

  trace_level = 1

  def __init__(self, from_where, start, parent=None, base_dist=0):
    self.from_where = from_where
    self.base_dist = base_dist
    self.start = start
    self.parent = parent

    self.dist = 0
    self.visited = {}
    self.visited[from_where] = 1
    self.visited[start] = 0
    self.trace = True

    # distances to things
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
    print(sp, '  keys: ',
          ', '.join(['%c @ %d' % (k, v) for k, v in self.keys.items()]))
    if self.forks:
      print(sp, '  forks: ', ', '.join([str(f) for f in self.forks]))

  def print_tree(self, level=0):
    self.print(indent=level, forks=False)
    for fork in self.forks:
      fork.print_tree(level=level+1)

  def _reachable_downstream(
     self, reachable, holding, cur_at=0, total_dist=0, exclude=None):
    assert cur_at * total_dist == 0
    for keylock in self.stuff:
      if keylock.name.isalpha():
        if keylock.dist > cur_at:
          reachable[keylock.name] = KeyLock(
              keylock.name, total_dist + keylock.dist - cur_at,
              keylock.path)
        else:
          # back the path
          reachable[keylock.name] = KeyLock(
              keylock.name, total_dist + cur_at - keylock.dist,
              keylock.path)

        if keylock.name.islower():
          if Path.trace_level > 1:
            print('key', keylock.name, 'at', keylock.dist)
          holding.add(keylock.name)
        else:
          if Path.trace_level > 1:
            print('lock', keylock.name, 'at', keylock.dist)
          if keylock.name.lower() not in holding:
            return reachable
      else:
        print('stuff', keylock.name, 'at', keylock.dist)

    for fork in self.forks:
      if fork == exclude:
        continue
      fork._reachable_downstream(
          reachable=reachable,
          holding=holding,
          total_dist=fork.base_dist + total_dist - cur_at)


  @memoized
  def route_to(self, path):
    # find paths I can reach going out
    out = self.outward_route_to(path)
    if out:
      return out
    up = [self.parent]
    while True:
      up.append(self.parent)
      out = up[-1].route_to(path)
      if out:
        return up + out

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
    self.path_heads = {}
    self.cur_dist = 0
    self.trace = True
    self.total_moved = 0
    self.all_keys = {}
    self.blocked_by = {}
    self.init()

  def init(self):
    self.set_start()
    self.top = Path(from_where=(-1, -1), start=self.start)
    self.cur_path = self.top
    self.maze.close_dead_ends()
    self.walk_path(self.top)
    self.resolve_edges()
    self.compute_distances()
    self.best_dist = self.worst_path
    print('upper bound for distance', self.best_dist)

  def set_start(self):
    self.start = None
    for pos, c in self.maze.points.items():
      if c == '@':
        self.start = pos
        return

  def add_key(self, keylock):
    self.all_keys[keylock.name] = keylock

  def resolve_edges(self):
    for key, blocker_name in self.blocked_by.items():
      blocker = self.all_keys[blocker_name]
      blocker.blocks.append(key)

  def compute_distances(self):
    self.worst_path = 0
    for name, key in self.all_keys.items():
      if name.isupper():
        continue
      rp = key.path_from_root()
      for other_name, other_key in self.all_keys.items():
        if other_name == name or other_name.isupper():
          continue
        if key.dists.get(other_name):
          continue
        if key.path == other_key.path:
          dist = abs(key.dist_from_root - other_key.dist_from_root)
        else:
          rp2 = other_key.path_from_root()
          for i in range(len(rp)):
            if rp[i] != rp2[i]:
              # path i-1 is common ancestor
              common_ancestor = rp[i-1]
              dist = ((key.dist_from_root - common_ancestor.base_dist)
                      + (other_key.dist_from_root - common_ancestor.base_dist))
              break

        print('dist %s %s = %d' % (name, other_name, dist))
        key.dists[other_name] = dist
        other_key.dists[name] = dist
        self.worst_path += dist

  def walk_path(self, path, dist_from_root=0, last_key=None):
    # trace out the tree
    self.path_heads[path.start] = -1
    pos = path.start
    up_keys = []
    while True:
      path.visited[pos] = path.dist
      content = self.maze.cell(pos)
      if content.isalpha():
        key = Key(content, path, dist_from_root + path.dist,
                  blocked_by=last_key, upstream_keys=set(up_keys))
        self.add_key(key)
        up_keys.append(key)
        if last_key:
          self.blocked_by[key] = last_key.name
        last_key = key

        path.stuff.append(KeyLock(content, path.dist, path))
        if content.islower():
          path.keys[content] = path.dist
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
        self.walk_path(child_path, dist_from_root=dist_from_root + path.dist,
                       last_key=last_key)
      break
    # path.print()

  def all_solutions(self):
    blocked = set(self.blocked_by.keys())
    # find unblocked
    keys = set(k for k in self.all_keys.values())
    unblocked = keys - blocked
    print('=keys', keys)
    print('=blocked', blocked)
    print('=unblocked', unblocked)

    # make sure the things behind the reachable keys are also reachable
    holding = set()
    reachable = set(unblocked)
    for key in unblocked:
      self.unblock_reachable_downstream(key, holding, reachable)
    # now try them all
    for start in unblocked:
      total_dist = start.dist_from_root
      self.try_paths(start, set(), set(reachable), total_dist, indent=0)
    print('best traversal distance', self.best_dist)


  def unblock_reachable_downstream(self, key, holding, reachable, indent=0):
    sp = ' ' * indent
    print(sp, 'adding downstream reachabilty for', key, 'blocks', key.blocks)
    for downstream in key.blocks:
      reachable.add(downstream)
      # YYY if downstream.name.islower():
      if downstream.name.islower() or downstream.name.lower() in holding:
        self.unblock_reachable_downstream(downstream, holding, reachable)

  def use_key(self, at_key, holding, reachable, indent=0):
    sp = ' ' * indent
    door = self.all_keys.get(at_key.name.upper())
    if not door:
      return
    holding.add(door)
    print(sp, 'use_key', at_key, 'holding', P(holding),
          'reachable', P(reachable))
    if door.is_reachable(holding, reachable):
      reachable.add(door)
      self.unblock_reachable_downstream(door, holding, reachable, indent)
    else:
      print(sp, 'can not ulock', door)
    print(sp, 'done: holding', P(holding), 'now reachable', P(reachable))


  def try_paths(self, at_key, holding, reachable, total_dist, indent):
    # holding is the keys we have picked up
    # reachable is what we can reach (which may include what we picked up
    if at_key in holding:
      return 0
    sp = '  ' * indent
    print(sp, 'visiting ', at_key, 'dist', total_dist)
    if total_dist > self.best_dist:
      print(sp, 'gone too far')
      return -1
    holding.add(at_key)
    # If we are at a key, then we must have picked up all the upstream things
    for key in at_key.upstream_keys:
      holding.add(key)
      self.use_key(key, holding, reachable, indent=indent+1)
      #XX d = self.all_keys.get(key.name.upper())
      #XX if d:
      #XX   holding.add(d)

    if at_key.name == 'f':
      print(sp, '=F holding', P(holding), 'now reachable', P(reachable))
    self.use_key(at_key, holding, reachable, indent=indent+1)

    if len(holding) == len(self.all_keys):
      print(sp, 'complete set: dist', total_dist)
      self.best_dist = min(self.best_dist, total_dist)
      return 1

    print(sp, 'holding', P(holding), 'now reachable', P(reachable))

    # visit each that are now reachable
    for to_unblock in (reachable-holding):
      if at_key == to_unblock:
        continue
      if to_unblock.name.islower() and to_unblock not in holding:
        status = self.try_paths(
            to_unblock, set(holding), set(reachable),
            total_dist = total_dist + at_key.dists[to_unblock.name],
            indent = indent + 1)
        if status < 0:
          return 0
        #if status > 0:
        #  return 1
    return 0


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

  maze.print()
  vault = Vault(maze)
  print('========================================')
  print(vault.all_keys)
  print(vault.blocked_by)
  print('========================================')
  vault.top.print_tree()
  # vault.do_it(vault.top)
  vault.all_solutions()


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
  print('========================================')
  print(vault.blocked_by)
  print('========================================')
  vault.top.print_tree()
  # vault.do_it(vault.top)
  vault.all_solutions()


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
  print('========================================')

  vault = Vault(maze)
  vault.top.print_tree()
  vault.do_it(vault.top)

  print('========================================')
  path.print_tree()

  # print('part1:', alignment)
  # assert 3428 == alignment


if __name__ == '__main__':
  test_part1()
  test_part1_b()
  # part1()
