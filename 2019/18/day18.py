#!/usr/bin/env python3

import sys
import time

import map
from memoized import memoized


TRACE_DIST = 0
TRACE_USE_KEY = 1
TRACE_TSORT = 1


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
    self.ordered = False
    self.loop_detect = False
    self.is_key = name.islower()

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
      if key.is_key and key in reachable:
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
    self.top.print_tree()  # TEMP
    self.compute_distances()
    self.best_dist = self.worst_path
    print('=upper bound for distance', self.best_dist)
    self.tsort()
    self.best_dist = self.route_distance(self.top_sorted)
    print('=better upper bound for distance', self.best_dist)
    self.n_keys = len([k for k in self.all_keys if k.islower()])

  def print_block_list(self):
    for name, key in self.all_keys.items():
      print('= key', name, 'blocks', key.blocks)

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
    for name, key in self.all_keys.items():
      if name.isupper():
        # I am a door, make sure my key blocks me
        k = self.all_keys[name.lower()]
        if key.blocked_by != k:
          k.blocks.append(key)
    for key, blocker_name in self.blocked_by.items():
      blocker = self.all_keys[blocker_name]
      blocker.blocks.append(key)
      # Why does this not work. If I am blocked by a door, then
      # also make the door key block me.
      # if blocker_name.isupper():
      #   self.all_keys[blocker_name.lower()].blocks.append(key)

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
          try:
            rp2 = other_key.path_from_root()
            fork_dist = None
            for i in range(min(len(rp), len(rp2))):
              if rp[i] != rp2[i]:
                # path i-1 is common ancestor
                fork_dist = rp[i].dist_from_root - 1
                break
            if fork_dist is None:
              # one must be a downstream path of the other
              dist = abs(key.dist_from_root - other_key.dist_from_root)
            else:
              # compute distance from juncture
              dist = ((key.dist_from_root - fork_dist)
                      + (other_key.dist_from_root - fork_dist))
          except Exception as e:
            print('was computing dist from %s to %s' % (key, other_key))
            raise e

        if TRACE_DIST:
          print('dist %s %s = %d' % (name, other_name, dist))
        key.dists[other_name] = dist
        other_key.dists[name] = dist
        self.worst_path += dist

  def route_distance(self, route):
    # What is distance along a specific route
    dist = 0
    last_key = None
    for key in route:
      if key.is_key:
        if not last_key:
          dist = key.dist_from_root
        else:
          dist += last_key.dists[key.name]
        last_key = key
    return dist


  def walk_path(self, path, dist_from_root=0, last_key=None):
    # trace out the tree
    self.path_heads[path.start] = -1
    pos = path.start
    while True:
      path.visited[pos] = path.dist
      content = self.maze.cell(pos)
      if content.isalpha():
        key = Key(content, path, dist_from_root + path.dist,
                  blocked_by=last_key, dist_down_path=path.dist,
                  upstream_keys=list(path.keys))
        self.add_key(key)
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
    keys = set([k for k in self.all_keys.values() if k.is_key])
    blocked = set(self.blocked_by.keys())
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
    self.try_count = 0
    self.start_time = time.time()
    for start in unblocked:
      print('=Starting from', start)
      total_dist = start.dist_from_root
      self.try_paths(start, set(), set(reachable), total_dist, visit_list=[],
                     indent=0)
    print('best traversal distance', self.best_dist)


  def unblock_reachable_downstream(self, key, holding, reachable, indent=0):
    if TRACE_USE_KEY > 0:
      sp = ' ' * indent
      print(sp, 'adding downstream reachabilty for', key, 'blocks', key.blocks)
    for downstream in key.blocks:
      reachable.add(downstream)
      if downstream.is_key or downstream.name.lower() in holding:
        self.unblock_reachable_downstream(
            downstream, holding, reachable, indent)

  def use_key(self, at_key, holding, reachable, indent=0):
    # make the keys downstream of the door for this key reachable
    sp = ' ' * indent
    door = self.all_keys.get(at_key.name.upper())
    if not door:
      return
    holding.add(door)
    if TRACE_USE_KEY > 0:
      print(sp, 'use_key', at_key, 'holding', P(holding),
            'reachable', P(reachable))
    if door.is_reachable(holding, reachable):
      reachable.add(door)
      self.unblock_reachable_downstream(door, holding, reachable, indent+1)
    else:
      print(sp+' ', 'can not ulock', door)
    if TRACE_USE_KEY > 1:
      print(sp+' ', 'done: holding', P(holding), 'now reachable', P(reachable))

  def try_paths(self, at_key, holding, reachable, total_dist, visit_list,
                indent):
    # holding is the keys we have picked up
    # reachable is what we can reach (which may include what we picked up
    if at_key in holding:
      return 0
    self.try_count += 1
    if self.try_count % 1000 == 0:
      t = int(time.time() - self.start_time)
      print('=tried paths', self.try_count, ', t:', t)
    sp = ' ' * indent
    print(sp, 'visiting ', at_key, 'dist', total_dist)
    if total_dist >= self.best_dist:
      print(sp, 'gone too far')
      return -1

    """ Not ready yet
    if ((total_dist + self.minimal_distance_possible_left(at_key, holding))
       > self.best_dist):
      print(sp, '=point of no return')
      return -2
    """

    holding.add(at_key)
    visit_list.append(at_key.name)
    # If we are at a key, then we must have picked up all the upstream things
    for key in at_key.upstream_keys:
      if key.is_key and key not in holding:
        visit_list.append(key.name)
      holding.add(key)
      self.use_key(key, holding, reachable, indent=indent)
    self.use_key(at_key, holding, reachable, indent=indent)

    if len(holding) == len(self.all_keys):
      print('=complete set: dist', total_dist,
            ', '.join(visit_list[0:self.n_keys]))
      self.best_dist = min(self.best_dist, total_dist)
      return 1

    print(sp, 'holding', P(holding), 'now reachable', P(reachable))

    # visit each that are now reachable
    to_visit = reachable - holding
    to_visit = set(key for key in to_visit if key.is_key)
    # to_visit = sorted(to_visit, key=lambda k: k.dists[at_key.name])
    #to_visit = sorted(
    #  to_visit,
    #  key=lambda k: -k.dist_from_root - 1000 * int(k.path == at_key.path))
    to_visit = sorted(
        to_visit,
        key=lambda k: k.dists[at_key.name] - 1000 * int(k.path == at_key.path))
    print(sp, 'at %s want to visit' % at_key.name, P(to_visit))

    for to_unblock in to_visit:
      if at_key == to_unblock:
        continue
      if to_unblock.is_key and to_unblock not in holding:
        status = self.try_paths(
            to_unblock, set(holding), set(reachable),
            total_dist = total_dist + at_key.dists[to_unblock.name],
            visit_list = list(visit_list),
            indent = indent + 1)
        if status < 0:
          return 0
    return 0

  def minimal_distance_possible_left(self, at_key, holding):
    # this is a theoretcial minimal distance
    keys = set([k for k in self.all_keys.values()
               if k != at_key and k.is_key])
    left = keys - holding
    to_visit = sorted(left, key=lambda k: k.dists[at_key.name])
    last_dist = 0
    min_dist = 0
    for key in to_visit:
      d = at_key.dists[key.name]
      min_dist += (d - last_dist)
      last_dist = d
    return min_dist

  def tsort(self):
    self.top_sorted = []
    while True:
      #keys = [k for k in self.all_keys.values() if k.is_key and not k.ordered]
      keys = [k for k in self.all_keys.values() if not k.ordered]
      if not keys:
        break
      self.tsort_visit(keys[0], depth=0)
    print('=tsort:', self.top_sorted)

  def tsort_visit(self, key, depth):
    if key.ordered:
      return
    if key.loop_detect:
      raise Exception('not a DAG')
    key.loop_detect = True
    if TRACE_TSORT > 1:
      print(' '*depth, '=tsort_visit', key)
    for blocked in key.blocks:
      #if blocked.is_key:
      self.tsort_visit(blocked, depth=depth+1)
    key.loop_detect = False
    key.ordered = True
    self.top_sorted = [key] + self.top_sorted
    if TRACE_TSORT > 1:
      print(' '*depth, '=tsort order', self.top_sorted)


  def tsort_solutions(self):
    keys = set([k for k in self.all_keys.values() if k.is_key])
    blocked = set(self.blocked_by.keys())
    unblocked = keys - blocked
    print('=keys', keys)
    print('=blocked', blocked)
    print('=unblocked', unblocked)

    an_ordering = [k for k in self.top_sorted if k.is_key]

    # https://en.wikipedia.org/wiki/Topological_sorting
    for start in unblocked:
      d = {k: self.best_dist for k in an_ordering}
      d[start] = 0
      p = [None] * len(an_ordering)
      # find start pos
      for u, k in enumerate(an_ordering):
        if k == start:
          start_pos = u
      for u_i in range(start_pos, len(an_ordering)-1):
        u = an_ordering[u]
        v = an_ordering[u+1]
        dist = an_ordering[u].dists[v.name]
        if d[v] > d[u] + dist:
          d[v] = d[u] + dist
          # p[v] = u



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
  print('==all_keys')
  print(vault.all_keys)
  print('==blocked by')
  print(vault.blocked_by)
  vault.print_block_list()
  print('========================================')
  vault.top.print_tree()
  # vault.do_it(vault.top)
  vault.all_solutions()
  # vault.tsort_solutions()


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
  vault.best_dist = 5218
  print('========================================')
  vault.all_solutions()
  assert 5218 > vault.best_dist



if __name__ == '__main__':
  test_part1()
  test_part1_c()
  # test_part1_b()
  # part1()
