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


class Sensor(object):

  def __init__(self):
    pass
    #self.x = x
    #self.y = y
    #self.bx = bx
    #self.by = by

  def __str__(self):
    return '(%d, %d) -> %d,%d' % (self.x, self.y, self.bx, self.by)



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

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    s = Sensor()
    self.parser.parse(s, line)
    print(s)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

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
""", expect1=26, expect2=None)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=None, expect2=None)
