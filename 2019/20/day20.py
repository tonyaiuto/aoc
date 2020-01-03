#!/usr/bin/env python3

from collections import defaultdict

import map


class PlutoMaze(object):

  def __init__(self):
    self.maze = map.Map(label_width=2, open=['.'], ignore=[' '])

  def load(self, file):
    self.maze.load(file)
    self.label_to_pos = defaultdict(list)
    for pos, label in self.maze.portals.items():
      self.label_to_pos[label].append(pos)
    # print(self.label_to_pos)
    self.jumps = {}
    for l, pairs in self.label_to_pos.items():
      if len(pairs) == 2:
        self.jumps[pairs[0]] = pairs[1]
        self.jumps[pairs[1]] = pairs[0]

    self.maze.close_dead_ends()

    self.start = self.label_to_pos['AA'][0]
    self.end = self.label_to_pos['ZZ'][0]

    def change_to_walls(pos, v):
      if v and v not in ('#', '.'):
        del self.maze.points[pos]

    self.maze.for_each_cell(change_to_walls)


  def print(self):
    self.maze.print()

  def find_min_path(self):
    best_dist = self.maze.width * self.maze.height
    for dist,more in self.walk_path(self.start, self.end, dict(), 0):
      print(dist, more)
      if more == 'end':
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
        # print('JUMP', jump)
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


if __name__ == '__main__':
  test_part1()
  part1()
