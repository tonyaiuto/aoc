#!/usr/bin/env python3
"AOC 2021: day 15"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils
from tools import qparser


def man_d(x, y, bx, by):
  return abs(x - bx) + abs(y - by)


class Sensor(object):

  def __init__(self):
    self.x = 0
    self.y = 0
    self.bx = 0
    self.by = 0
    self.dist = 0

  def reset(self):
    self.dist = man_d(self.x, self.y, self.bx, self.by)

  def __str__(self):
    return '(%d, %d) =%d=> %d,%d' % (self.x, self.y, self.dist, self.bx, self.by)



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
    self.parser = qparser.QParser([
        qparser.Literal('Sensor at x='),
        qparser.Number('x'),
        qparser.Literal(', y='),
        qparser.Number('y'),
        qparser.Literal(': closest beacon is at x='),
        qparser.Number('bx'),
        qparser.Literal(', y='),
        qparser.Number('by'),
        ])
    self.sensors = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    if line.startswith("Row"):
      self.target_row = int(line.split()[1])
      return
    s = Sensor()
    self.parser.parse(s, line)
    s.reset()
    print(s)
    self.sensors.append(s)

  def post_load(self):
    # called after all input is read
    self.min_x = min([min(s.x, s.bx) for s in self.sensors])
    self.max_x = max([max(s.x, s.bx) for s in self.sensors])
    self.min_y = min([min(s.y, s.by) for s in self.sensors])
    self.max_y = max([max(s.y, s.by) for s in self.sensors])


  def part1(self):
    print('===== Start part 1')
    self.reset()
    print('check row', self.target_row, 'from', self.min_x, self.max_x)

    return 42


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day15.sample_test("""
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
Row 10
""", expect1=26, expect2=None)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=None, expect2=None)
