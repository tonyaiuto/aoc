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
    gp = line.find('^')
    if gp >= 0:
      self.guard_start = (gp, self.grid.height)
      print('guard at', self.guard_start, self.grid.get_pos(self.guard_start))
      self.grid.set(gp, self.grid.height, ' ')
    pass

  def post_load(self):
    # called after all input is read
    # self.grid.print()
    pass


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

    return 42


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
  day06.run_and_check('input.txt', expect1=5086, expect2=None)
