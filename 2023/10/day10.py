#!/usr/bin/env python3
"AOC 2023: day 10"

from tools import aoc


N = 1
S = 2
E = 4
W = 8
START = 16

C_TO_PIPE = {
  '|': N | S,
  '-': W | E,
  'L': N | E,
  'J': N | W,
  '7': S | W,
  'F': S | E,
  'S': START,
  '.': 0,
}

PIPE_TO_C = {
  N | S: '|',
  W | E: '-',
  N | E: 'L',
  N | W: 'J',
  S | W: '7',
  S | E: 'F',
  0:     '.',
  START: 'S',
}


class day10(aoc.aoc):

  def __init__(self):
    super(day10, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = [[0]]
    self.start_x = -1
    self.start_y = -1
    self.max_x = 0
    self.max_y = 0
    self.map = {}

  def do_line(self, line):
    # called for each line of input
    pipes = [0]
    self.max_x = max(self.max_x, len(line))
    self.max_y += 1
    for ic in range(len(line)):
      c = line[ic]
      self.map[(ic+1, self.max_y)] = C_TO_PIPE[c]
      pipes.append(C_TO_PIPE[c])
      if c == 'S':
        self.start_x = ic + 1
        self.start_y = self.max_y
    pipes.append(0)
    self.grid.append(pipes)

  def post_load(self):
    # called after all input is read
    edge = [0] * (self.max_x + 2)
    self.grid[0] = edge
    self.grid.append(edge)
    # Calculate what the start cll should be.
    c = 0
    if self.map.get((self.start_x  , self.start_y-1), 0) & S:
      c |= N
    if self.map.get((self.start_x  , self.start_y+1), 0) & N:
      c |= S
    if self.map.get((self.start_x-1, self.start_y  ), 0) & E:
      c |= W
    if self.map.get((self.start_x+1, self.start_y  ), 0) & W:
      c |= E
    self.grid[self.start_y][self.start_x] = c
    self.map[(self.start_x, self.start_y)] = c

  def find_moves(self, x, y):
    starts = []
    c = self.map.get((x, y), 0)
    if c & N:
      starts.append((x,   y-1))
    if c & E:
      starts.append((x+1, y))
    if c & S:
      starts.append((x,   y+1))
    if c & W:
      starts.append((x-1, y))
    return starts

  def oprint_grid(self):
    for r in self.grid:
      print(r)

  def part1(self):
    print('===== Start part 1')

    self.print_grid(self.map)
    visited = {} 
    to_visit = [(self.start_x, self.start_y)]
    steps = 0
    while len(to_visit) > 0:
      # print("LOOP", visited) 
      to_visit = self.flood(visited, to_visit, steps)
      steps += 1
    return steps - 1

  def flood(self, visited, to_visit, steps):
    ret = set()
    if steps == 0:
      print('starts', to_visit)
    # print('steps', steps, to_visit)
    for cell in to_visit:
      dist = visited.get(cell) or -1
      # print('  cell', cell, 'dist', dist)
      if dist < 0:
        visited[cell] = steps
        # print('    visited[cell]', visited[cell], visited.get(cell))
        for nxt in self.find_moves(cell[0], cell[1]):
          # print("  NXT", nxt)
          if nxt not in visited:
            ret.add(nxt)
    return list(ret)

  def part2(self):
    print('===== Start part 2')
    self.map = self.double_grid()
    self.print_grid(self.map)

    # Find the loop
    loop_visited = {} 
    to_visit = [(self.start_x, self.start_y)]
    steps = 0
    while len(to_visit) > 0:
      # print("LOOP", loop_visited) 
      to_visit = self.flood(loop_visited, to_visit, steps)
      if steps < 2:
        print(' cur loop', loop_visited, 'to', to_visit)
      steps += 1

    print("==== done with loop")
    self.print_grid(self.map, visited=loop_visited)

    # flood fill from the outside edges
    to_visit = set()
    visited = set(loop_visited.keys())
    for x in range(1, self.max_x+1):
      if not self.map.get((x, 1)):
        to_visit.add((x, 1))
      if not self.map.get((x, self.max_y)):
        to_visit.add((x, self.max_y))
    for y in range(2, self.max_y):
      if not self.map.get((1, y)):
        to_visit.add((1, y))
      if not self.map.get((self.max_x, y)):
        to_visit.add((self.max_x, y))
    # self.print_grid(self.map, visited=visited, outside=to_visit)

    visited = set(loop_visited.keys())
    i = 0
    while len(to_visit) > 0:
      #if i < 3:
      #  print('to_visit', to_visit)
      to_visit = self.expand_outside(visited, to_visit)
    self.print_grid(self.map, visited=loop_visited, outside=visited)
    self.print_grid(self.map, visited=loop_visited, outside=visited, shrink=True)

    n_captured = 0
    for y in range(3, self.max_y-1, 2):
      for x in range(3, self.max_x-1, 2):
        cell = (x, y)
        if cell in loop_visited or cell in visited:
          continue 
        n_captured += 1
    return n_captured

  def expand_outside(self, visited, to_visit):
    ret = set()
    # print('steps', steps, to_visit)
    for cell in to_visit:
      visited.add(cell)
      for off in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        n_x = cell[0] + off[0]
        n_y = cell[1] + off[1]
        if n_x <= 0 or n_y <= 0:
          continue
        if n_x >= self.max_x or n_y >= self.max_y:
          continue
        nxt = (n_x, n_y)
        if nxt not in visited:
          ret.add(nxt)
    return list(ret)

  def double_grid(self):
    g2 = {}
    for y in range(1, self.max_y+1):
      for x in range(1, self.max_x+1):
        c = self.grid[y][x]
        g2[(2 * x - 1, 2 * y - 1)] = c
        if c & E and x < self.max_x:
          g2[(2 * x,     2 * y - 1)] = W|E
        if c & S and y < self.max_y:
          g2[(2 * x - 1, 2 * y    )] = N|S
        if x == self.start_x and y == self.start_y:
          # look ahead for S over up
          if self.grid[y+1][x]:
            g2[(2 * x - 1, 2 * y    )] = N|S
    self.start_x = 2 * self.start_x - 1
    self.start_y = 2 * self.start_y - 1
    self.max_x = self.max_x * 2 - 1
    self.max_y = self.max_y * 2 - 1
    return g2

  def print_grid(self, grid, visited={}, outside=set(), shrink=False):
    mx = 0
    my = 0
    inc = 2 if shrink else 1
    for cell in grid:
      mx = max(mx, cell[0])
      my = max(my, cell[1])
    for y in range(1, my+1, inc):
      line = []
      got_start = 0
      for x in range(1, mx+1, inc):
        if x == self.start_x and y == self.start_y:
          line.append('X')
          got_start = grid.get((x, y))
        elif (x, y) in visited:
          line.append('#')
        elif (x, y) in outside:
          line.append('O')
        else:
          line.append(PIPE_TO_C[grid.get((x, y)) or 0])
      suffix = ('X=%c' % PIPE_TO_C[got_start]) if got_start > 0 else ''
      print('%3d' % y, ''.join(line), suffix)


day10.sample_test("""
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""", expect1=8, expect2=1)

day10.sample_test("""
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""", expect1=80, expect2=10)


if __name__ == '__main__':
  day10.run_and_check('input.txt', expect1=7107, expect2=281)
