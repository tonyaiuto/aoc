#!/usr/bin/env python3
"AOC 2021: day 24"

from collections import defaultdict
import copy
import itertools

from tools import aoc
from tools import gridutils


class State(object):

  def __init__(self, x, y, turn):
    self.x = x
    self.y = y
    self.turn = turn


class Blizzard(object):

  def __init__(self, x, y, dir):
    self.x = x
    self.y = y
    self.dir = dir

  def __str__(self):
    return "(%d, %d, %c)" % (self.x, self.y, self.dir)

  def pos(self):
    return (self.x, self.y)

  def bounce(self):
    if self.dir == '<':
      self.dir = '>'
    elif self.dir == '>':
      self.dir = '<'
    elif self.dir == '^':
      self.dir = 'v'
    elif self.dir == 'v':
      self.dir = '^'
    else:
      assert self.dir == 42


class day24(aoc.aoc):

  def __init__(self):
    super(day24, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid()
    self.bliz = []
    self.n_rows = 0
    self.x = 1
    self.y = 0
    self.places = {}
    self.move = 0

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)
    for i,c in enumerate(line):
      if c in ('<', '>', 'v', '^'):
        b = Blizzard(i, self.n_rows, c)
        self.bliz.append(b)
    self.n_rows += 1

  def post_load(self):
    # called after all input is read
    if self.trace_sample:
      self.grid.print()
    self.right = len(self.all_input[0]) - 1
    self.bottom = len(self.all_input) - 1
    print('loaded', len(self.bliz), 'blizzards')

  def show(self):
    g = gridutils.Grid()
    print("Minute", self.move)
    for x in range(self.right+1):
      if x != 1:
        g.set(x, 0, '#')
      if x != self.right-1:
        g.set(x, self.bottom, '#')
    for y in range(self.bottom):
      g.set(0, y, '#')
      g.set(self.right, y, '#')
 
    for b in self.bliz:
      c = g.get(b.x, b.y)
      v = b.dir
      if c != ' ':
        if c.isdigit():
          v = chr(ord(c) + 1)
        else:
          v = '2'
      g.set(b.x, b.y, v)
    for p in self.places:
      g.set(p[0], p[1], 'e')
    g.print()

  def move_all(self):
    occupied = set()
    for b in self.bliz:
      if b.dir == '<':
        b.x -= 1
        if b.x == 0:
          b.x = self.right - 1
      elif b.dir == '>':
        b.x += 1
        if b.x == self.right:
          b.x = 1
      elif b.dir == '^':
        b.y -= 1
        if b.y == 0:
          b.y = self.bottom - 1
      elif b.dir == 'v':
        b.y += 1
        if b.y == self.bottom:
          b.y = 1
      occupied.add((b.x, b.y))
    return occupied

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.places[(1, 0)] = 0

    # while True:
    for i in range(290):
      np = self.do_turn(goal=(self.right-1, self.bottom))
      if np is None:
        break
      print("Changed # states", len(self.places), len(np))
      self.places = np
      self.show()
      if (self.right-1, self.bottom-1) in self.places:
        print("In the good place")
        #return self.move+1
    return self.move

  def do_turn(self, goal):
    self.move += 1
    occupied = self.move_all()
    # print(occupied)
    ret = {}
    for pos in self.places:
      x = pos[0]
      y = pos[1]
      for off_x, off_y in [(0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)]:
        x1 = x + off_x
        y1 = y + off_y
        if x1 == goal[0] and y1 == goal[1]:
          print("DONE ", x1, y1, self.move)
          return None

        if x1 <= 0 or x1 >= self.right:
          continue
        if off_x != 0 or off_y != 0:
          if y1 <= 0 or  y1 >= self.bottom:
            continue
        np = (x1, y1)
        if np in occupied:
          # print('occupied', np)
          continue
        # print(x1, y1)
        ret[np] = self.move
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.places[(1, 0)] = 0
    for i in range(1000):
      np = self.do_turn(goal=(self.right-1, self.bottom))
      if np is None:
        break
      print("Changed # states", len(self.places), len(np))
      self.show()
      self.places = np
      if (self.right-1, self.bottom-1) in self.places:
        print("In the good place #1")

    self.places = {
        (self.right-1, self.bottom): self.move
    }
    self.show()
    for i in range(1000):
    # while True:
      np = self.do_turn(goal=(1, 0))
      if np is None:
        break
      print("Changed # states", len(self.places), len(np))
      self.places = np
      self.show()
      if (1, 0) in self.places:
        print("In the good place #2")

    self.places = {}
    self.places[(1, 0)] = self.move
    for i in range(1000):
    # while True:
      np = self.do_turn(goal=(self.right-1, self.bottom))
      if np is None:
        break
      print("Changed # states", len(self.places), len(np))
      self.places = np
      self.show()
      if (self.right-1, self.bottom-1) in self.places:
        print("In the good place #1")

    return self.move


day24.sample_test("""
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""", expect1=18, expect2=54)


if __name__ == '__main__':
  # part2, 598 too low
  day24.run_and_check('input.txt', expect1=274, expect2=839)
