#!/usr/bin/env python3
"AOC 2021: day 09"

import math

from tools import aoc
from tools import gridutils


class Pos(object):

  def __init__(self, name):
    self.name = name
    self.r = 0
    self.c = 0
    self.visited = set((0, 0))

  def __str__(self):
    return '%s %d,%d' % (self.name, self.r, self.c)

  def move(self, dir, dist):
    if dir == 'R':
      self.c += dist
    elif dir == 'L':
      self.c -= dist
    elif dir == 'U':
      self.r += dist
    elif dir == 'D':
      self.r -= dist
    else:
      self.fail('bad move', dir, dist)

  def follow(self, other):
    r_delta = other.r - self.r
    c_delta = other.c - self.c
    # TIL: copysign(1, 0) => 1 instead of 0, because support for signed zero.
    r_inc = int(math.copysign(1, r_delta)) if r_delta else 0
    c_inc = int(math.copysign(1, c_delta)) if c_delta else 0

    if abs(r_delta) <= 1 and abs(c_delta) <= 1:
      return
    self.r += r_inc
    self.c += c_inc
    self.visited.add((self.r, self.c))
    if abs(self.r) < 2:
      print(self.visited)
    return


class day09(aoc.aoc):

  def __init__(self):
    super(day09, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.head = Pos('H')
    self.tail = Pos('T')

  def part1(self):
    print('===== Start part 1')
    self.reset()
    for line in self.all_input:
      dir, dist = line.split(' ')
      dist = int(dist)
      for i in range(dist):
        self.head.move(dir, 1)
        self.tail.follow(self.head)
        # print(self.head, self.tail)

    return len(self.tail.visited)


  def part2(self):
    print('===== Start part 2')
    self.head = Pos('H')
    knots = []
    for k in range(9):
      knots.append(Pos(str(k+1)))

    for line in self.all_input:
      dir, dist = line.split(' ')
      dist = int(dist)
      for i in range(dist):
        self.head.move(dir, 1)
        target = self.head
        for k in knots:
          k.follow(target)
          target = k
        # print(self.head, self.tail)

    return len(knots[-1].visited)


day09.sample_test("""
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""", expect1=13, expect2=1)


if __name__ == '__main__':
  day09.run_and_check('input.txt', expect1=6236, expect2=2449)
