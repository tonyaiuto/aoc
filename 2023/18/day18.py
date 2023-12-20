#!/usr/bin/env python3
"AOC 2023: day 18"

from collections import defaultdict

from tools import aoc
from tools import gridutils

C2DIR = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

class Dig(object):

  def __init__(self, s):
    self.raw = s
    #"R 6 (#70c710)"
    p = s.split(' ')
    self.dir = p[0]
    self.dist = int(p[1])
    self.color = p[2][2:-1]
    self.dist2 = int(self.color[0:5], 16)
    self.dir2 = C2DIR[self.color[5]]

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return '%c %d %s %c %d' % (self.dir, self.dist, self.color, self.dir2, self.dist2)

  def dig(self, grid, x, y):
    for i in range(self.dist):
      x, y = self._move(self.dir, x, y)
      grid.set(x, y, self.color)
    return x, y

  def dig2(self, grid, x, y):
    for i in range(self.dist2):
      x, y = self._move(self.dir2, x, y)
      grid.set(x, y, self.color)
    return x, y

  def _move(self, dir, x, y):
    if dir == 'R':
      x = x + 1
    elif dir == 'L':
      x = x - 1
    elif dir == 'U':
      y = y - 1
    elif dir == 'D':
      y = y + 1
    return x, y


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
    self.digs = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    dig = Dig(line)
    if self.doing_sample:
      print(dig)
    self.digs.append(dig)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')

    grid = gridutils.Grid(default_cell=None)
    x = 0
    y = 0
    for dig in self.digs:
      if self.doing_sample:
        print("=== Digging", dig)
      x, y = dig.dig(grid, x, y)
    if self.doing_sample:
      print_grid(grid)
    edge_size = len(grid.live_cells())
    #filled = fill_grid_flood(grid)
    #filled_size = len(filled)
    filled = fill_grid3(grid)
    print('edge', edge_size, 'filled', filled)
    return filled


  def part2(self):
    print('===== Start part 2')
    grid = gridutils.Grid(default_cell=None)
    x = 0
    y = 0
    for dig in self.digs:
      if self.doing_sample:
        print("=== Digging", dig)
      x, y = dig.dig2(grid, x, y)

    edge_size = len(grid.live_cells())
    print('edge', edge_size)
    filled = fill_grid3(grid)
    print('edge', edge_size, 'filled', filled)
    print("too high by ", filled - 952408144115)
    return filled


def print_grid(grid):
  for y in range(grid.min_y, grid.max_y+1):
    out = []
    for x in range(grid.min_x, grid.max_x+1):
      cell = grid.get(x, y)
      out.append('#' if cell else '.')
    print(''.join(out))

def fill_grid_flood(grid):
  visited = set()
  x = 1
  y = 1
  frontier = set([(x, y)]) 

  while len(frontier) > 0:
    # print("LOOP n_frontiers=", len(frontier))
    nf = set()
    for pos in frontier:
      x = pos[0]
      y = pos[1]
      cell = grid.get(x, y)
      if cell:
        continue
      if (x, y) in visited:
        continue
      visited.add((x,y))
      for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + offset[0]
        ny = y + offset[1]
        if (nx, ny) not in visited:
          nf.add((nx, ny))
    frontier = nf
  return visited


def fill_grid2(grid):
  ret = 0
  for y in range(grid.min_y, grid.max_y+1):
    row_n = 0
    last_cell_edge = False
    count_it = False
    for x in range(grid.min_x, grid.max_x+1):
      cell = grid.get(x, y)
      if cell:
        row_n += 1
        if not last_cell_edge:
          count_it = not count_it
        last_cell_edge = True
      else:
        if count_it:
          row_n += 1
        last_cell_edge = False
    # print('row_n', row_n)
    ret += row_n
  return ret


def fill_grid3(grid):
  rows = defaultdict(list)
  for cell in grid.live_cells():
    x = cell[0]
    y = cell[1]
    rows[y].append(x)

  ret = 0
  for y in range(grid.min_y, grid.max_y+1):
    xs = sorted(rows[y])
    row_n = 0
    count_gap = False
    inside = False
    next_inside = True
    edge_span = 0
    x = -1000000
    for cell_x in xs:
      # . . 3 4 . 6 . 8 . => 5
      # . . 3 . . 6 . 8 9 => 6
      # . . 3 . . 6 . 8 9 10 . => 7
      # . . 3 4 . 6 7 . 9 10 . => 7

      #print('x=%d, cnt=%d, inside=%s, nxt=%s, in_edge=%s' % (
      #       cell_x, row_n, inside, next_inside, in_edge))
      row_n += 1  # count the edge part
      gap = (cell_x - x - 1)
      if gap > 0:
        if count_gap:
          row_n += gap
        count_gap = not count_gap
      x = cell_x

    if abs(y) < 10:
      print('row', y, xs, '  row_n', row_n)
    ret += row_n
  return ret

day18.sample_test("""
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""", expect1=62, expect2=952408144115)


if __name__ == '__main__':
  day18.run_and_check('input.txt', expect1=48652, expect2=None)
