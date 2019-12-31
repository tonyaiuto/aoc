#!/usr/bin/env python3

from collections import namedtuple
import sys
import textwrap

from elf_image import ElfImage
import map
from memoized import memoized


TRACE_DIST = False


def P(key_set):
  return ','.join(sorted(key.name for key in key_set))


class Key(object):

  def __init__(self, name, path, dist_from_root, dist_down_path=None,
               blocked_by=None, upstream_keys=None):
    self.name = name
    self.path = path
    self.dist_from_root = dist_from_root
    self.dist_down_path = dist_down_path
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

  def __init__(self, from_where, start, parent=None, base_dist=0,
               dist_from_root=0):
    self.from_where = from_where
    self.base_dist = base_dist
    self.dist_from_root = dist_from_root
    self.start = start
    self.parent = parent

    self.dist = 0
    self.visited = {}
    self.visited[from_where] = 1
    self.visited[start] = 0
    self.trace = True

    # distances to things
    self.keys = []
    self.forks = []
    # print('Create path: start', self.start, 'visited', self.visited)

  def __str__(self):
    return '<Path from %s>' % str(self.start)

  def __repr__(self):
    return '<Path from %s>' % str(self.start)

  def print(self, indent=0, forks=True):
    sp = '   ' * indent
    print(sp, 'Path from', self.start, '@', self.dist_from_root,
        ', '.join(['(%s,%d)' % (k.name, k.dist_from_root) for k in self.keys]))
    if self.forks:
      print(sp, '  forks: ', ', '.join([str(f) for f in self.forks]))

  def print_tree(self, level=0):
    self.print(indent=level, forks=False)
    for fork in self.forks:
      fork.print_tree(level=level+1)

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

  def get_key(self, keyname):
    return self.all_keys.get(keyname)

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
          dist_to_forks = 0
          for i in range(len(rp)):
            if rp[i] != rp2[i]:
              # path i-1 is common ancestor
              fork_dist = rp[i].dist_from_root - 1
              break
          # compute distance from juncture
          dist = ((key.dist_from_root - fork_dist)
                  + (other_key.dist_from_root - fork_dist))
        if TRACE_DIST:
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
                  blocked_by=last_key, dist_down_path=path.dist,
                  upstream_keys=set(up_keys))
        self.add_key(key)
        up_keys.append(key)
        path.keys.append(key)
        if last_key:
          self.blocked_by[key] = last_key.name
        last_key = key

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
                          base_dist=path.dist,
                          dist_from_root=dist_from_root + path.dist)
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
      if downstream.name.islower() or downstream.name.lower() in holding:
        self.unblock_reachable_downstream(
            downstream, holding, reachable, indent)

  def use_key(self, at_key, holding, reachable, indent=0):
    # make the keys downstream of the door for this key reachable
    sp = ' ' * indent
    door = self.all_keys.get(at_key.name.upper())
    if not door:
      return
    holding.add(door)
    print(sp, 'use_key', at_key, 'holding', P(holding),
          'reachable', P(reachable))
    if door.is_reachable(holding, reachable):
      reachable.add(door)
      self.unblock_reachable_downstream(door, holding, reachable, indent+1)
    else:
      print(sp+' ', 'can not ulock', door)
    print(sp+' ', 'done: holding', P(holding), 'now reachable', P(reachable))


  def try_paths(self, at_key, holding, reachable, total_dist, indent):
    # holding is the keys we have picked up
    # reachable is what we can reach (which may include what we picked up
    if at_key in holding:
      return 0
    sp = ' ' * indent
    print(sp, 'visiting ', at_key, 'dist', total_dist)
    if total_dist > self.best_dist:
      print(sp, 'gone too far')
      return -1
    holding.add(at_key)
    # If we are at a key, then we must have picked up all the upstream things
    for key in at_key.upstream_keys:
      holding.add(key)
      self.use_key(key, holding, reachable, indent=indent)
      #XX d = self.all_keys.get(key.name.upper())
      #XX if d:
      #XX   holding.add(d)
    self.use_key(at_key, holding, reachable, indent=indent)

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


def dist_check(vault, k1, k2, expect):
  key1 = vault.get_key(k1)
  dist = key1.dists[k2]
  if expect != dist:
    print('Distance from %s to %s. Expect %d got %d' % (k1, k2, expect, dist))
  assert expect == dist


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
  dist_check(vault, 'a', 'f', 30)
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
  assert 136 == vault.best_dist


def test_part1_c():
  maze = map.Map()
  maze.load_from_string("""\
      ########################
      #@..............ac.GI.b#
      ###d#e#f################
      ###A#B#C################
      ###g#h#i################
      ########################
      """)
  # Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h
  maze.print()
  vault = Vault(maze)
  vault.top.print_tree()

  dist_check(vault, 'd', 'g', 2)
  dist_check(vault, 'd', 'e', 4)
  dist_check(vault, 'd', 'h', 6)
  print('========================================')
  print(vault.blocked_by)
  print('========================================')
  vault.all_solutions()
  assert 81 == vault.best_dist



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
  #test_part1()
  test_part1_b()
  #test_part1_c()
  # part1()
