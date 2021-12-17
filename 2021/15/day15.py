#!/usr/bin/env python3
"AOC 2021: day 15"

import copy
import heapq
import itertools

from tools import aoc
from tools import grid


class day15(aoc.aoc):

  def __init__(self):
    super(day15, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    self.memo = {}

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    self.grid = []
    self.cells = {}
    row = 0
    self.width = -1
    for line in self.all_input:
       self.grid.append([int(c) for c in line])
       for i,c in enumerate(line):
         self.cells[(i, row)] = int(c)
       row += 1
       if self.width == -1:
         self.width = len(line)
       else:
         assert self.width == len(line)
    self.height = len(self.grid)

    self.pos = (0,0)
    if self.trace_sample:
      print(self.cells)

  def part1(self):
    print('===== Start part 1')
    self.reset()

    pos = (0, 0)
    risk = -self.cells[pos]
    self.end = (self.width-1, self.height-1)
    print('end at', self.end)
    visited = set()

    self.lowrisk = 9 * len(self.cells)
    self.maxrisk = 9 * len(self.cells)

    # self.walk1(0, 0, visited, risk)
    # return self.lowrisk
    for d in range(min(self.width, self.height)-1, 0, -1):
      risk = self.least_risk_via(d, d)
      if self.trace_sample:
        print("risk:", d, d, '=', risk)
    return min(self.least_risk_via(0, 1), self.least_risk_via(1, 0))

  def least_risk_via(self, x, y):
    """This only works by luck."""
    ret = self.memo.get((x,y))
    if ret is not None:
      return ret

    if (x,y) == self.end:
      self.memo[(x,y)] = self.cells[self.end]
      return self.cells[self.end]
    r = []
    if x < self.width-1:
      r.append(self.least_risk_via(x+1, y))
    if y < self.height-1:
      r.append(self.least_risk_via(x, y+1))
    self.memo[(x,y)] = self.cells[(x,y)] + min(r)
    return self.cells[(x,y)] + min(r)

  def walk1(self, x, y, visited, risk):
    if (x,y) in visited:
      return
    risk += self.cells[(x,y)]
    if risk >= self.lowrisk:
      return
    if (x,y) == self.end:
      self.lowrisk = min(self.lowrisk, risk)
      if self.trace_sample:
        print('reached end at', x, y, 'risk', risk)
    if x < self.width-1:
      self.walk1(x+1, y, copy.copy(visited), risk)
    if y < self.height-1:
      self.walk1(x, y+1, copy.copy(visited), risk)

  def part2(self):
    print('===== Start part 2')
    self.reset()

    nc = {}
    w = self.width
    h = self.height
    # make it wider
    for i in range(5):
      for x, y in itertools.product(range(w), range(h)):
        risk = self.cells[(x,y)] + i
        if risk > 9:
          risk -= 9
        pos = (x+w*i, y)
        nc[pos] = risk
        if self.trace_sample and y == 0:
          print('5x', pos, risk)
    self.cells = nc

    print(''.join([str(nc[(x,0)]) for x in range(w * 5)]))
    print(''.join([str(nc[(x,h-1)]) for x in range(w * 5)]))

    # make it taller
    w = w * 5
    for i in range(1, 5):
      print('ybounds', (i-1)*h, i*h)
      for x, y in itertools.product(range(w), range((i-1)*h, i*h)):
        # print('5xy', x, y)
        risk = self.cells[(x,y)] + 1
        if risk > 9:
          risk -= 9
        pos = (x, y + h)
        self.cells[pos] = risk
        if self.trace_sample and (x == 0 or y == 0):
          print('5y', pos, risk)
      last_row = (i+1)*h - 1
      print(''.join([str(self.cells[(x,last_row)]) for x in range(w)]))

    self.width = w
    self.height = h * 5
    pos = (0, 0)
    self.end = (self.width-1, self.height-1)

    # use Dijkstra, right from wikipedia

    visited = set()
    risk = {}
    unvisited = set()
    max_risk = 9 * (self.width + 1) * (self.height + 1)
    for x in range(self.width):
      for y in range(self.height):
        risk[(x,y)] = max_risk
        unvisited.add((x,y))
    start = (0, 0)
    risk[start] = 0

    n_cells = self.width * self.height
    queue = []
    heapq.heappush(queue, (0, start))
    cur_node = start
    while len(unvisited) > 0 and cur_node != self.end:
      while cur_node in visited:
        _, cur_node = heapq.heappop(queue)

      if len(unvisited) % 1000 == 0:
        print('=========', len(unvisited), 'left')
      risk_so_far = risk[cur_node]
      for pos in grid.coords4(cur_node[0], cur_node[1], n_rows=self.height, n_cols=self.width):
        if pos in visited:
          continue
        # print(' visit:', pos)
        risk[pos] = min(risk[pos], risk_so_far + self.cells[pos])
        heapq.heappush(queue, (risk[pos], pos))
      visited.add(cur_node)
      unvisited.remove(cur_node)

    return risk[self.end]


day15.sample_test("""
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""", expect1=40, expect2=315)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=423, expect2=2778)
  pass
