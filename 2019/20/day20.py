#!/usr/bin/env python3

from collections import namedtuple
import sys
import textwrap

import map
# from memoized import memoized


class PlutoMaze(object):

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

  def find_best_action(self):
    # start from cur_path, cur_dist
    reachable = self.cur_path.reachable_targets(self.cur_dist, set())
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
    best_action = self.find_best_action()
    print('best_action', best_action)
    self.move_to(best_action[2])


def test_part1():
  maze = map.Map()
  maze.load('sample20_1.txt')
  maze.print()



def part1():
  maze = map.Map()
  maze.load('input_20.txt')
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
