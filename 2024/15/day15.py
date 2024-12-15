#!/usr/bin/env python3
"AOC 2023: day 15"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

DIRS=gridutils.DIRS4

move_dir = {
    '^': DIRS[0],
    '>': DIRS[1],
    'v': DIRS[2],
    '<': DIRS[3],
}


class day15(aoc.aoc):

  def __init__(self):
    super(day15, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid()
    self.in_grid = True
    self.moves = ''

  def do_line(self, line):
    if not line:
      self.in_grid = False
      return

    if self.in_grid:
      self.grid.add_row(line)
      if '@' in line:
        self.robot_x = line.find('@')
        self.robot_y = self.grid.height
    else:
      self.moves = self.moves + line

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.doing_sample:
      self.grid.print()
      print(self.moves)
      print(self.robot_x, self.robot_y)

    pos = (self.robot_x, self.robot_y)
    self.grid.set_pos(pos, '.')
    for move in self.moves:
      pos = self.do_move(pos, move)
    self.grid.print()
    return self.lantern_gps()

  def do_move(self, pos, move):
    new_pos = gridutils.add_vector(pos, move_dir[move])
    c = self.grid.get_pos(new_pos)
    if c == '#':
      return pos
    if c == '.':
      return new_pos
    assert c == 'O'
    # find line of O to wall

    np = new_pos
    while True:
      np = gridutils.add_vector(np, move_dir[move])
      c = self.grid.get_pos(np)
      if c == 'O':
        continue
      if c == '#':
        return pos
      assert c == '.'
      self.grid.set_pos(new_pos, '.')
      self.grid.set_pos(np, 'O')
      return new_pos

  def lantern_gps(self):
    ret = 0
    for pos in self.grid.live_cells():
      if self.grid.get_pos(pos) == 'O':
        ret += 100 * pos[1] + pos[0]
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day15.sample_test("""
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""", expect1=10092, expect2=None)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=1487337, expect2=9021)
