#!/usr/bin/env python3
"AOC 2023: day 10"

from tools import aoc
from tools import gridutils

DIRS=gridutils.DIRS4


def add_vector(a, v):
  return (a[0]+v[0], a[1]+v[1])


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
    self.grid = gridutils.Grid()
    self.high = gridutils.Grid()
    self.heads = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.high.add_row([int(c) for c in line])
    self.grid.add_row(line)
    for x, c in enumerate(line):
      if c == '0':
        self.heads.append((x, self.grid.height))

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      self.grid.print(show_row_numbers=True)
      print(self.heads)


  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for start in self.heads:
      score = self.score_trail(start)
      ret += score
    return ret

  def score_trail(self, start):
    score = self.next_steps([start], 1)
    if self.doing_sample:
      print('score', start, score)
    return score

  def next_steps(self, frontier, want):
    new_f = set()
    for pos in frontier:
      for d in DIRS:
        neighbor = add_vector(pos, d)
        if self.high.get_pos(neighbor) == want:
          new_f.add(neighbor)
    if want == 9:
      return len(new_f)
    else:
      return self.next_steps(new_f, want+1)
        

  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for start in self.heads:
      score = self.score_trail2(start)
      ret += score
    return ret

  def score_trail2(self, start):
    score = self.find_paths([[start]], 1)
    if self.doing_sample:
      print('score2', start, score)
    return score

  def find_paths(self, frontier, want):
    for want in range(1, 10):
      new_f = list()
      for path in frontier:
        head = path[-1]
        for d in DIRS:
          neighbor = add_vector(head, d)
          if self.high.get_pos(neighbor) == want:
            new_f.append(path + [neighbor])
            if self.doing_sample:
              print('   path', path + [neighbor])
      frontier = new_f
    return len(frontier)


day10.sample_test("""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""", expect1=36, expect2=81)


if __name__ == '__main__':
  day10.run_and_check('input.txt', expect1=593, expect2=1192)
