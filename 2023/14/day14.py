#!/usr/bin/env python3
"AOC 2023: day 14"

from tools import aoc
from tools import gridutils


class day14(aoc.aoc):

  def __init__(self):
    super(day14, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.map = gridutils.Grid()
    self.n_rows = 0

  def do_line(self, line):
    # called for each line of input
    for ic, c in enumerate(line):
      if c in ('O', '#'):
        self.map.set(ic, self.n_rows, c)
    self.n_rows += 1

  def tilt(self, dir):
    # Dir N=0, E=1, S=2, W=3
    pass

  def tilt_north(self):
    for x in range(self.map.max_x+1):
      edge = -1
      for y in range(self.map.max_y+1):
        c = self.map.get(x, y)
        if c == '#':
          edge = y
        elif c == 'O':
          edge = edge + 1
          if y != edge:
            self.map.unset(x, y)
            self.map.set(x, edge, c)

  def tilt_south(self):
    for x in range(self.map.max_x+1):
      edge = self.map.max_y + 1
      for y in range(self.map.max_y, -1, -1):
        c = self.map.get(x, y)
        if c == '#':
          edge = y
        elif c == 'O':
          edge = edge - 1
          if y != edge:
            self.map.unset(x, y)
            self.map.set(x, edge, c)

  def tilt_west(self):
    for y in range(self.map.max_y+1):
      edge = -1
      for x in range(self.map.max_x+1):
        c = self.map.get(x, y)
        if c == '#':
          edge = x
        elif c == 'O':
          edge = edge + 1
          if x != edge:
            self.map.unset(x, y)
            self.map.set(edge, y, c)

  def tilt_east(self):
    sig = []  # signature of the board as a side effect
    for y in range(self.map.max_y+1):
      edge = self.map.max_x + 1
      for x in range(self.map.max_x, -1, -1):
        c = self.map.get(x, y)
        if c == '#':
          edge = x
        elif c == 'O':
          edge = edge - 1
          if x != edge:
            self.map.unset(x, y)
            self.map.set(edge, y, c)
          sig.append(102*y+x)  # cheating, I know the input width
    return ','.join([str(x) for x in sig])

  def compute_load(self):
    ret = 0
    for x in range(self.map.max_x+1):
      load = self.map.max_y + 1
      for y in range(self.map.max_y+1):
        c = self.map.get(x, y)
        if c == 'O':
          # print('O at', x, y, 'load', load)
          ret += load
        load -= 1
    return ret

  def part1(self):
    print('===== Start part 1')
    self.tilt_north()
    # self.map.print()
    ret = self.compute_load()
    print("part1", ret)
    return ret

  def part2(self):
    print('===== Start part 2')

    sigs_cycle = {}
    need_cycles = 1000000000
    loop = 0
    ld = 0
    cycle_len = 0
    while loop < need_cycles:
      loop += 1
      # print('loop', loop)
      self.tilt_north()
      self.tilt_west()
      self.tilt_south()
      sig = self.tilt_east()
      # self.map.print()
      if cycle_len == 0:
        prev = sigs_cycle.get(sig)
        sigs_cycle[sig] = loop
        if prev:
          cycle_len = loop - prev
          print("repeat at", prev, loop, 'cycle len', cycle_len)
          if cycle_len > 0:
            fake_loops = ((need_cycles - loop) // cycle_len) - 1
            loop += fake_loops * cycle_len

    ret = self.compute_load()
    print("part2", ret)
    return ret

day14.sample_test("""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""", expect1=136, expect2=64)


if __name__ == '__main__':
  day14.run_and_check('input.txt', expect1=109654, expect2=94876)
