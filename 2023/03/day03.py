#!/usr/bin/env python3
"AOC 2023: day 03"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


def is_symbol(c):
  if c.isdigit():
    return False
  if c == '.':
    return False
  return True


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day03(aoc.aoc):

  def __init__(self):
    super(day03, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.rows = ['']

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.rows.append('.' + line.strip() + '.')
    pass

  def post_load(self):
    # called after all input is read
    width = len(self.rows[1])
    dots = width * '.'
    self.rows[0] = dots
    self.rows.append(dots)
    self.adj = []
    for r in range(len(self.rows)):
      self.adj.append([0] * width)

  def find_partnos(self, row):
    prev = self.rows[row-1]
    cur = self.rows[row]
    nxt = self.rows[row+1]

    part_no = 0
    start = -1
    ret = []
    for sc in range(1, len(cur)):
      c = cur[sc]
      if c.isdigit():
        part_no = part_no * 10 + (ord(c) - ord('0'))
        if start < 0:
          start = sc
          ok = is_symbol(prev[sc-1]) or is_symbol(cur[sc-1]) or is_symbol(nxt[sc-1])
        ok |= is_symbol(prev[sc]) or is_symbol(nxt[sc])
      else:
        if start >= 0:
          ok |= is_symbol(prev[sc]) or is_symbol(cur[sc]) or is_symbol(nxt[sc])
          if ok:
            ret.append([part_no, row, start, sc])
          self.adj[row][start - 1] += 1
          self.adj[row][sc] += 1
          for i in range(start - 1, sc+1):
            self.adj[row-1][i] += 1
            self.adj[row+1][i] += 1
        part_no = 0
        start = -1
    return ret

  def part1(self):
    print('===== Start part 1')
    self.reset()
    sum = 0
    for row in range(1, len(self.rows) - 1):
      parts = self.find_partnos(row)
      # print(parts)
      for p in parts:
        sum += p[0]
    return sum

  def part2(self):
    print('===== Start part 2')
    self.reset()
    parts = []
    for row in range(1, len(self.rows) - 1):
      parts.extend(self.find_partnos(row))
    print(parts)
    #for a in self.adj:
    #  print(a)
    sum = 0
    for row in range(1, len(self.rows) - 1):
      cur = self.rows[row]
      print('%02d' % row, cur)
      for sc in range(1, len(cur)):
        c = cur[sc]
        if c == '*':
          if self.adj[row][sc] == 2:
            print("OK AT", row, sc)
            ratio = 1
            for p in parts:
              part_row = p[1]
              if part_row < row - 1 or part_row > row + 1:
                continue
              print('row ok for', p)
              if sc < p[2] - 1:
                continue
              if sc > p[3]:
                continue
              print('col ok for', p)
              ratio *= p[0]
              print('ratio', ratio, 'sum', sum)
            sum += ratio
    print('final ratio', ratio, 'sum', sum)
    return sum


day03.sample_test("""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""", expect1=4361, expect2=467835)


if __name__ == '__main__':
  day03.run_and_check('input.txt', expect1=535235, expect2=79844424)
