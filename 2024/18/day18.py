#!/usr/bin/env python3
"AOC 2023: day 18"

from collections import defaultdict

from tools import aoc
from tools import gridutils

DIRS=gridutils.DIRS4

class Path(object):

  def __init__(self, pos):
    self.pos = pos

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.__dict__)


class day18(aoc.aoc):

  def __init__(self):
    super(day18, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid()
    self.drops = []
    self.max_x = 0
    self.max_y = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    parts = line.split(',')
    x = int(parts[0])
    y = int(parts[1])
    self.drops.append((x, y))
    self.max_x = max(self.max_x, x)
    self.max_y = max(self.max_y, y)

  def post_load(self):
    # called after all input is read
    # print(self.drops)
    # self.grid.print()
    pass
 
  def neighbor_positions(self, pos):
    ret = []
    for dir in range(4):
      new_pos = gridutils.add_vector(pos, DIRS[dir])
      if new_pos[0] < 0 or new_pos[1] < 0:
        continue
      if new_pos[0] > self.max_x or new_pos[1] > self.max_y:
        continue
      ret.append(new_pos)
    return ret

  def part1(self):
    print('===== Start part 1')
    self.reset()

    limit = 1024
    if self.doing_sample:
      limit = 12
    points = set()
    for drop in range(limit):
      self.grid.set_pos(self.drops[drop], '#')
      points.add(self.drops[drop])
    if self.doing_sample:
      self.grid.print()
    ret = self.find_shortest_path(points)
    return ret

  def find_shortest_path(self, points):
    # plain old flood fill
    at = (0,0)
    frontier = set([at])
    visited = set([at])
    grid = gridutils.Grid()
    for pos in points:
      grid.set_pos(pos, "#")
    ret = -1
    for cost in range((self.max_x + 1) * (self.max_y + 1)):
      nf = set()
      for pos in frontier:
        for n in self.neighbor_positions(pos):
          if n in points:
            continue
          # print(n)
          if n in visited:
            continue
          grid.set_pos(n, "O")
          visited.add(n)
          nf.add(n)
          if n == (self.max_x, self.max_y):
            return cost + 1
            break
      frontier = nf
    if self.doing_sample:
      print("Could not solve")
      grid.print()
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    pre_run = 1024
    if self.doing_sample:
      pre_run = 12
    points = set()
    for drop in range(pre_run):
      self.grid.set_pos(self.drops[drop], '#')
      points.add(self.drops[drop])
    for drop in self.drops[pre_run:]:
      points.add(drop)
      self.grid.set_pos(drop, 'X')
      ret = self.find_shortest_path(points)
      if ret > 0:
        # print("Still can solve at", drop, "with cost", ret)
        continue
      print("break at", drop)
      if self.doing_sample:
        self.grid.print()
      return '%d,%d' % drop
    return -1


day18.sample_test("""
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""", expect1=22, expect2="6,1")


if __name__ == '__main__':
  day18.run_and_check('input.txt', expect1=344, expect2="46,18")
