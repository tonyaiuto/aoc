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


class Key(object):

  def __init__(self, name, path, dist_from_root, blocked_by=None):
    self.name = name
    self.path = path
    self.dist_from_root = dist_from_root
    self.blocked_by = blocked_by
    self.dists = {}

  def __str__(self):
    return 'Key<%s, %d>' % (self.name, self.dist_from_root)

  def __repr__(self):
    return 'Key<%s, %d>' % (self.name, self.dist_from_root)

  def path_from_root(self):
    ret = []
    path = self.path
    while path:
      ret.append(path)
      path = path.parent
    ret.reverse()
    return ret


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
    if key_name.islower():
      del self.keys[key_name]
    self.stuff = [keylock for keylock in self.stuff
                  if keylock.name != key_name]


  def reachable_targets(self, cur_at=0, total_dist=0, holding=None):
    reachable = {}
    self._reachable_downstream(reachable, holding, cur_at, total_dist)

    # Now that we have downstream, move back up and look.
    cur_fork = self.parent
    if not cur_fork:
      return reachable

    # move to fork point (== dist to base of path + up to fork)
    total_dist = cur_at + 1
    for fork in cur_fork.forks:
      if fork == self:
        continue
      # Walk back cur_at distance to forking point and deal with siblings
      fork._reachable_downstream(
          reachable, holding, cur_at=0, total_dist=total_dist+1)

    # Account for locks & keys on reverse of path to parent
    for keylock in cur_fork.stuff:
      if keylock.name.isalpha():
        reachable[keylock.name] = KeyLock(
            keylock.name, self.base_dist - keylock.dist, keylock.path)
      if keylock.name.islower():
        print('parent key', keylock.name, 'at', self.base_dist - keylock.dist)
        holding.add(keylock.name)

    # now we can reach from our grandparent in the normal way
    if cur_fork.parent:
      total_dist += self.base_dist
      cur_fork.parent._reachable_downstream(
          reachable=reachable,
          holding=holding,
          cur_at=0,
          total_dist=total_dist,
          exclude=cur_fork)
    return reachable


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
    self.compute_distances()

  def set_start(self):
    self.start = None
    for pos, c in self.maze.points.items():
      if c == '@':
        self.start = pos
        return

  def add_key(self, keylock):
    self.all_keys[keylock.name] = keylock


  def compute_distances(self):
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


  def walk_path(self, path, dist_from_root=0, last_key=None):
    # trace out the tree
    self.path_heads[path.start] = -1
    pos = path.start
    while True:
      path.visited[pos] = path.dist
      content = self.maze.cell(pos)
      if content.isalpha():
        key = Key(content, path, dist_from_root + path.dist,
                  blocked_by=last_key)
        self.add_key(key)
        if last_key:
          self.blocked_by[key] = last_key.name.lower()
        last_key = key

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
        self.walk_path(child_path, dist_from_root=dist_from_root + path.dist,
                       last_key=last_key)
      break
    # path.print()

  def find_best_action(self):
    # start from cur_path, cur_dist
    reachable = self.cur_path.reachable_targets(
        cur_at=self.cur_dist, total_dist=0, holding=set(self.holding))
    if self.trace:
      print('reachable:', reachable)
    # {'A': (A, 2, path@7,3), 'e': (e, 4, path@7,3), 'F': (F, 6, path@7,3), 'g': (g, 8, path@7,3), 'D': (D, 34, path@5,3)}
    best_door = None
    for content, thing in reachable.items():
      dist = thing[1]
      if content.isupper():
        key = reachable.get(content.lower())
        if key:
          if best_door == None or dist < best_door[1]:
            best_door = (content, dist, key)
    if best_door is None and reachable:
      door_name = self.last_pick.upper()
      door = reachable[door_name]
      return (door_name, door[1], door)
    return best_door

  def move_to(self, keyloc):
    self.ploc()
    key_name = keyloc[0]
    to_path = keyloc[2]
    route = self.cur_path.route_to(to_path)
    if to_path in route:
      print('can move out to', to_path, route)
      self.total_moved += self.traverse_to(to_path, key_name, route)
    else:
      raise Exception('no route to', keyloc)
    self.ploc()

  def ploc(self):
    print('now at path', self.cur_path, 'dist', self.cur_dist,
          'holding', self.holding)


  def traverse_to(self, to_path, key_name, route):
    # move from current pos to the new place
    dist = 0
    while True:
      print('traversing to, route', to_path, route)
      self.ploc()
      nxt = route[0]
      route = route[1:]
      if nxt == self.cur_path:
        continue
      if self.cur_path.parent == nxt:
        print('moving on up')
        self.cur_path = nxt
        if self.cur_dist > 0:
          dist += self.cur_dist
        self.cur_dist = 0
        dist += nxt.base_dist + 1
      else:
        # traverse down
        dist_to_path = nxt.base_dist - self.cur_dist
        dist += dist_to_path
        self.cur_path = nxt
        self.cur_dist = 0

      if to_path == self.cur_path:
        break

    # now we are at the right path, move to the key
    key_dist = self.cur_path.keys[key_name]
    pick_or_open = set()
    for keylock in self.cur_path.stuff:
      if keylock.name.isalpha() and keylock.dist <= key_dist:
        if keylock.name.islower():
          print('Drive by pickup key', keylock.name)
          pick_or_open.add(keylock.name)
          self.last_pick = keylock.name
        elif (keylock.name.lower() in self.holding
              or keylock.name.lower() in pick_or_open):
          print('Drive by unlock', keylock.name)
          pick_or_open.add(keylock.name)

    for key_name in pick_or_open:
      if key_name.islower():
        self.pick_up(key_name)
      else:
        self.unlock(key_name)

    dist += key_dist
    self.cur_dist = key_dist
    print('travese_to: moved', dist)
    return dist

  def pick_up(self, key_name):
    self.holding.add(key_name)
    self.cur_path.drop_key(key_name)

  def unlock(self, key_name):
    self.cur_path.drop_key(key_name)


  def do_it(self, start_path):
    self.cur_loc = start_path
    self.holding = set()
    while True:
      print('\n=== New round')
      if not self.do_round():
        break
    print('total moved', self.total_moved)

  def do_round(self):
    best_action = self.find_best_action()
    print('best_action', best_action)
    if not best_action:
      print('no more actions. total moved', self.total_moved)
      return False
    self.move_to(best_action[2])
    return True


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
  vault.do_it(vault.top)


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
