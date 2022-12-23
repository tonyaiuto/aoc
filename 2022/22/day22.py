#!/usr/bin/env python3
"AOC 2021: day 22"

from collections import defaultdict
import copy
import itertools

from tools import aoc
from tools import gridutils


XDISP=[0, 1, 0, -1] 
YDISP=[-1, 0, 1, 0] 

#  0
# 3 1
#  2
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

dir_to_name = ["UP", "RIGHT", "DOWN", "LEFT"]
dir_to_marker = ["^", ">", "v", "<"]

def print_fr(rot):
  for face in range(1, 7):
    rf = rot[face]
    for dir in rf:
      nf, nd = rf[dir]
      print('face', face, dir_to_name[dir], nf, dir_to_name[nd])
      

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
    self.face_2_box = {}
    for box_row in self.all_input[2][1:]:
      faces =[int(x) for x in box_row.split(' ')]
      for i in range(len(faces)):
        if faces[i] != 0:
          self.face_2_box[faces[i]] = (i, len(self.box_2_face))
      self.box_2_face.append(faces)

    print('Box to face:', self.cell_size, 'X', self.box_2_face)
    print('Face to box:', self.face_2_box)

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.trace_sample = False
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
      print('path[%d]:' % self.path_i, what)
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

    # face => dir => (face, ...)
    self.face_rot = {
        1: {
            DIR_RIGHT: (6, DIR_LEFT),
            DIR_LEFT: (3, DIR_DOWN),
            DIR_UP: (2, DIR_DOWN),
          },
        2: {
            DIR_UP: (1, DIR_DOWN),
            DIR_LEFT: (6, DIR_UP),
            DIR_DOWN: (5, DIR_UP),
          },
        3: {
            DIR_UP: (1, DIR_RIGHT),
            DIR_DOWN: (5, DIR_RIGHT),
          },
        4: {
            DIR_RIGHT: (6, DIR_DOWN),
          },
        5: {
            DIR_DOWN: (2, DIR_UP),
            DIR_LEFT: (3, DIR_UP),
          },
        6: {
            DIR_UP: (4, DIR_LEFT),
            DIR_RIGHT: (1, DIR_LEFT),
            DIR_DOWN: (2, DIR_RIGHT),
          },
      }
    if self.cell_size > 20:
      # 0 1 2
      # 0 3 0
      # 4 5 0
      # 6 0 0
      self.face_rot = {
        1: {
            DIR_LEFT: (4, DIR_RIGHT),
            DIR_UP: (6, DIR_RIGHT),
          },
        2: {
            DIR_DOWN: (3, DIR_LEFT),
            DIR_RIGHT: (5, DIR_LEFT),
            DIR_UP: (6, DIR_UP),
          },
        3: {
            DIR_LEFT: (4, DIR_DOWN),
            DIR_RIGHT: (2, DIR_UP),
          },
        4: {
            DIR_UP: (3, DIR_RIGHT),
            DIR_LEFT: (1, DIR_RIGHT),
          },
        5: {
            DIR_RIGHT: (2, DIR_LEFT),
            DIR_DOWN: (6, DIR_LEFT),
          },
        6: {
            DIR_RIGHT: (5, DIR_UP),
            DIR_LEFT: (1, DIR_DOWN),
            DIR_DOWN: (2, DIR_DOWN),
          },
        }
    # print_fr(self.face_rot)

    self.grid.set(self.x, self.y, 'v')
    # for i in range(min(20, len(self.path))):
    for i in range(len(self.path)):
      self.move2()
      if self.trace_sample:
        self.grid.print(show_row_numbers=True)

    print('FINAL', self.x, self.y, self.dir)
    return 1000 * (self.y + 1) + 4 * (self.x + 1) + (self.dir - 1) % 4


  def move2(self):
    fx = self.x
    fy = self.y
    what = self.path[self.path_i]
    if self.trace_sample:
      print('path[%d]:' % self.path_i, what)
    self.path_i += 1
    if what == 'L':
      self.dir = (self.dir - 1) % 4
      self.grid.set(self.x, self.y, dir_to_marker[self.dir])
      return
    if what == 'R':
      self.dir = (self.dir + 1) % 4
      self.grid.set(self.x, self.y, dir_to_marker[self.dir])
      return

    for move_i in range(what):
      nx = self.x + XDISP[self.dir]
      ny = self.y + YDISP[self.dir]
      next_cell = self.grid.get(nx, ny)
      if next_cell == '#':
        if self.trace_sample:
          self.grid.set(self.x, self.y, '@')
          print('Move from', fx, fy, 'to', self.x, self.y)
        return
      #if next_cell in ('.', 'v', '@'):
      if next_cell != ' ':
        self.x = nx
        self.y = ny
        self.grid.set(self.x, self.y, dir_to_marker[self.dir])
        continue
      if next_cell != ' ':
        print("WTF2", nx, ny, next_cell)
        assert next_cell == 42

      # What CELL am I in
      face = self.box_2_face[self.y // self.cell_size][self.x // self.cell_size]
      rel_x = self.x % self.cell_size
      rel_y = self.y % self.cell_size
      if not face in self.face_rot:
        print('Missing face walk_off for', face, dir_to_name[self.dir])
        print("face rot", self.face_rot)
        print_fr(self.face_rot)
      new_face, new_dir = self.face_rot[face][self.dir]
      nx, ny = self.new_pos(face, new_face=new_face, new_dir=new_dir, relx=rel_x, rely=rel_y)

      if self.trace_sample:
        print('walk off face', face, 'at', rel_x, rel_y,
              'to face', new_face, dir_to_name[new_dir],
              'landing at', nx, ny)
      next_cell = self.grid.get(nx, ny)
      if next_cell == '#':
        if self.trace_sample:
          print("  => blocked")
        return
      self.x = nx
      self.y = ny
      self.dir = new_dir
      self.grid.set(self.x, self.y, 'o')
    # done

  def new_pos(self, old_face, new_face, new_dir, relx, rely):
    CLOCKWISE = (self.dir + 1) % 4 == new_dir
    ANTICLOCK = (new_dir + 1) % 4 == self.dir
    SAME = (self.dir + new_dir) % 2 == 0

    if new_dir in (DIR_DOWN, DIR_UP):
      if SAME:
        if self.dir == new_dir:
          retx = relx
        else:
          retx = self.cell_size - 1 - relx
      elif CLOCKWISE:
        retx = self.cell_size - 1 - rely
      elif ANTICLOCK:
        retx = rely
      if new_dir == DIR_DOWN:
        rety = 0
      else:
        rety = self.cell_size - 1
    elif new_dir in (DIR_LEFT, DIR_RIGHT):
      if SAME:
        if self.dir == new_dir:
          rety = rely
        else:
          rety = self.cell_size - 1 - rely
      elif CLOCKWISE:
        rety = relx
      elif ANTICLOCK:
        rety = self.cell_size - 1 - relx
      if new_dir == DIR_RIGHT:
        retx = 0
      else:
        retx = self.cell_size - 1
    else:
      print("wonky new dir", new_dir)
      return None

    box_x, box_y = self.face_2_box[new_face]
    # print('box at', box_x, box_y, 'relxy', retx, rety)
    return (box_x * self.cell_size + retx),  (box_y * self.cell_size + rety)


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
""", expect1=6032, expect2=5031)


if __name__ == '__main__':
  # too high: 127118
  # part2: 52368 is wrong, because it is the folding from sample
  # 87260
  # 87321 Low
  day22.run_and_check('input.txt', expect1=67390, expect2=95291)
