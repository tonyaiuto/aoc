#!/usr/bin/env python3
"AOC 2023: day 20"

from collections import defaultdict

from tools import aoc
from tools import gridutils

DIRS = gridutils.DIRS4


class day20(aoc.aoc):

  def __init__(self):
    super(day20, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid(ignore='.')

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    self.grid.add_row(line)
    s_pos = line.find('S')
    if s_pos >= 0:
      self.start = (s_pos, self.grid.max_y)
      self.grid.set_pos(self.start, '.')
    e_pos = line.find('E')
    if e_pos >= 0:
      self.end = (e_pos, self.grid.max_y)
      self.grid.set_pos(self.end, '.')

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      self.grid.print()
      print("start/end at", self.start, self.end)

  def compute_distance_to_ends(self):
    self.dist = {}
    dist = 0
    pos = self.end
    self.dist[self.end] = 0
    while pos != self.start:
      dist += 1
      for mv in DIRS:
        np = gridutils.add_vector(pos, mv)
        if self.grid.get_pos(np) != '#' and np not in self.dist:
          pos = np
          self.dist[pos] = dist
          break
    # print(self.dist)

  def is_cheat_ok(self, pos, cur_dist, timing):
    ret = None
    assert self.grid.get_pos(pos) == '#'
    for mv in DIRS:
      np = gridutils.add_vector(pos, mv)
      if self.grid.get_pos(np) != '#':
        if self.dist[np] < cur_dist - timing:
          assert not ret
          ret = np
    return ret

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.compute_distance_to_ends()
    pos = self.start
    self.cheats = defaultdict(int)
    while pos != self.end:
      for mv in DIRS:
        np = gridutils.add_vector(pos, mv)
        if np[0] <= 0 or np[0] >= self.grid.max_x:
          continue
        if np[1] <= 0 or np[1] >= self.grid.max_y:
          continue
        if self.grid.get_pos(np) == '#':
          cur_dist = self.dist[pos]
          to_pos = self.is_cheat_ok(np, cur_dist, timing=2)
          if to_pos:
            savings = self.dist[pos] - self.dist[to_pos] - 2
            # print("Cheat at", pos, to_pos, savings)
            self.cheats[savings] += 1
        else:
          if self.dist[np] < self.dist[pos]:
            next_pos = np
      pos = next_pos

    return self.do_cheat_counts()

  def do_cheat_counts(self):
    min_ok = 100
    if self.doing_sample:
      min_ok = 36
      for savings in sorted(self.cheats):
        print(savings, self.cheats[savings])
    ret = 0
    for savings in self.cheats:
      if savings >= min_ok:
        ret += self.cheats[savings]
    return ret

  def manhattan_dist_cells(self, pos):
    max_d = 20
    for m_dist in range(2, max_d+1):
      for x_d in range(-m_dist, m_dist+1):
        x = pos[0] + x_d
        if x <= 0 or x >= self.grid.max_x:
          continue
        y_bound = max_d - abs(x)
        for y_d in range(-y_bound, y_bound+1):
          y = pos[1] + y_d
          if y <= 0 or y >= self.grid.max_y:
            continue
          if self.grid.get_pos((x, y)) == '#':
            continue
          yield((x, y))


  def part2(self):
    print('===== Start part 2')
    self.reset()

    self.compute_distance_to_ends()
    pos = self.start
    self.cheats = defaultdict(int)
    self.cheat_ends = set()
    # print('max', self.grid.max_x, self.grid.max_y)
    min_cheat = 100
    if self.doing_sample:
      min_cheat = 36
    while pos != self.end:
      cur_dist = self.dist[pos]
      for jump_pos in self.manhattan_dist_cells(pos):
        #if self.grid.get_pos(jump_pos) == '#':
        #  continue
        dist = abs(jump_pos[0] - pos[0]) + abs(jump_pos[1] - pos[1])
        savings = self.dist[pos] - self.dist[jump_pos] - dist
        if savings >= min_cheat:
          # print("Cheat at", pos, jump_pos, savings)
          ends = (pos, jump_pos)
          if ends not in self.cheat_ends:
            self.cheats[savings] += 1
          self.cheat_ends.add(ends)

      for mv in DIRS:
        np = gridutils.add_vector(pos, mv)
        if np in self.dist and self.dist[np] < self.dist[pos]:
            pos = np
            break
    return self.do_cheat_counts()


day20.sample_test("""
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""", expect1=4, expect2=701)


if __name__ == '__main__':
  # 74436 low
  day20.run_and_check('input.txt', expect1=1459, expect2=None)
