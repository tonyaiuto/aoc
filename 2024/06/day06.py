#!/usr/bin/env python3
"AOC 2023: day 06"

from collections import defaultdict

from tools import aoc
from tools import gridutils


class day06(aoc.aoc):

  def __init__(self):
    super(day06, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid() # ignore='.'

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)
    g_x = line.find('^')
    if g_x >= 0:
      self.guard_start = (g_x, self.grid.height)
      print('guard at', self.guard_start, self.grid.get_pos(self.guard_start))
      # self.grid.set(g_x, self.grid.height, ' ')

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      self.grid.print()
    self.max_loop = self.grid.width * self.grid.height


  def part1(self):
    print('===== Start part 1')
    self.reset()
    at = self.guard_start
    dir_index = 0
    visited = set([at])
    vg = gridutils.Grid()
    while True:
      visited.add(at)
      np = gridutils.move_in_dir(at, dir=gridutils.DIRS4[dir_index])
      if self.grid.get_pos(np) == '#':
        vg.set(np[0], np[1], '#')
        # print('from', at, 'to', np, 'would collide', self.grid.get_pos(np))
        # would colide
        dir_index = (dir_index + 1) % 4
        np = gridutils.move_in_dir(at, dir=gridutils.DIRS4[dir_index])
      if (np[0] < 0 or np[0] > self.grid.max_x 
          or np[1] < 0 or np[1] > self.grid.max_y):
        break 
      at = np
      # print('from', at, 'to', np, self.grid.get_pos(np), 'visited', len(visited))
      # vg.set(at[0], at[1], 'X')
  
    # vg.print()
    return len(visited)

  def part2(self):
    print('===== Start part 2')
    self.reset()
    at = self.guard_start
    dir_index = 0
    n_pos = 0
    added = set()
    while True:
      np = gridutils.move_in_dir(at, dir=gridutils.DIRS4[dir_index])
      if (np[0] < 0 or np[0] > self.grid.max_x 
          or np[1] < 0 or np[1] > self.grid.max_y):
        break 
      hit_wall = False
      iii = 0
      while self.grid.get_pos(np) == '#':
        iii += 1
        if iii > 1:
          print("CORNER WALL AT", at)
        hit_wall = True
        # print('from', at, 'to', np, 'would collide', self.grid.get_pos(np))
        # would colide
        dir_index = (dir_index + 1) % 4
        np = gridutils.move_in_dir(at, dir=gridutils.DIRS4[dir_index])

      if not hit_wall:
        if self.would_loop(at, dir_index, extra=np):
          if self.doing_sample:
            print("ADD ONE AT", np)
          added.add(np)
          n_pos += 1
      at = np

    print("n_pos", n_pos, "size", len(added))
    return len(added)

  def would_loop(self, at, dir_index, extra):
    iter = 0
    vis = set()
    assert at != extra
    assert self.grid.get_pos(at) != '#'
    assert self.grid.get_pos(extra) != '#'
    while iter < self.max_loop:
      iter += 1
      sig = (at, dir_index)
      if sig in vis:
        return True
      vis.add(sig)
      np = gridutils.move_in_dir(at, dir=gridutils.DIRS4[dir_index])
      # if blocked ahead, turn right and check again.
      while (self.grid.get_pos(np) == '#' or np == extra):
        dir_index = (dir_index + 1) % 4
        np = gridutils.move_in_dir(at, dir=gridutils.DIRS4[dir_index])
      if (np[0] < 0 or np[0] > self.grid.max_x 
          or np[1] < 0 or np[1] > self.grid.max_y):
        return False
      at = np
    return True


day06.sample_test("""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""", expect1=41, expect2=6)


if __name__ == '__main__':
  # 731 too low
  # 1929 too high
  # 1833 too high
  # 1791 it did not like
  # 1790 it did not like
  day06.run_and_check('input.txt', expect1=5086, expect2=1700)
