"AOC 2021: day 05"

from collections import defaultdict
import math

from tools import aoc
from tools import qparser as qp


class Vent(object):

  def __init__(self):
    pass

  def __str__(self):
    return '%d,%d -> %d,%d' % (self.x1, self.y1, self.x2, self.y2)


class day05(aoc.aoc):

  def __init__(self):
    super(day05, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.parser = qp.QParser([
        qp.Number('x1'),
        qp.Literal(','),
        qp.Number('y1'),
        qp.Literal('->'),
        qp.Number('x2'),
        qp.Literal(','),
        qp.Number('y2'),
    ])
    self.vents = []

  def do_line(self, line):
    # called for each line of input
    vent = Vent()
    self.parser.parse(vent, line)
    # print(vent.y2)
    self.vents.append(vent)

  def post_load(self):
    # called after all input is read
    dim = 0
    for v in self.vents:
      dim = max(dim, v.x1, v.y1, v.x2, v.y2)
    self.dim = dim + 1

  def pgrid(self, g):
    print('---')
    for row in range(self.dim):
      print(g[row])

  def count_over(self, g, n):
    ret = 0
    for y in range(self.dim):
      for x in range(self.dim):
        if g[y][x] >= n:
          ret += 1
    return ret

  @staticmethod
  def fillx(grid, y, x1, x2):
    for x in aoc.visit_range(x1, x2):
      grid[y][x] += 1

  @staticmethod
  def filly(grid, x, y1, y2):
    for y in aoc.visit_range(y1, y2):
      grid[y][x] += 1

  def part1(self):
    print('===== Start part 1')
    self.reset()

    grid = []
    for row in range(self.dim):
      grid.append([0] * self.dim)

    for v in self.vents:
      if v.x1 == v.x2:
        # print('use', v)
        self.filly(grid, v.x1, v.y1, v.y2)
      elif v.y1 == v.y2:
        self.fillx(grid, v.y1, v.x1, v.x2)
        continue
      else:
        # print('skip', v)
        pass
    if self.trace_sample:
      self.pgrid(grid)

    return self.count_over(grid, 2)


  def part2(self):
    print('===== Start part 2')
    self.reset()

    grid = []
    for row in range(self.dim):
      grid.append([0] * self.dim)

    for v in self.vents:
      if v.x1 == v.x2:
        # print('use', v)
        self.filly(grid, v.x1, v.y1, v.y2)
      elif v.y1 == v.y2:
        self.fillx(grid, v.y1, v.x1, v.x2)
      else:
        self.filldiag(grid, v)
        pass

    if self.trace_sample:
      self.pgrid(grid)
    return self.count_over(grid, 2)

  @staticmethod
  def filldiag(grid, v):
    assert abs(v.x2 - v.x1) == abs(v.y2 - v.y1)
    length = abs(v.x2 - v.x1) + 1
    x = v.x1
    xmove = aoc.direction(v.x1, v.x2)
    y = v.y1
    ymove = aoc.direction(v.y1, v.y2)
    for i in range(length):
      grid[y][x] += 1
      x += xmove
      y += ymove


day05.sample_test("""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""", expect1=5, expect2=12)


if __name__ == '__main__':
  day05.run_and_check('input.txt', expect1=5147, expect2=16925)
