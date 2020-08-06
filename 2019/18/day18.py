#!/usr/bin/env python3

import sys
import time

import map
from memoized import memoized


TRACE_DIST = 0
TRACE_USE_KEY = 0
TRACE_TSORT = 1
TRACE_MEMO = 0
TRACE_TIME = 1
TRACE_RESOLVE = 0
TRACE_REDUCE = 1
VERBOSE = 0

MEMO_HOLDING = True

def P(key_set):
  return ','.join(sorted(key.name for key in key_set))

def key_names(key_set):
  return ','.join(key.name for key in key_set)

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
    self.upstream_keys = list(upstream_keys)  # keys between me and root

    # Computed state
    self.blocks = []  # list of Keys that can not be reached unless I am held
    # list of keys which must be reached before me
    self.edges_in = set()
    if blocked_by:
      self.edges_in.add(blocked_by)
    self.edges_out = set()
    self.dists = {}  # distance to every other node
    self.loop_detect = False  # used for graph error detection
    self.is_key = name.islower()


  def __str__(self):
    return 'Key<%s, %d, in_from:%s>' % (self.name, self.dist_from_root, key_names(self.edges_in))

  def __repr__(self):
    return 'Key<%s, %d, in:%s, out:%s>' % (self.name, self.dist_from_root,
        key_names(self.edges_in), key_names(self.edges_out))

  def print(self):
    print('Key:%s, dist:%3d  in:%-12s out:%-12s upstream:%-15s blocks:%-15s' % (
        self.name, self.dist_from_root, key_names(self.edges_in),
        key_names(self.edges_out),  key_names(self.upstream_keys),P(self.blocks)))

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
    return not self.is_key

  @property
  def door_name(self):
    assert self.is_key
    return self.name.upper()

  @property
  def key_name(self):
    assert not self.is_key
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
      for k in key.blocks:
        if k.is_key:
          self.reachable.add(k)
          for k2 in k.blocks:
            if k2.is_key:
             self.reachable.add(k2)
    self.holding.add(key)

  def is_holding(self, key):
    return key in self.holding

  def is_reachable(self, key):
    return key in self.reachable

  @staticmethod
  def hash_keys(s):
    ret = 0
    pos_a = ord('A')
    for k in s:
      ret |= (1 << (ord(k.name) - pos_a))
    return ret

  def holding_hash(self):
    return self.hash_keys(self.holding)

  def reachable_hash(self):
    return self.hash_keys(self.reachable)


