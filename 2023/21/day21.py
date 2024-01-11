#!/usr/bin/env python3
"AOC 2023: day 21"

from tools import aoc
from tools import gridutils


class day21(aoc.aoc):

  def __init__(self):
    super(day21, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.map = gridutils.Grid()
    self.rocks = set()
    self.ncols = 0
    self.nrows = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    for x, c in enumerate(line):
      if c == '#':
        self.map.set(x, self.nrows, c)
        self.rocks.add((x,self.nrows))
      if c == 'S':
        self.start_x = x
        self.start_y = self.nrows
    self.nrows += 1
    self.ncols = max(self.ncols, x + 1)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.map.print()

    need_steps = 64
    if self.doing_sample:
      need_steps = 6

    visited = {(self.start_x, self.start_y): 0}
    for steps in range(1, need_steps+1):
      nv = {}
      for cur in visited:
        for disp in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
          pos = (cur[0] + disp[0], cur[1] + disp[1])
          if (pos[0] % self.ncols, pos[1] % self.nrows) not in self.rocks:
            nv[pos] = steps
      visited = nv

    ret = len([x for x in nv.values() if x == need_steps])
    return ret


  def part2(self):
    print('===== Start part 2')
    need_steps = 26501365
    if self.doing_sample:
      need_steps = 100
    all = {(self.start_x, self.start_y): 0}
    visited = {(self.start_x, self.start_y): 0}
    max_nv = 0
    for steps in range(1, need_steps+1):
      nv = {}
      max_nv = max(max_nv, len(visited))
      for cur, ns in visited.items():
        if ns < steps - self.ncols:
          continue
        for disp in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
          pos = (cur[0] + disp[0], cur[1] + disp[1])
          if (pos[0] % self.ncols, pos[1] % self.nrows) not in self.rocks:
            nv[pos] = steps
      visited = nv

    print("max_nv", max_nv)
    # ret = len([x for x in nv.values() if x == need_steps])
    ret = len(all)
    return ret


day21.sample_test("""
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""", expect1=16, expect2=6536+1)


if __name__ == '__main__':
  day21.run_and_check('input.txt', expect1=3594, expect2=None)
