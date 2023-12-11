#!/usr/bin/env python3
"AOC 2021: day 14"

from collections import defaultdict
import copy
import heapq
import itertools
# import jsonrpclib
import math
import time
import tkinter

from tools import aoc
from tools import gridutils

import textgrid

class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)

class day14(aoc.aoc):

  animate = False

  def __init__(self):
    super(day14, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid(default_cell=' ')
    self.hose = 500
    self.min_x = 500
    # self.grid.set(self.hose, 0, '+')
    self.endpoints = []
    if day14.animate:
      host = '10.0.0.135'
      host = 'localhost'
      # self.canvas = jsonrpclib.Server('http://%s:8888' % host)
      self.tk_root = tkinter.Tk()
      self.canvas = textgrid.Canvas(self.tk_root)
    else:
      self.canvas = None

  @classmethod
  def set_animate(cls, animate):
    cls.animate = animate

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    last_x = None
    lasy_y = None
    for part in line.split(' '):
      if part == '->':
        continue
      x, y = part.split(',')
      x = int(x)
      y = int(y)
      if x < self.min_x:
        self.min_x = x
      self.grid.set(x, y, '#')
      if last_x:
        if last_x == x:
          for i in aoc.visit_range(last_y, y):
            self.grid.set(x, i, '#')
        else:
          for i in aoc.visit_range(last_x, x):
            self.grid.set(i, y, '#')
        self.endpoints.append([(last_x, last_y), (x, y)])
      last_x = x
      last_y = y

  def post_load(self):
    # called after all input is read
    self.bottom = self.grid.max_y
    self.setup_anim()

  def setup_anim(self):
    if not self.canvas:
      return
    self.v_xoff = max(0, self.min_x - self.bottom - 10)
    res = self.canvas.grid(width=500, height=self.bottom+1, cell_width=2)
    print('grid =>', res)
    for line in self.endpoints:
      sx = line[0][0]
      sy = line[0][1]
      ex = line[1][0]
      ey = line[1][1]
      pound = ord('#')
      if sx == ex:
        for i in aoc.visit_range(sy, ey):
          self.canvas.draw_cell(sx-self.v_xoff, i, 1)
      else:
        for i in aoc.visit_range(sx, ex):
          self.canvas.draw_cell(i-self.v_xoff, sy, 1)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.grid.print(from_x=490)
    print('max y:', self.bottom)

    for i in range(10000):
      if not self.drop_sand():
         return i
      if i < 5:
        # self.grid.print(from_x=490)
        pass

  def drop_sand(self):
    x = self.hose
    y = 0
    while True:
      y = self.fall_from(x, y)
      if y < 0:
        return False
      # down left
      if self.grid.get(x-1, y+1) == ' ':
        x = x - 1
        y = y + 1
      elif self.grid.get(x+1, y+1) == ' ':
        x = x + 1
        y = y + 1
      else:
        self.grid.set(x, y, 'o')
        if self.canvas:
          self.canvas.draw_cell(x, y, 1, 'pink')
          # time.sleep(.005)
        return True

  def fall_from(self, x, y):
    for y in range(y, self.bottom+1):
      # print(x, y, self.grid.get(x, y))
      if self.grid.get(x, y) != ' ':
        return y - 1
    return -1

  def part2(self):
    print('===== Start part 2')
    self.reset()

    self.bottom += 2
    print('max y:', self.bottom)
    for x in range(self.hose - 2 * self.bottom, self.hose + 2 * self.bottom):
      self.grid.set(x, self.bottom, '#')
    self.grid.print()

    for i in range(500000):
      self.drop_sand()
      if self.grid.get(self.hose, 0) == 'o':
        if i % 100 == 0:
          self.grid.print()
        return i + 1

    return -1



day14.set_animate(True)

day14.sample_test("""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""", expect1=24, expect2=93)

# day14.set_animate(False)

if __name__ == '__main__':
  day14.run_and_check('input.txt', expect1=755, expect2=None)
  pass
