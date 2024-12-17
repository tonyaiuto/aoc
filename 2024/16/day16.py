#!/usr/bin/env python3
"AOC 2023: day 16"

from collections import defaultdict
from collections import namedtuple
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

DIRS=gridutils.DIRS4

Head = namedtuple('Head', 'pos, dir, cost')


class day16(aoc.aoc):

  def __init__(self):
    super(day16, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid(ignore='.')
    self.dir = 1  # EAST

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)
    x = line.find('E')
    if x >= 0:
      self.end = (x, self.grid.height)
      self.grid.set_pos(self.end, ' ')
    x = line.find('S')
    if x >= 0:
      self.start = (x, self.grid.height)
      self.grid.set_pos(self.start, ' ')
      

  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.doing_sample:
      self.grid.print()
    print("start", self.start, 'end', self.end)

    # (pos, dir) => cost
    initial = Head(self.start, self.dir, 0)
    heads = [initial]
    visited = {(initial.pos, initial.dir): 0}
    print(self.possible_moves(initial))
    end_costs = set()
    for n in range(self.grid.width * self.grid.height):
      new_heads = []
      for p in heads:
        for nxt, cost in self.possible_moves(p):
          prev_cost = visited.get(nxt)
          if nxt[0] == self.end:
            # print("===================== end", nxt)
            end_costs.add(cost)
          if prev_cost and prev_cost <= cost:
            # print('got to', nxt, 'at cost', prev_cost, '<', cost)
            continue
          new_heads.append(Head(nxt[0], nxt[1], cost))
          visited[nxt] = cost
      heads = new_heads
    if self.doing_sample:
      cells = set([v[0] for v in visited.keys()])
      print(cells)
      print(len(cells))
    return min(end_costs)

  def possible_moves(self, path):
    ret = []
    np = gridutils.add_vector(path.pos, DIRS[path.dir])
    if self.grid.get_pos(np) != '#':
      ret.append(((np, path.dir), path.cost+1))
    right = (path.dir+1) % 4
    np = gridutils.add_vector(path.pos, DIRS[right])
    if self.grid.get_pos(np) != '#':
      ret.append(((path.pos, right), path.cost+1000))
    left = (path.dir+3) % 4
    np = gridutils.add_vector(path.pos, DIRS[left])
    if self.grid.get_pos(np) != '#':
      ret.append(((path.pos, left), path.cost+1000))
    return ret

  def part2(self):
    print('===== Start part 2')

    # (pos, dir) => cost
    initial = Head(self.start, self.dir, 0)
    heads = [initial]
    visited = {(initial.pos, initial.dir): 0}
    print(self.possible_moves(initial))
    end_costs = set()
    best_end = -1
    for n in range(self.grid.width * self.grid.height):
      new_heads = []
      for p in heads:
        for nxt, cost in self.possible_moves(p):
          prev_cost = visited.get(nxt)
          if prev_cost and prev_cost < cost:
            # print('got to', nxt, 'at cost', prev_cost, '<', cost)
            continue
          if nxt[0] == self.end:
            print("===================== end", nxt, cost)
            if best_end < 0 or cost < best_end:
              best_end = cost
              # visited now has the lowest costs
              pos_costs = [{cell_dir[0]: cost for cell_dir, cost in visited.items()}]
            elif cost == best_end:
              best_end = cost
              # visited now has the lowest costs
              pos_costs.append({cell_dir[0]: cost for cell_dir, cost in visited.items()})
            end_costs.add(cost)
          new_heads.append(Head(nxt[0], nxt[1], cost))
          visited[nxt] = cost
      heads = new_heads

    # visited now has the lowest costs
    costs = {cell_dir[0]: cost for cell_dir, cost in visited.items()}

    for pc in pos_costs:
      i = 0
      keys = list(pc.keys())
      for i in range(1, len(pc), 8):
        print(",  ".join(["%-9s= %4d" % (key, pc[key]) for key in keys[i:i+8]]))
      
    # print(pos_costs)
    pos = self.end
    ends = [self.end]
    for n in range(10):
      new_ends = []
      for end in ends:
        lc = costs[end]
        print("at", end, 'lc=', lc)
        for dir in range(4):
          np = gridutils.add_vector(end, DIRS[dir])
          if np not in costs:
            print('loser', np)
            continue
          from_cost = costs[np]
          if from_cost < lc:
            best = [np]
            lc = from_cost
          elif from_cost == lc:
            best.append(np)
        print("back to", best)
        new_ends.extend(list(best))
      ends = new_ends

    return min(end_costs)

  def possible_moves(self, path):
    ret = []
    np = gridutils.add_vector(path.pos, DIRS[path.dir])
    if self.grid.get_pos(np) != '#':
      ret.append(((np, path.dir), path.cost+1))
    right = (path.dir+1) % 4
    np = gridutils.add_vector(path.pos, DIRS[right])
    if self.grid.get_pos(np) != '#':
      ret.append(((path.pos, right), path.cost+1000))
    left = (path.dir+3) % 4
    np = gridutils.add_vector(path.pos, DIRS[left])
    if self.grid.get_pos(np) != '#':
      ret.append(((path.pos, left), path.cost+1000))
    return ret

    return 42


day16.sample_test("""
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""", expect1=7036, expect2=45)


if __name__ == '__main__':
  day16.run_and_check('input.txt', expect1=85420, expect2=None)
