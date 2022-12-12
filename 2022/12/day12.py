#!/usr/bin/env python3
"AOC 2021: day 12"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Point(object):

  def __init__(self, r, c):
    self.r = r
    self.c = c

  def __str__(self):
    return '%d,%d' % (self._r, self._c)

  def __hash__(self):
    return self.r * 1000 + self.c

  def __eq__(self, other):
    return self.r == other.r and self.c == other.c

  @property
  def _r(self):
    return self.r

  @property
  def _c(self):
    return self.c


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
      self.start = Point(len(self.rows), s)
      print('start at', self.start)
      line = line[0:s] + 'a' + line[s+1:]
    e = line.find('E')
    if e >= 0:
      self.end = Point(len(self.rows), e)
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
    if p.r > 0:
      ret.append(Point(p.r-1, p.c))
    if p.r < self.height-1:
      ret.append(Point(p.r+1, p.c))
    if p.c > 0:
      ret.append(Point(p.r, p.c-1))
    if p.c < self.width-1:
      ret.append(Point(p.r, p.c+1))
    return ret


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.height < 10:
      self.mm.print()
    self.shortest_path = self.width * self.height + 1
    self.mm.shortest_path = self.shortest_path

    costs = []
    for r in range(self.mm.height):
      costs.append([-1] * self.width)
    costs[self.start.r][self.start.c] = 0
    print("W, H", self.width,self.height)
    print('start', self.start)
    print('END', self.end)

    self.s1bfs(costs, self.start, self.end, visited=set())
    return self.shortest_path

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


  def s1bfs(self, costs, start, end, visited, tag=''):
    if len(visited) >= self.shortest_path:
      return -1

    frontier = set()
    visited = set([start])
    costs[start.r][start.c] = 0
    self.expand_frontier(start, costs, frontier, visited)

    while len(frontier) > 0:
      print('Cur frontier', [str(s) for s in frontier])
      if len(frontier) > 100:
         print("CRAP")
         return
      cur = set(frontier)
      frontier = set()
      for at in cur:
        if at in visited:
          continue
        if at == end:
          at_cost = costs[at.r][at.c]
          print("AT END", end, 'cost=', at_cost)
          if at_cost < self.shortest_path:
            print("new short path", at_cost)
            self.shortest_path = at_cost
        self.expand_frontier(at, costs, frontier, visited)
        visited.add(at)

  def expand_frontier(self, at, costs, frontier, visited):
    x = self.rows[at.r][at.c]
    cost_at = costs[at.r][at.c]
    sh = ord(x)
    # visited.add(at)
    to_visit = self.neighbors(at)
    print('at', at, '(%c)' % x, 'cost', cost_at, [str(v) for v in to_visit])
    for vv in to_visit:
      if vv in visited:
        continue
      h = ord(self.rows[vv.r][vv.c])
      if h > sh + 1:
        continue
      if costs[vv.r][vv.c] > 0 and costs[vv.r][vv.c] < cost_at + 1:
        continue
      costs[vv.r][vv.c] = cost_at + 1
      frontier.add(vv)


  def s1dfs(self, mm, costs, at, end, visited, tag=''):
    if len(visited) >= mm.shortest_path:
      return -1
    x = self.rows[at.r][at.c]
    cost_at = costs[at.r][at.c]
    sh = ord(x)
    visited.add(at)
    to_visit = self.neighbors(at)
    # print(tag, 'at', at, '(%c)' % x, 'cost', cost_at, to_visit)
    lpath = -1
    for vv in to_visit:
      if vv in visited:
        continue
      h = ord(self.rows[vv.r][vv.c])
      if h > sh + 1:
        continue

      if vv == end:
        print("AT END", end, 'cost=', costs[at.r][at.c])
        return len(visited) 
  
      # print(vv)
      if costs[vv.r][vv.c] < 0 or costs[vv.r][vv.c] > cost_at + 1:
        costs[vv.r][vv.c] = cost_at + 1
      else:
        continue
  
      lpath = self.s1dfs(mm, costs, vv, end, set(visited), tag=tag+' ')
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
  day12.run_and_check('input.txt', expect1=528, expect2=None)
