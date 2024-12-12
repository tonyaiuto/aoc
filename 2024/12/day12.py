#!/usr/bin/env python3
"AOC 2023: day 12"

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

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.__dict__)



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
    self.grid = gridutils.Grid()

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      self.grid.print()
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    ret = 0
    done = set()
    for pos in self.grid.points:
      if pos in done:
        continue
      crop = self.grid.get_pos(pos)
      region, perimeter = self.find_region(pos, crop)
      ret += len(region) * perimeter
      done.update(region)
    return ret


  def find_region(self, pos, crop):
    region = set()
    frontier = set([pos])
    perimeter = 0
    while len(frontier) > 0:
      nf = set()
      for pos in frontier:
        region.add(pos)
        for delta in gridutils.DIRS4:
          npos = gridutils.add_vector(pos, delta)
          if npos in region:
            continue
          neighbor = self.grid.get_pos(npos)
          if self.doing_sample:
            print(crop, pos, neighbor, npos)
          if neighbor == crop:
            nf.add(npos)
          else:
            perimeter += 1
      frontier = nf
    print("region", crop, "area", len(region), "perimeter", perimeter)
    return region, perimeter
    
  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    done = set()
    for pos in self.grid.points:
      if pos in done:
        continue
      crop = self.grid.get_pos(pos)
      region, perimeter = self.find_region(pos, crop)
      perimeter = self.how_many_sides(region)
      ret += len(region) * perimeter
      done.update(region)
    return ret

  def how_many_sides(self, region):
    return 7


day12.sample_test("""
AAAA
BBCD
BBCC
EEEC
""", expect1=140, expect2=80)

day12.sample_test("""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""", expect1=1930, expect2=None)


if __name__ == '__main__':
  day12.run_and_check('input.txt', expect1=1402544, expect2=None)
