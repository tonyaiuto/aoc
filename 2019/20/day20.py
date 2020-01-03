#!/usr/bin/env python3

from collections import defaultdict
import sys

import map


class PlutoMaze(object):

  def __init__(self):
    self.maze = map.Map(label_width=2, open=['.'], ignore=[' '])
    self.jumps = {}
    self.start = None
    self.end = None

  def clone(self):
    ret = PlutoMaze()
    ret.maze = self.maze.clone()
    ret.jumps = dict(self.jumps)
    ret.start = self.start
    ret.end = self.end
    return ret

  def load(self, file):
    # Load the maze and make it ready to work with
    self.maze.load(file)

    label_to_pos = defaultdict(list)
    for pos, label in self.maze.portals.items():
      if label == 'AA':
        self.start = pos
      elif label == 'ZZ':
        self.end = pos
      else:
        label_to_pos[label].append(pos)
    # print(label_to_pos)
    for l, pairs in label_to_pos.items():
      self.jumps[pairs[0]] = pairs[1]
      self.jumps[pairs[1]] = pairs[0]

    self.maze.close_dead_ends()

    def change_to_walls(pos, v):
      if v and v not in ('#', '.'):
        del self.maze.points[pos]

    self.maze.for_each_cell(change_to_walls)

  def print(self):
    self.maze.print()

  def is_pos_on_edge(self, pos):
    x = pos[0]
    y = pos[1]
    return (x == 0 or x == self.maze.width-1
            or y == 0 or y == self.maze.height-1)

  def find_min_path(self):
    best_dist = self.maze.width * self.maze.height
    for dist,more in self.walk_path(self.start, self.end, dict(), 0):
      if more == 'end':
        print('got to end in', dist)
        best_dist = min(best_dist, dist)
    return best_dist

  def walk_path(self, pos, end, visited, dist):
    while True:
      if pos == end:
        yield dist, 'end'
      visited[pos] = dist
      moves = self.maze.get_moves(pos, visited)
      jump = self.jumps.get(pos)
      if jump and jump not in visited:
        # print('JUMP', jump, self.maze.portals[jump])
        moves.append(jump)
      # print('at', pos, 'dist', dist, 'moves', moves)
      if not moves:
        break
      dist += 1
      if len(moves) == 1:
        pos = moves[0]
        continue
      for branch in moves:
        for n_dist, more in self.walk_path(branch, end, dict(visited), dist):
          yield n_dist, more
      break
    yield -1, 'dead end'


def test_part1():
  maze = PlutoMaze()
  maze.load('sample20_1.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert 23 == best_dist

  maze = PlutoMaze()
  maze.load('sample20_2.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert 58 == best_dist

def part1():
  maze = PlutoMaze()
  maze.load('input_20.txt')
  maze.print()
  print('========================================')
  best_dist = maze.find_min_path()
  print('part1:', best_dist)
  assert 632 == best_dist

  # check that clone works
  m2 = maze.clone()
  best_dist = m2.find_min_path()
  assert 632 == best_dist


class RecursivePlutoMaze(PlutoMaze):

  def __init__(self):
    super(RecursivePlutoMaze, self).__init__()

  def find_min_path(self):

    self.visited = {}
    self.visited[0] = dict()
    self.portals_used = set()

    best_dist = None
    for dist,more in self.walk_path(
        self.start, self.end, self.visited[0], set(), dist=0, level=0):
      print(dist, more)
      if more == 'end':
        if best_dist is None:
          best_dist = dist
        else:
          best_dist = min(best_dist, dist)
    return best_dist

  def walk_path(self, pos, end, visited, in_jumps, dist, level):

    while True:
      if pos == end and level == 0:
        yield dist, 'end'
      visited[pos] = dist
      moves = self.maze.get_moves(pos, visited)
      jump = self.jumps.get(pos)
      if jump and jump in visited:
        jump = None
      print('at level', level, pos, 'dist', dist, 'moves', moves)
      if not moves and not jump:
        break
      dist += 1
      if len(moves) == 1 and not jump:
        pos = moves[0]
        continue
      for branch in moves:
        for n_dist, more in self.walk_path(
            branch, end, self.visited[level], set(in_jumps), dist, level=level):
          yield n_dist, more

      if jump:
        if self.is_pos_on_edge(jump):
          # outer jump
          if level == 0:
            return
          new_level = level - 1
          print('Jump out', jump, self.maze.portals[jump], 'level', level-1)
        else:
          # inner jump
          if jump in in_jumps:
            print('would recurse on', jump, self.maze.portals[jump])
            yield -1, 'recurse'
            return
          in_jumps.add(jump)

          new_level = level + 1
          print('Jump in', jump, self.maze.portals[jump], 'level', new_level)
          if not self.visited.get(new_level):
            self.visited[new_level] = dict()

          # mark the jumping off point as visited so we do not go deeper
          self.visited[new_level][pos] = dist

        print('shift to level', level, pos, '=>', jump)
        sys.stdout.flush()
        for n_dist, more in self.walk_path(
            jump, end, self.visited[new_level], set(in_jumps), dist=dist, level=new_level):
          yield n_dist, more
      break
    yield -1, 'dead end'


def test_part2():
  maze = RecursivePlutoMaze()
  maze.load('sample20_1.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert 26 == best_dist

  maze = RecursivePlutoMaze()
  maze.load('sample20_2.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert None == best_dist


  maze = RecursivePlutoMaze()
  maze.load('sample20_3.txt')
  maze.print()
  best_dist = maze.find_min_path()
  print('sample3 best', best_dist)
  assert -1 == best_dist


def part2():
  maze = PlutoMaze()
  maze.load('input_20.txt')
  maze.print()
  print('========================================')
  best_dist = maze.find_min_path()
  print('part2:', best_dist)
  assert 632 == best_dist


if __name__ == '__main__':
  #test_part1()
  #part1()
  test_part2()
