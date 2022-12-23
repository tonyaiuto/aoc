#!/usr/bin/env python3
"AOC 2021: day 23"

from collections import defaultdict

from tools import aoc
from tools import gridutils


class day23(aoc.aoc):

  def __init__(self):
    super(day23, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid(ignore='.')
    self.round = 0

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)

  def post_load(self):
    # called after all input is read
    if self.trace_sample:
      self.grid.print()
    # print(self.grid.live_cells())

  def elf_at(self, x, y, deltas):
    for dx, dy in deltas:
      if self.grid.get(x+dx, y+dy) == '#':
        return True
    return False

  def part1(self):
    print('===== Start part 1')
    for i in range(10):
      _ = self.do_round()
      if self.trace_sample:
        print("== End round", self.round)
        self.grid.print(show_row_numbers=True)
    return self.count_empty()

  def count_empty(self):
    min_x = 1000
    max_x = -1000
    min_y = 1000
    max_y = -1000
    live = 0
    for ex, ey in self.grid.live_cells():
      live += 1
      min_x = min(min_x, ex)
      max_x = max(max_x, ex)
      min_y = min(min_y, ey)
      max_y = max(max_y, ey)
    return (max_x-min_x+1) * (max_y-min_y+1) - live

  def do_round(self):
    moves = {}
    dest_count = defaultdict(int) 
    anyone_has_neighbors = False
    for elf in self.grid.live_cells():
      mv, has_neighbors = self.first_valid(elf)
      anyone_has_neighbors = anyone_has_neighbors or has_neighbors
      if mv:
        if self.trace_sample:
          print('elf at', elf, 'moves', mv)
        moves[elf] = mv
        dest_count[mv] += 1
    for elf, mv in moves.items():
      if dest_count[mv] == 1:
        if self.trace_sample:
          print('elf at', elf, 'moves to', mv)
        self.grid.unset(elf[0], elf[1])
        self.grid.set(mv[0], mv[1], '#')
      else:
        if self.trace_sample:
          print('elf at', elf, 'blocked from', mv)
    self.round += 1 
    return anyone_has_neighbors
 

  def first_valid(self, pos):
    x = pos[0]
    y = pos[1]
    offset = self.round % 4
  
    ret = []
    for i in range(4):
      sel = (i + offset) % 4
      if sel == 0 and not self.elf_at(x, y, [(-1, -1), (0, -1), (1, -1)]):
        ret.append((x, y-1))
      if sel == 1 and not self.elf_at(x, y, [(-1, 1), (0, 1), (1, 1)]):
        ret.append((x, y+1))
      if sel == 2 and not self.elf_at(x, y, [(-1, -1), (-1, 0), (-1, 1)]):
        ret.append((x-1, y))
      if sel == 3 and not self.elf_at(x, y, [(1, -1), (1, 0), (1, 1)]):
        ret.append((x+1, y))
    if len(ret) == 4:
      return None, False
    if len(ret) == 0:
      return None, True
    return ret[0], True

  def part2(self):
    print('===== Start part 2')
    while True:
      anyone_has_neighbors = self.do_round()
      if self.trace_sample:
        print("== End round", self.round)
        self.grid.print(show_row_numbers=True)
      if not anyone_has_neighbors:
        break
    return self.round


day23.sample_test("""
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""", expect1=110, expect2=20)


if __name__ == '__main__':
  day23.run_and_check('input.txt', expect1=3689, expect2=965)