class Vault(object):

  def __init__(self, maze):
    self.maze = maze
    self.path_heads = {}
    self.cur_dist = 0
    self.trace = True
    self.total_moved = 0
    self.keys_and_doors = {}
    self.blocked_by = {}  # map of key or door to immediately upstream blocking door
    self.min_routes = {}
    self.debug_key = None  # (char) print more tracing when visiting this key
    self.init()

  def init(self):
    self.set_start()
    self.top = Path(from_where=(-1, -1), start=self.start)
    self.cur_path = self.top
    self.maze.close_dead_ends()
    self.walk_path(self.top)
    self.all_nodes = set(self.keys_and_doors.values())

    self.resolve_edges()
    self.top.print_tree()  # TEMP
    self.compute_distances()
    self.print_distances()
    self.print_keys()
    self.best_dist = self.worst_path
    print('=upper bound for distance', self.best_dist)
    self.tsort()
    self.best_dist = self.route_distance(self.top_sorted)
    print('=better upper bound for distance', self.best_dist)
    self.n_keys = len([k for k in self.keys_and_doors if k.islower()])

  def print_keys(self):
    print('=== keys')
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

    if TRACE_RESOLVE > 0:
      print('===== resolve_edges()')
      self.print_keys()

    #
    # Replace doors in edges_in with the keys that unlock them. This gives a
    # graph of key to key without any doors.
    #
    # - make sure all doors are blocked by the key that opens them
    for node in self.all_nodes:
      if not node.is_key:
        k = self.keys_and_doors[node.key_name]
        node.edges_in.add(k)
    # - now we can reduce each
    self.r_level = 0
    for node in self.all_nodes:
      self.reduce_edges_in(node)
    # - and now we can create input edges
    for node in self.all_nodes:
      if node.is_key:
        for e_in in node.edges_in:
          e_in.edges_out.add(node)
    if TRACE_REDUCE > 0:
      print('== reduced edges')
      self.print_keys()

    # The rest might be useless

    for key, blocker_name in self.blocked_by.items():
      blocker = self.keys_and_doors[blocker_name]
      blocker.blocks.append(key)

    # remove doors that do not block anything
    v = {}
    dead_doors = set()
    for k in self.all_nodes:
      if k.is_door and not k.blocks:
        print("=== Dead door", k)
        dead_doors.add(k)
        if k in self.blocked_by:
          del self.blocked_by[k]
      else:
        v[k.name] = k
    self.keys_and_doors = v
    self.all_nodes = set(self.keys_and_doors.values())

    # remove the dead doors from the blocks list of any keys
    for k in self.all_nodes:
      k.blocks = list(filter(lambda x: x not in dead_doors, k.blocks))

    # Make sure all doors are blocked by the key that opens them
    for node in self.all_nodes:
      if not node.is_key:
        k = self.keys_and_doors[node.key_name]
        k.blocks.append(node)

    # Replace  x blocks X blocks y  with x -> y
    # This does not work. It unblocks things that might be far away.
    # replace the door I block with the things the door blocks
    if False:
      for key in self.all_nodes:
        if key.is_key:
          for i, k in enumerate(key.blocks):
            if k.name == key.name.upper():
              print('reduce key: from', key, key.blocks)
              key.blocks = key.blocks[0:i] + key.blocks[i+1:] + k.blocks
              print('reduce key:   to', key, key.blocks)
              break

  @memoized
  def reduce_edges_in(self, node):
    """Reduce edges into a node from doors.

    From: {a} -> A,  {a,b} -> B,  {B} -> c
    To: {a,b} -> c
    """
    sp = '  ' * self.r_level
    assert node
    new_edges_in = set([])
    if TRACE_REDUCE > 1:
      print('reduce_in:', node)
    for from_node in node.edges_in:
      if TRACE_REDUCE > 1:
        print('  reduce_from:', from_node)
      if from_node.is_key:
        new_edges_in.add(from_node)
      else:
        self.r_level += 1
        door_blockers = self.reduce_edges_in(from_node)
        self.r_level -= 1
        # Do not add an ancestor key.  E.g.
        #  a B c d A e   =>   e blocked_by d, NOT blocked by d,a
        for n in door_blockers:
          if from_node.key_name != n.name or n not in from_node.upstream_keys:
            new_edges_in.add(n)
    node.edges_in = new_edges_in
    return new_edges_in

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
      l.append('  %s' % x)
    print(' '.join(l))
    for start in keys:
      the_key = self.keys_and_doors[start]
      l = [start]
      for other in keys:
        if other in the_key.dists:
          l.append('%3d' % the_key.dists[other])
        else:
          l.append('  x')
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
                  upstream_keys=path.keys)
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

  def all_solutions1(self, force_start_from=None):
    """Run through the possible paths.

    Args:
      force_start_from: (char) start with this key first
    """

    # start in name order
    # keys = set(sort_keys([k for k in self.all_nodes if k.is_key]))
    # start in distance order
    keys = set(sorted(filter(lambda k: k.is_key, self.all_nodes),
                             key=lambda k: k.dist_from_root))

    blocked = set(sort_keys(self.blocked_by.keys()))
    unblocked = set(sort_keys(keys - blocked))
    print('=keys     ', P(keys))
    print('=blocked  ', P(blocked))
    print('=unblocked', P(unblocked))

    # make sure the things behind the reachable keys are also reachable
    state = State(reachable = set(unblocked))
    for key in unblocked:
      self.unblock_reachable_downstream(key, state)

    # Attempt to start from first thing in tsort. Did not help
    #first = self.top_sorted[0]
    #unblocked = [first] + list(filter(lambda x: x != first, unblocked))

    if force_start_from:
      first = self.get_key(force_start_from)
      unblocked = [first] + list(filter(lambda x: x != first, unblocked))

    # now try them all
    self.try_count = 0
    self.start_time = time.time()
    for start in unblocked:
      print('=Starting from', start)
      state = State(reachable=set(unblocked), total_dist=start.dist_from_root)
      d = start.dist_from_root + self.min_route(start, state)
      if d < self.best_dist:
        self.best_dist = d
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
      if TRACE_USE_KEY > 1:
        print(sp+' ', 'can not ulock', door)
    if TRACE_USE_KEY > 1:
      print(sp+' ', 'done: holding', P(state.holding), 'now reachable', P(state.reachable))


  def min_route(self, at_key, state):
    """Try all the paths from at_key to end of maze.

    Args:
      at_key: start point
    """
    assert at_key not in state.holding

    if TRACE_TIME > 0:
      self.try_count += 1
      if self.try_count % 10000 == 0:
        t = int(time.time() - self.start_time)
        print('=tried paths', self.try_count, ', t:', t)
    if VERBOSE > 0 or at_key.name == self.debug_key:
      sp = ' ' * state.indent
      print(sp, 'visiting ', at_key, 'dist', state.total_dist)

    """
    if ((state.total_dist + self.minimal_distance_possible_left(at_key, state.holding))
       > self.best_dist):
      sp = ' ' * state.indent
      print(sp, '=point of no return', )
      return self.worst_path
    """

    if MEMO_HOLDING:
      # XXX route_key = (at_key.name, state.holding_hash(), state.reachable_hash())
      route_key = (at_key.name, state.holding_hash())
      if route_key in self.min_routes:
        if TRACE_MEMO > 0 or at_key.name == self.debug_key:
          print('   === got a memo', P(state.holding), 'dist:', self.min_routes[route_key])
        return self.min_routes[route_key]

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
      if MEMO_HOLDING:
        # XXX self.min_routes[route_key] = state.total_dist
        self.min_routes[route_key] = 0
      return 0

    # print(sp, 'holding', P(state.holding), 'now reachable', P(state.reachable))

    # visit each that are now reachable
    to_visit = state.reachable - state.holding
    to_visit = set(key for key in to_visit if key.is_key)

    if VERBOSE > 0 or at_key.name == self.debug_key:
      print(sp, 'holding', P(state.holding), 'to_visit', P(to_visit))

    # to_visit = sorted(to_visit, key=lambda k: k.dists[at_key.name])
    #to_visit = sorted(
    #  to_visit,
    #  key=lambda k: -k.dist_from_root - 1000 * int(k.path == at_key.path))
    to_visit = sorted(
        to_visit,
        key=lambda k: k.dists[at_key.name] - 1000 * int(k.path == at_key.path))
    if VERBOSE > 0 or at_key.name == self.debug_key:
      print(sp, 'at %s want to visit' % at_key.name, P(to_visit))

    min_r = 10000000
    for to_unblock in to_visit:
      if at_key == to_unblock or to_unblock in state.holding:
        continue

      if to_unblock.is_key:
        base_dist = at_key.dists[to_unblock.name]
        if state.total_dist + base_dist < self.best_dist:
          v_state = state.clone()
          v_state.travel(at_key.dists[to_unblock.name])
          d = self.min_route(to_unblock, v_state)
          if base_dist + d < min_r:
            min_r = base_dist + d

    if MEMO_HOLDING:
      self.min_routes[route_key] = min_r
    return min_r


  def minimal_distance_possible_left(self, at_key, holding):
    """If we ignored doors, what would be the theorectial minimal distance"""

    # This is not right
    keys = set([k for k in self.all_nodes
               if k != at_key and k.is_key])
    left = keys - holding
    a_path = self.tsort_keys(left)
    return self.route_distance(a_path) - at_key.dist_from_root

    # nor this
    """
    to_visit = sorted(left, key=lambda k: k.dists[at_key.name])
    last_dist = 0
    min_dist = 0
    for key in to_visit:
      d = at_key.dists[key.name]
      min_dist += (d - last_dist)
      last_dist = d
    return min_dist
    """


  def tsort(self):
    self.top_sorted = self.tsort_keys(self.all_nodes)
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
        # if blocked.is_key:
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
    keys = set([k for k in self.all_nodes if k.is_key])
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

  def all_solutions2(self, force_start_from=None):
    """Run through the possible paths.

    Args:
      force_start_from: (char) start with this key first
    """

    key_nodes = set([k for k in self.all_nodes if k.is_key])
    possible_end_nodes = [k for k in key_nodes if not k.blocks]
    print('=all nodes:', P(key_nodes))
    print('=possible end nodes:', P(possible_end_nodes))

    blocked = set(self.blocked_by.keys())
    unblocked = self.all_nodes - blocked
    print('=unblocked', P(unblocked))

    for last in possible_end_nodes:
      self.tsort_nodes(key_nodes, end_at=last)
      #if self.best_dist < path.total_dist:
      #  self.best_dist = path.total_dist

      #self.walk_backwards(last, path_tail=[], needs=set(possible_end_nodes),
      #                    level=0)

  def walk_backwards(self, from_key, path_tail, needs, level):
    sp = ' ' * level

    print(sp, 'walk_backwards:', from_key.name, ', tail:', key_names(path_tail))

    if path_tail:
      assert from_key != path_tail[0]
    if from_key.upstream_keys:
      assert from_key != from_key.upstream_keys[-1]

    path_tail = from_key.upstream_keys + [from_key] + path_tail
    print(sp, 'walk_backwards2:', from_key.name, ', tail:', key_names(path_tail))

    # compute the keys we need to hold to get through this tail
    holding = set()
    # we also have to visit the remaining
    need = needs - set([from_key])
    for node in path_tail:
      if node.is_key:
        holding.add(node)
      else:
        need_key = self.get_key(node.key_name)
        if need_key not in holding:
          need.add(need_key)

    print(sp, 'at', from_key.name, ', need:', key_names(need),
          'tail:', key_names(path_tail))

    # left = all_nodes - set(path_tail)

    if not need:
      dist = self.route_distance(path_tail)
      print(sp, '==== Got a path: dist:', dist, path_tail)
      if dist < self.best_dist:
        self.best_dist = dist
      return

    for node in need:
      if node != path_tail[0]:
        self.walk_backwards(node, path_tail, need, level+1)
      else:
        print(sp, 'why does need have head of path_tail')

  def tsort_nodes(self, all_nodes, end_at):

    visited = set()
    cur_path = None
 
    def tsort_visit(path):
      nonlocal visited
      nonlocal cur_path

      node = path.path[0]
      print(' '*len(path.path), path)
      if len(all_nodes) == len(path.path):
        print('= Complete path: dist:', path.total_dist,
              ',', key_names(path.path))
        if self.best_dist < path.total_dist:
          self.best_dist = path.total_dist
          print('= ####### New best')
        assert not node.edges_in
        return

      if node in visited:
        raise Exception('Revisit:', node, path.path)
      #if node in path.path:
      #  raise Exception('Loop:', node, path.path)
      if path.total_dist > self.best_dist:
        print('= trimming work on path because dist:',
              try_path.total_dist, '>', self.best_dist)
        path.too_long = True

      if TRACE_TSORT > 1:
        print(' '*len(path), '=tsort_visit', node)

      if node.edges_in:
        to_try = node.edges_in
      else:
        to_try = all_nodes - set(path.path)
      for from_node in to_try:
        if from_node in path.path:
          continue
        tsort_visit(NodePath(from_node, tail=path))
      visited.add(node)



      cur_path = path
      if TRACE_TSORT > 1:
        print(' '*len(path), '=tsort order', result)
      # END

    tsort_visit(NodePath(end_at))
    while True:
      nodes_left = all_nodes - visited
      if not nodes_left:
        break
      for try_node in nodes_left:
        self.tsort_nodes(nodes_left, try_node)

    print('= ### Complete path: dist:', cur_path.total_dist, ',', key_names(cur_path.path))
    if self.best_dist < cur_path.total_dist:
      self.best_dist = cur_path.total_dist
      print('= ####### New best')

  def all_solutions(self, force_start_from=None):
    return self.all_solutions2(force_start_from=force_start_from)


