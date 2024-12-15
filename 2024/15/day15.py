#!/usr/bin/env python3
"AOC 2023: day 15"

import sys

from tools import aoc
from tools import gridutils

DIRS=gridutils.DIRS4

MOVE_DIR = {
    '^': DIRS[0],
    '>': DIRS[1],
    'v': DIRS[2],
    '<': DIRS[3],
}

REV_DIR = {
    '^': DIRS[2],
    'v': DIRS[0],
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
        # turn it back to free space
        self.grid.set(self.robot_x, self.robot_y, '.')
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
    for move in self.moves:
      pos = self.do_move(pos, move)
    self.grid.print()
    return self.lantern_gps()

  def do_move(self, pos, move):
    new_pos = gridutils.add_vector(pos, MOVE_DIR[move])
    c = self.grid.get_pos(new_pos)
    if c == '#':
      return pos
    if c == '.':
      return new_pos
    assert c == 'O'
    # find line of O to wall

    np = new_pos
    while True:
      np = gridutils.add_vector(np, MOVE_DIR[move])
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

  def double_map(self):
    self.robot_x *= 2
    ng = gridutils.Grid()
    for y in range(self.grid.max_y+1):
      for x in range(self.grid.max_x+1):
        c = self.grid.get(x, y)
        if c in ('#', '.'):
          ng.set(2*x, y, c)
          ng.set(2*x+1, y, c)
        elif c == 'O':
          ng.set(2*x, y, '[')
          ng.set(2*x+1, y, ']')
        else:
          print("WTF", x, y, c)
          sys.exit(1)
    self.grid = ng


  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.double_map()
    if self.doing_sample:
      self.grid.print()

    pos = (self.robot_x, self.robot_y)
    n = 0
    for move in self.moves:
      pos = self.do_move2(pos, move)
      n += 1
      #if n < 10 and self.doing_sample:
      #  print("====== Move", n)
      #  self.grid.set_pos(pos, '@')
      #  self.grid.print()
      #  self.grid.set_pos(pos, '.')
    self.grid.print()
    return self.lantern_gps()

  def do_move2(self, pos, move):
    new_pos = gridutils.add_vector(pos, MOVE_DIR[move])
    c = self.grid.get_pos(new_pos)
    if c == '#':
      return pos
    if c == '.':
      return new_pos
    if c not in ('[', ']'):
      print("WTF: not [] at", new_pos, c)
      return 0

    # left right are easy. probably can be combined with up
    # down, but doing this is practice
    if move in ('<', '>'):
      np = new_pos
      while True:
        np = gridutils.add_vector(np, MOVE_DIR[move])
        c = self.grid.get_pos(np)
        if c in ('[', ']'):
          continue
        if c == '#':
          return pos
        assert c == '.'

        # Found the gap, move them over
        x = new_pos[0]
        y = new_pos[1]
        assert y == np[1]
        nx = np[0]
        if nx > x:  # push right
          while nx > x:
            self.grid.set(nx, y, self.grid.get(nx-1, y))
            nx -= 1
        else:
          while nx < x:
            self.grid.set(nx, y, self.grid.get(nx+1, y))
            nx += 1
        # since the robot pushed the block out of the way
        # make it empty
        self.grid.set_pos(new_pos, '.')
        return new_pos

    # find up/down group of [] to wall 
    to_move = set()
    to_clear = set()
    heads = set([new_pos])
    c = self.grid.get_pos(new_pos)
    if c == '[':
      heads.add(gridutils.add_vector(new_pos, DIRS[1]))
    else:
      heads.add(gridutils.add_vector(new_pos, DIRS[3]))
    to_move = set(heads)
    to_clear = set(heads)
    while len(heads) > 0:
      new_heads = set()
      last_heads = set(heads)
      for head in heads:
        np = gridutils.add_vector(head, MOVE_DIR[move])
        c = self.grid.get_pos(np)
        if c == '#':
          return pos
        if c in ('[', ']'):
          # STACK EM
          new_heads.add(np)
          to_move.add(np)
          if c == '[':
            move_to_pos = gridutils.add_vector(np, DIRS[1])
            new_heads.add(move_to_pos)
            if move_to_pos not in to_move:
              to_clear.add(move_to_pos)
            to_move.add(move_to_pos)
            #clear_pos = gridutils.add_vector(move_to_pos, REV_DIR[move])
            #if clear_pos not in to_move and move_to_pos not in heads:
            #  to_clear.add(clear_pos)
          else:
            move_to_pos = gridutils.add_vector(np, DIRS[3])
            new_heads.add(move_to_pos)
            if move_to_pos not in to_move:
              to_clear.add(move_to_pos)
            to_move.add(move_to_pos)
            #clear_pos = gridutils.add_vector(move_to_pos, REV_DIR[move])
            #if clear_pos not in to_move and move_to_pos not in heads:
            #  to_clear.add(clear_pos)
        else:
          assert c == '.'
      if self.doing_sample:
        print("Heads from ", heads, 'to', new_heads,"moving", to_move, "clearing", to_clear)
      heads = new_heads
    if last_heads:
      if self.doing_sample:
        print("final heads at", last_heads, 'moving', to_move, 'clearing', to_clear)
        self.grid.set_pos(pos, '@')
        self.grid.print()
        self.grid.set_pos(pos, '.')
      if move == '^':
        # Move down from y
        for cell in sorted(to_move, key=lambda x: x[1], reverse=True):
          above = (cell[0], cell[1]-1)
          self.grid.set_pos(above, self.grid.get_pos(cell))
      else:
        for cell in sorted(to_move, key=lambda x: x[1]):
          below = (cell[0], cell[1]+1)
          self.grid.set_pos(below, self.grid.get_pos(cell))

      print("clearing", to_clear)
      for cell in to_clear:
        self.grid.set_pos(cell, '.')
      self.grid.set_pos(new_pos, '@')
      self.grid.print()
      self.grid.set_pos(new_pos, '.')

    return new_pos


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
""", expect1=10092, expect2=7)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=1487337, expect2=9021)
