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

def sort_keys(key_set):
  return sorted(key_set, key=lambda k: k.name)


class Key(object):

  def __init__(self, name, path, dist_from_root, dist_down_path=None,
               blocked_by=None, upstream_keys=None):
    self.name = name
    self.path = path
    self.dist_from_root = dist_from_root
    self.dist_down_path = dist_down_path
    self.blocked_by = blocked_by
    self.upstream_keys = upstream_keys  # keys between me and root
    self.blocks = []  # list of Keys that can not be reached unless I am held
    self.dists = {}
    self.loop_detect = False
    self.is_key = name.islower()

  def __str__(self):
    return 'Key<%s, %d>' % (self.name, self.dist_from_root)

  def __repr__(self):
    return 'Key<%s, %d>' % (self.name, self.dist_from_root)

  def print(self):
    print('Key:%s, dist:%2d, upstream:%-10s blocks:%s' % (
        self.name, self.dist_from_root, P(self.upstream_keys), P(self.blocks)))

  def path_from_root(self):
    ret = []
    path = self.path
    while path:
      ret.append(path)
      path = path.parent
    ret.reverse()
    return ret

  @property
  def is_door(self):
    return self.name.isupper()

  @property
  def door_name(self):
    return self.name.upper()

  @property
  def key_name(self):
    return self.name.lower()

  def is_reachable(self, state):
    for key in self.upstream_keys:
      if key in state.holding:
        continue
      if key.is_key and key in state.reachable:
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


class State(object):

  def __init__(self, holding=None, reachable=None, total_dist=0):
    self.holding = holding or set()   # set of keys we have picked up
    # what we can reach (which may include what we picked up)
    self.reachable = reachable or set()
    self.total_dist = total_dist
    self.indent = 0
    self.visited = []

  def clone(self):
    ret = State(holding=set(self.holding), reachable=set(self.reachable),
                total_dist=self.total_dist)
    ret.indent = self.indent + 1
    ret.visited = list(self.visited)
    return ret

  def travel(self, dist):
    self.total_dist += dist

  def pick_up(self, key):
    if key.is_key and not self.is_holding(key):
      self.visited.append(key.name)
    self.holding.add(key)

  def is_holding(self, key):
    return key in self.holding

  def is_reachable(self, key):
    return key in self.reachable


