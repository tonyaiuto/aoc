#!/usr/bin/env python3
"AOC 2021: day 12"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)


class day12(aoc.aoc):

  def __init__(self):
    super(day12, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.mm = gridutils.Grid()
    self.rows = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    s = line.find('S')
    if s >= 0:
      self.start = (len(self.rows), s)
      print('start at', self.start)
      line = line[0:s] + 'a' + line[s+1:]
    e = line.find('E')
    if e >= 0:
      self.end = (len(self.rows), e)
      print('end at', self.end)
      line = line[0:e] + 'z' + line[e+1:]
    self.mm.add_row(line)
    self.rows.append(line)

  def post_load(self):
    # called after all input is read
    self.height = len(self.rows)
    self.width = len(self.rows[0])

  def neighbors(self, p):
    ret = []
    r = p[0]
    c = p[1]
    if r > 0:
      ret.append((r-1, c))
    if r < self.height-1:
      ret.append((r+1, c))
    if c > 0:
      ret.append((r, c-1))
    if c < self.width-1:
      ret.append((r, c+1))
    return ret


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.height < 10:
      self.mm.print()
    self.mm.shortest_path = self.width * self.height + 1

    costs = []
    for r in range(self.mm.height):
      costs.append([-1] * self.width)
    costs[self.start[0]][self.start[1]] = 0
    print(costs)

    print("W, H", self.width,self.height)

    print('END', self.end)
    _ = self.s1(self.mm, costs, self.start, self.end, visited=set())
    return self.mm.shortest_path

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


  def s1(self, mm, costs, at, end, visited, tag=''):
    if at == end:
      print("AT END", end, 'cost=', costs[at[0]][at[1]])
      return len(visited)
    if len(visited) >= mm.shortest_path:
      return -1
    x = self.rows[at[0]][at[1]]
    cost_at = costs[at[0]][at[1]]
    sh = ord(x)
    visited.add(at)
    to_visit = self.neighbors(at)
    print(tag, 'at', at, '(%c)' % x, 'cost', cost_at, to_visit)
    lpath = -1
    for vv in to_visit:
      if vv in visited:
        continue
      h = ord(self.rows[vv[0]][vv[1]])
      if h > sh + 1:
        continue
  
      # print(vv)
      if costs[vv[0]][vv[1]] < 0 or costs[vv[0]][vv[1]] > cost_at + 1:
        costs[vv[0]][vv[1]] = cost_at + 1
      #else:
      #  continue
  
      # lpath = s1(mm, costs, vv, end, set(visited), tag=tag+' ')
      # sv.add(vv)
      sv = set(visited)
      lpath = self.s1(mm, costs, vv, end, sv, tag=tag+' ')
      if lpath < 0:
        continue
      if 0 < lpath and lpath < mm.shortest_path:
        print("new short path", lpath)
        mm.shortest_path = lpath
    return lpath


day12.sample_test("""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""", expect1=31, expect2=None)


if __name__ == '__main__':
  day12.run_and_check('input.txt', expect1=None, expect2=None)
