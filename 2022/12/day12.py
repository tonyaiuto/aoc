#!/usr/bin/env python3
"AOC 2021: day 12"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)


def neighbors(mm, p):
  ret = []
  r = p[0]
  c = p[1]
  if r > 0:
    ret.append((r-1, c))
  if r < mm.width-1:
    ret.append((r+1, c))
  if c > 0:
    ret.append((r, c-1))
  if c < mm.height-1:
    ret.append((r, c+1))
  return ret

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

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    s = line.find('S')
    if s >= 0:
      self.start = (s, self.mm.height)
      print('start at', self.start)
      line = line[0:s] + 'a' + line[s+1:]
    e = line.find('E')
    if e >= 0:
      self.end = (e, self.mm.height)
      print('end at', self.end)
      line = line[0:e] + 'z' + line[e+1:]
    self.mm.add_row(line)
    pass

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.mm.height < 10:
      self.mm.print()

    print("W, H", self.mm.width,self.mm.height)

    self.mm.shortest_path = self.mm.width * self.mm.height
    print('END', self.end)
    ret = s1(self.mm, self.start, self.end, visited=set())
    return self.mm.shortest_path

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


def s1(mm, at, end, visited, tag=''):
  if at == end:
    # print("AT END", end)
    return len(visited)
  if len(visited) >= mm.shortest_path:
    return -1
  x = mm.get(at[0], at[1])
  sh = ord(x)
  visited.add(at)
  to_visit = neighbors(mm, at)
  # print(tag, 'at', at, x, to_visit)
  sh = ord(mm.get(at[0], at[1]))
  lpath = -1
  for vv in to_visit:
    if vv in visited:
      continue
    h = ord(mm.get(vv[0], vv[1]))
    if h > sh + 1:
      continue
    lpath = s1(mm, vv, end, set(visited), tag=tag+' ')
    if lpath < 0:
      continue
    if mm.shortest_path < 0 or lpath < mm.shortest_path:
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
  day12.run_and_check('input.txt', expect1=None, expect2=None)