class NodePath(object):
  """Path through nodes."""

  def __init__(self, head, tail=None):
    assert head
    if tail:
      self.path = [head] + list(tail.path)
      self.dist = head.dists[tail.path[0].name] + tail.dist
    else:
      self.path = [head]
      self.dist = 0
    self.too_long = False

  def __repr__(self):
    return 'Path<dist:%d, %s>' % (self.dist, key_names(self.path))
  
  @property
  def total_dist(self):
    return self.path[0].dist_from_root + self.dist


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
  print('========================================')
  vault.all_solutions()
  assert 132 == vault.best_dist


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
  vault.all_solutions()
  assert 136 == vault.best_dist


def test_part1_c():
  print('========================================  test c')
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
  dist_check(vault, 'd', 'g', 2)
  dist_check(vault, 'd', 'e', 4)
  dist_check(vault, 'd', 'h', 6)

  for start_from in ('d', 'e', 'f', 'a'):
    print('============ test c - start from %s' % start_from)
    vault = Vault(maze)
    vault.all_solutions(force_start_from=start_from)
    assert 81 == vault.best_dist


def part1():
  maze = map.Map()
  maze.load('input_18.txt')
  maze.print()
  print('========================================')
  vault = Vault(maze)
  # vault.debug_key = 'q'
  assert vault.best_dist <= 4950
  print('========================================')
  vault.all_solutions()
  assert 4950 > vault.best_dist


if __name__ == '__main__':
  test_part1_a()
  test_part1_b()
  test_part1_c()
  # part1()