class Vault(object):

  def __init__(self, maze):
    self.maze = maze
    self.path_heads = {}
    self.cur_dist = 0
    self.trace = True
    self.total_moved = 0
    self.keys_and_doors = {}
    self.blocked_by = {}  # map of key or door to immediately upstream blocking door
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
    self.print_distances()
    self.best_dist = self.worst_path
    print('=upper bound for distance', self.best_dist)
    self.tsort()
    self.best_dist = self.route_distance(self.top_sorted)
    print('=better upper bound for distance', self.best_dist)
    self.n_keys = len([k for k in self.keys_and_doors if k.islower()])

  def print_block_list(self):
    for name, key in self.keys_and_doors.items():
      print('= key', name, 'blocks', key.blocks)


  def print_keys(self):
    for name in sorted(self.keys_and_doors):
      self.get_key(name).print()

  def set_start(self):
    self.start = None
    for pos, c in self.maze.points.items():
      if c == '@':
        self.start = pos
        return

  def add_key(self, keylock):
    self.keys_and_doors[keylock.name] = keylock

  def get_key(self, keyname):
    return self.keys_and_doors.get(keyname)

  def resolve_edges(self):
    """Create edges from keys to the doors they unlock."""
    for key in self.keys_and_doors.values():
      # Make sure all doors are blocked by the key that opens them
      if key.is_door:
        k = self.keys_and_doors[key.key_name]
        k.blocks.append(key)

    for key, blocker_name in self.blocked_by.items():
      blocker = self.keys_and_doors[blocker_name]
      blocker.blocks.append(key)
      # Why does this not work. If I am blocked by a door, then
      # also make the door key block me.
      # if blocker.is_door:
      #   self.keys_and_doors[blocker_name.lower()].blocks.append(key)

  def compute_distances(self):
    """Compute distances from each key to key, ignoring doors."""
    self.worst_path = 0
    for name, key in self.keys_and_doors.items():
      if name.isupper():
        continue
      rp = key.path_from_root()
      for other_name, other_key in self.keys_and_doors.items():
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

  def print_distances(self):
    keys = sorted(filter(lambda x: x.islower(), self.keys_and_doors.keys()))
    l = [' ']
    for x in keys:
      l.append(' %s' % x)
    print(' '.join(l))
    for start in keys:
      the_key = self.keys_and_doors[start]
      l = [start]
      for other in keys:
        if other in the_key.dists:
          l.append('%2d' % the_key.dists[other])
        else:
          l.append(' x')
      print(' '.join(l))


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
    keys = set(sort_keys([k for k in self.keys_and_doors.values() if k.is_key]))
    blocked = set(sort_keys(self.blocked_by.keys()))
    unblocked = set(sort_keys(keys - blocked))
    print('=keys', keys)
    print('=blocked', blocked)
    print('=unblocked', unblocked)

    # make sure the things behind the reachable keys are also reachable
    state = State(reachable = set(unblocked))
    for key in unblocked:
      self.unblock_reachable_downstream(key, state)
    # now try them all
    self.try_count = 0
    self.start_time = time.time()
    for start in unblocked:
      print('=Starting from', start)
      state = State(reachable=set(unblocked), total_dist=start.dist_from_root)
      status = self.try_paths(start, state)
    print('best traversal distance', self.best_dist)


  def unblock_reachable_downstream(self, key, state):
    # given what we are holding, add 
    if TRACE_USE_KEY > 0:
      sp = ' ' * (state.indent + 1)
      print(sp, 'adding downstream reachabilty for', key, 'blocks', key.blocks)
    for downstream in key.blocks:
      state.reachable.add(downstream)
      if state.holding and (
          downstream.is_key or downstream.key_name in state.holding):
        self.unblock_reachable_downstream(downstream, state)

  def pick_up_key(self, at_key, state):
    """Unlock what we can based on having this key.

    Mark the keys downstream of the door for this key reachable.
    """
    sp = ' ' * state.indent
    door = self.keys_and_doors.get(at_key.name.upper())
    if not door:
      return
    state.pick_up(door)
    if TRACE_USE_KEY > 0:
      print(sp, 'pick_up_key', at_key, 'holding', P(state.holding),
            'reachable', P(state.reachable))
    if door.is_reachable(state):
      state.reachable.add(door)
      self.unblock_reachable_downstream(door, state)
    else:
      print(sp+' ', 'can not ulock', door)
    if TRACE_USE_KEY > 1:
      print(sp+' ', 'done: holding', P(state.holding), 'now reachable', P(state.reachable))

  def try_paths(self, at_key, state):
    """Try all the paths from at_key to end of maze.

    Args:
      at_key: start point
    """
    assert at_key not in state.holding

    self.try_count += 1
    if self.try_count % 1000 == 0:
      t = int(time.time() - self.start_time)
      print('=tried paths', self.try_count, ', t:', t)
    sp = ' ' * state.indent
    print(sp, 'visiting ', at_key, 'dist', state.total_dist)
    if state.total_dist > self.best_dist:
      print(sp, 'gone too far')
      return -1

    """ Not ready yet
    if ((state.total_dist + self.minimal_distance_possible_left(at_key, state.holding))
       > self.best_dist):
      print(sp, '=point of no return')
      return -2
    """

    state.pick_up(at_key)
    # If we are at a key, then we must have picked up all the upstream things
    for key in at_key.upstream_keys:
      assert key != at_key
      state.pick_up(key)
      self.pick_up_key(key, state)
    self.pick_up_key(at_key, state)

    if len(state.holding) == len(self.keys_and_doors):
      print('=complete set: dist', state.total_dist,
            ', '.join(state.visited))
      self.best_dist = min(self.best_dist, state.total_dist)
      return 1

    # print(sp, 'holding', P(state.holding), 'now reachable', P(state.reachable))

    # visit each that are now reachable
    to_visit = state.reachable - state.holding
    to_visit = set(key for key in to_visit if key.is_key)

    print(sp, 'holding', P(state.holding), 'to_visit', P(to_visit))

    # to_visit = sorted(to_visit, key=lambda k: k.dists[at_key.name])
    #to_visit = sorted(
    #  to_visit,
    #  key=lambda k: -k.dist_from_root - 1000 * int(k.path == at_key.path))
    to_visit = sorted(
        to_visit,
        key=lambda k: k.dists[at_key.name] - 1000 * int(k.path == at_key.path))
    print(sp, 'at %s want to visit' % at_key.name, P(to_visit))

    for to_unblock in to_visit:
      if at_key == to_unblock or to_unblock in state.holding:
        continue

      if to_unblock.is_key:
        v_state = state.clone()
        v_state.travel(at_key.dists[to_unblock.name])
        status = self.try_paths(to_unblock, v_state)
        if status < 0:
          return 0
    return 0

  def minimal_distance_possible_left(self, at_key, holding):
    # this is a theoretcial minimal distance
    keys = set([k for k in self.keys_and_doors.values()
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
    self.top_sorted = self.tsort_keys(self.keys_and_doors.values())
    print('=tsort:', self.top_sorted)

  @staticmethod
  def tsort_keys(list_of_keys):

    ordered = set()
    result = []

    def tsort_visit(key, depth):
      nonlocal result
      nonlocal ordered

      if key in ordered:
        return
      if key.loop_detect:
        raise Exception('not a DAG')
      key.loop_detect = True
      if TRACE_TSORT > 1:
        print(' '*depth, '=tsort_visit', key)
      for blocked in key.blocks:
        #if blocked.is_key:
        tsort_visit(blocked, depth=depth+1)
      key.loop_detect = False
      ordered.add(key)
      result = [key] + result
      if TRACE_TSORT > 1:
        print(' '*depth, '=tsort order', result)
      # END

    while True:
      keys = [k for k in list_of_keys if k not in ordered]
      if not keys:
        break
      tsort_visit(keys[0], depth=0)
    return result


  def tsort_solutions(self):
    keys = set([k for k in self.keys_and_doors.values() if k.is_key])
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
        v = an_ordering[u_i]   # OR  an_ordering[u+1]
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


def test_part1_a():
  print('========================================  test a')
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
  print('==keys_and_doors')
  print(vault.keys_and_doors)
  print('==blocked by')
  print(vault.blocked_by)
  vault.print_block_list()
  print('========================================')
  vault.top.print_tree()
  vault.all_solutions()
  assert 132 == vault.best_dist
  # vault.tsort_solutions()


def test_part1_b():
  print('========================================  test b')
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
  maze.print()
  # Shortest paths are 136 steps;
  # one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m

  vault = Vault(maze)
  print(vault.blocked_by)
  print('========================================')
  vault.top.print_tree()
  vault.print_keys()
  vault.all_solutions()
  # vault.tsort_solutions()
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
  assert vault.best_dist <= 5218
  print('========================================')
  vault.all_solutions()
  assert 5218 > vault.best_dist



if __name__ == '__main__':
  test_part1_a()
  test_part1_b()
  # test_part1_c()
  # part1()
