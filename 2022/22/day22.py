#!/usr/bin/env python3
"AOC 2021: day 22"

from collections import defaultdict
import copy
import itertools

from tools import aoc
from tools import gridutils


XDISP=[0, 1, 0, -1] 
YDISP=[-1, 0, 1, 0] 

class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day22(aoc.aoc):

  def __init__(self):
    super(day22, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': False,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    self.grid = gridutils.Grid()
    for row in self.all_input[0]:
      self.grid.add_row(row)
    if self.trace_sample:
      self.grid.print()

    self.start_y = 0
    for x in range(self.grid.max_x):
      if self.grid.get(x, 0) == '.':
        self.start_x = x
        break
    if self.trace_sample:
      print('start at', self.start_x, self.start_y)
    self.x = self.start_x
    self.y = self.start_y
    #  0
    # 3 1
    #  2
    self.dir = 1

    self.path = []
    n = 0
    rule = self.all_input[1][0]
    for c in rule:
      if c in ('L', 'R'):
        self.path.append(n)
        self.path.append(c)
        n = 0
      else:
        n = n * 10 + ord(c) - ord('0')
    self.path.append(n)
    if self.trace_sample:
      print('Path:', self.path)
    self.path_i = 0

    self.box_2_face = []
    self.cell_size = int(self.all_input[2][0])
    for box_row in self.all_input[2][1:]:
      self.box_2_face.append([int(x) for x in box_row.split(' ')])
    print('Box to face:', self.cell_size, 'X', self.box_2_face)

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.grid.set(self.x, self.y, 'v')
    for i in range(len(self.path)):
      self.move()
      if self.trace_sample:
        self.grid.set(self.x, self.y, 'v')
        self.grid.print(show_row_numbers=True)

    print(self.x, self.y, self.dir)
    return 1000 * (self.y + 1) + 4 * (self.x + 1) + (self.dir - 1) % 4

  def move(self):
    fx = self.x
    fy = self.y
    what = self.path[self.path_i]
    if self.trace_sample:
      print('path[%d]: %s' % (self.path_i, str(what)))
    self.path_i += 1
    if what == 'L':
      self.dir = (self.dir - 1) % 4
      return
    if what == 'R':
      self.dir = (self.dir + 1) % 4
      return

    for move_i in range(what):
      nx = self.x + XDISP[self.dir]
      ny = self.y + YDISP[self.dir]
      next_cell = self.grid.get(nx, ny)
      if next_cell == '#':
        if self.trace_sample:
          print('Move from', fx, fy, 'to', self.x, self.y)
        return
      if next_cell in ('.', 'v'):
        self.x = nx
        self.y = ny
        continue
      if next_cell != ' ':
        print("WTF", nx, ny, next_cell)
        assert next_cell == 42

      # wrap it
      if dir == 0 or dir == 2:
        max_scan = self.grid.max_y
      else:
        max_scan = self.grid.max_x
      # print('start wrap', nx, ny, '(%s)' % next_cell)
      for s in range(max_scan):
        nx = (nx + XDISP[self.dir]) % (self.grid.max_x + 1)
        ny = (ny + YDISP[self.dir]) % (self.grid.max_y + 1)
        next_cell = self.grid.get(nx, ny)
        # print('Try wrap', nx, ny, '(%s)' % next_cell)
        if next_cell == ' ':
          continue
        if next_cell == '#':
          if self.trace_sample:
            print('Move from', fx, fy, 'to', self.x, self.y)
          return
        if next_cell in ('.', 'v'):
          if self.trace_sample:
            print("Wrap dir", self.dir, 'from', self.x, self.y, 'to', nx, ny) 
          self.x = nx
          self.y = ny
          break
        print("Wrap FAIL", 'c=(%s)'%next_cell, 'dir', self.dir, 'from', self.x, self.y, 'to', nx, ny) 
    # done

  def part2(self):
    print('===== Start part 2')
    self.reset()

    self.path_i = 0

    self.cell_rot = [
      [0],
    ]

    self.grid.set(self.x, self.y, 'v')
    # for i in range(len(self.path)):
    for i in range(20):
      self.move2()
      if self.trace_sample:
        self.grid.set(self.x, self.y, 'v')
        self.grid.print(show_row_numbers=True)

    print(self.x, self.y, self.dir)
    return 1000 * (self.y + 1) + 4 * (self.x + 1) + (self.dir - 1) % 4


  def move2(self):
    fx = self.x
    fy = self.y
    what = self.path[self.path_i]
    if self.trace_sample:
      print('path[%d]: %s' % (self.path_i, str(what)))

    self.path_i += 1
    if what == 'L':
      self.dir = (self.dir - 1) % 4
      return
    if what == 'R':
      self.dir = (self.dir + 1) % 4
      return

    for move_i in range(what):
      nx = self.x + XDISP[self.dir]
      ny = self.y + YDISP[self.dir]
      next_cell = self.grid.get(nx, ny)
      if next_cell == '#':
        if self.trace_sample:
          print('Move from', fx, fy, 'to', self.x, self.y)
        return
      if next_cell in ('.', 'v'):
        self.x = nx
        self.y = ny
        continue
      if next_cell != ' ':
        print("WTF", nx, ny, next_cell)
        assert next_cell == 42

      # What CELL am I in

      # wrap it
      if dir == 0 or dir == 2:
        max_scan = self.grid.max_y
      else:
        max_scan = self.grid.max_x
      # print('start wrap', nx, ny, '(%s)' % next_cell)
      for s in range(max_scan):
        nx = (nx + XDISP[self.dir]) % (self.grid.max_x + 1)
        ny = (ny + YDISP[self.dir]) % (self.grid.max_y + 1)
        next_cell = self.grid.get(nx, ny)
        # print('Try wrap', nx, ny, '(%s)' % next_cell)
        if next_cell == ' ':
          continue
        if next_cell == '#':
          if self.trace_sample:
            print('Move from', fx, fy, 'to', self.x, self.y)
          return
        if next_cell in ('.', 'v'):
          if self.trace_sample:
            print("Wrap dir", self.dir, 'from', self.x, self.y, 'to', nx, ny) 
          self.x = nx
          self.y = ny
          break
        print("Wrap FAIL", 'c=(%s)'%next_cell, 'dir', self.dir, 'from', self.x, self.y, 'to', nx, ny) 
    # done

#0123456789 1
day22.sample_test("""
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5

4
0 0 1 0
2 3 4 0
0 0 5 6
""", expect1=6032, expect2=None)


if __name__ == '__main__':
  # too high: 127118
  day22.run_and_check('input.txt', expect1=67390, expect2=None)
