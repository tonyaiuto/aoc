5511201#!/usr/bin/env python3
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

def merge_ranges(a, b):
  # disjoint
  if a[1] < b[0] or a[0] > b[1]:
    return a, b
  if a[0] < b[0]:
    return (a[0], b[1]), None
  if a[0] < b[0]:
    return (a[0], b[1]), None



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
    return '(%8d, %8d) =%8d=> %8d,%8d' % (self.x, self.y, self.dist, self.bx, self.by)



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
    # print(s)
    self.sensors.append(s)

  def post_load(self):
    # called after all input is read
    self.min_x = min([min(s.x, s.bx) for s in self.sensors])
    self.max_x = max([max(s.x, s.bx) for s in self.sensors])
    self.min_y = min([min(s.y, s.by) for s in self.sensors])
    self.max_y = max([max(s.y, s.by) for s in self.sensors])
    self.beacons = defaultdict(list)
    for s in self.sensors:
      key = (s.bx, s.by)
      self.beacons[key].append(s)
    print('n_sensors:', len(self.sensors), 'n_beacons:', len(self.beacons))


  def part1(self):
    print('===== Start part 1')
    self.reset()
    print('check row', self.target_row, 'from', self.min_x, self.max_x)

    safe_ranges = self.safe_ranges_for_row(self.target_row)
    safe = 0
    for r in safe_ranges:
      safe += r[1] - r[0] + 1
      print(r, 'safe', safe)
    for b in self.beacons.keys():
      if b[1] == self.target_row:
        print("reduce for beacon", b)
        safe -= 1
    #for s in self.sensors:
    #  if s.y == self.target_row:
    #    print("reduce for sensor", s)
    #    safe -= 1
    return safe


  def safe_ranges_for_row(self, row):
    ranges = []
    for s in self.sensors:
      ydisp = abs(s.y - row)
      xdisp = s.dist - ydisp
      if xdisp < 0:
        # print(s, 'ydisp:', '%8d' % ydisp, 'gives xdisp: %8d' % xdisp, 'SKIP')
        continue
      # left = max(self.min_x, s.x - xdisp)
      # right = min(self.max_x, s.x + xdisp)
      left = s.x - xdisp
      right = s.x + xdisp
      # print(s, 'ydisp:', '%8d' % ydisp, 'gives range: %8d,%8d' % (left, right))
      ranges.append((left, right))

    ranges = sorted(ranges)
    ret = []
    left = ranges[0]
    for right in ranges[1:]:
      # (-4, 8) (9, 25)
      # a, b = merge_ranges(left, right)
      # print("CMP:", left, right)
      if left[1] < right[0] or left[0] > right[1]:
        ret.append(left)
        # print("  shift")
        left = right
      else:
        #  merge
        nleft = (left[0], max(left[1], right[1]))
        # print(' merge', left, right, '=>', nleft)
        left = nleft
    ret.append(left)
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    max_pos = 4000000
    x = 1
    y = 42
    if len(self.sensors) < 20:
      max_pos = 20
    for row in range(max_pos):
      # invert ranges w.r.t 0:4000000
      possible = [(0, max_pos)]
      possible = []
      # (-4, 8) (9, 25)
      # (-4, 8) (10, 25)
      # (-5, 24)
      last_end = -1
      for r in self.safe_ranges_for_row(row):
        start = r[0]
        end = r[1]
        # print('  last_end', last_end, start, end)
        pos_start = last_end + 1
        pos_end = r[0] - 1
        if pos_end >= pos_start:
          # print("possible", pos_start, pos_end)
          possible.append((pos_start, pos_end))
          return pos_start * 4000000 + row
        last_end = r[1]
    return -1



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
""", expect1=26, expect2=56000011)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=5511201, expect2=11318723411840)
