#!/usr/bin/env python3
"AOC 2023: day 14"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Robot(object):

  def __init__(self, line):
    p,v = line.split(' ')
    t = [int(x) for x in p[2:].split(',')]
    self.x = t[0]
    self.y = t[1]
    t = [int(x) for x in v[2:].split(',')]
    self.dx = t[0]
    self.dy = t[1]
    # print(self)

  def __repr__(self):
    return str(self)

  def __str__(self):
    return '@%s,v=%d,%d' % ((self.x, self.y), self.dx, self.dy)



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
    self.robots = []

  def do_line(self, line):
    robot = Robot(line)
    self.robots.append(robot)

  def post_load(self):
    self.max_x = max([r.x for r in self.robots])
    self.max_y = max([r.y for r in self.robots])
    print("max_x/y", self.max_x, self.max_y)

  def move_robot(self, r, n):
    nx = (r.x + r.dx * n) % (self.max_x + 1)
    ny = (r.y + r.dy * n) % (self.max_y + 1)
    return nx, ny

  def part1(self):
    print('===== Start part 1')
    self.reset()

    if self.doing_sample:
      grid = gridutils.Grid(default_cell='.')
      for r in self.robots:
        nx, ny =  self.move_robot(r, 100)
        # print('moved', r.x, r.y, 'to', nx, ny)
        prev = grid.get(nx, ny)
        if not prev or prev == '.':
          prev = '0'
        grid.set(nx, ny, str(int(prev) + 1))
      grid.print()

    quads = [0] * 4
    mid_x = (self.max_x + 1) // 2
    mid_y = (self.max_y + 1) // 2
    print("mid x/y", mid_x, mid_y)
    for r in self.robots:
      nx, ny =  self.move_robot(r, 100)
      # print('moved', r.x, r.y, 'to', nx, ny)
      if nx == mid_x or ny == mid_y:
        continue
      quad = 0
      if nx > mid_x:
        quad = 1
      if ny >  mid_y:
        quad += 2
      quads[quad] += 1
    print(quads)
    ret = 1
    for q in quads:
      ret = ret * q
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    """
    for i in range(5):
      nx = (r.x + r.dx * i) % (self.max_x + 1)
      print(r.x, r.dx, i, self.max_x, '=>', nx)
      ny = (r.y + r.dy * i) % (self.max_y + 1)
      print(r.y, r.dy, i, self.max_y, '=>', ny)
      print(i, 'moved', r.x, r.y, 'to', nx, ny)
    """
  
    move = 0
    while move < 20000:
      move += 1

      points = set()
      grid = gridutils.Grid(default_cell='.')
      for r in self.robots:
        nx, ny = self.move_robot(r, move)
        grid.set(nx, ny, 'X')
      # grid.print(show_row_numbers=True)

      last_y = -1
      tree = True
      xat = set()
      for pos in sorted(grid.live_cells(), key=lambda x: x[1]):
        # print(pos)
        if pos[1] != last_y:
          if len(xat) > 0:
            if not is_symetric(xat, self.max_x):
              tree = False
              break
            xat = set()
        xat.add(pos[0])
      if tree:
        grid.print()
        print(move)
        return move

    return -1

def is_symetric(xat, max_x):
  for x in xat:
    if max_x+1-x not in xat:
      return False
  return True




day14.sample_test("""
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""", expect1=12, expect2=1)


if __name__ == '__main__':
  day14.run_and_check('input.txt', expect1=224438715, expect2=None)
