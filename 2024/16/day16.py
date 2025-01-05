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


  def part2(self):
    print('===== Start part 2')

    least_cost = self.part1()
    print("PART1 least cost", least_cost)

    # Track all paths fully.
    # But delete it if they get too costly
    # union the points at the end

    # (pos, dir) => cost
    initial = Head(self.start, self.dir, 0)
    path = set([self.start])
    paths = {initial: path}
    heads = [initial]
    # Map of cells visited and what it cost to get there.
    visited = {(initial.pos, initial.dir): 0}
    # print(self.possible_moves(initial))
    end_costs = defaultdict(set)
    best_end = -1
    for n in range(self.grid.width * self.grid.height):
      new_paths = {}
      for head, p_path in paths.items():
        for nxt, cost in self.possible_moves(head):
          prev_cost = visited.get(nxt)
          # Did we get here at lower cost before?
          if (prev_cost and prev_cost < cost) or least_cost < cost:
            # print('got to', nxt, 'at cost', prev_cost, '<', cost)
            if self.doing_sample and nxt[0][1] == 7:
              print("drop path:", n, head, nxt, '\n  ', len(path), [p for p in sorted(p_path)])
            continue

          if head.pos != nxt[0] and nxt[0] in p_path: 
            # print("BACKTRACKING", n, head, nxt)
            continue

          # We'll keep this head
          path = set(p_path)
          path.add(nxt[0])
          new_head = Head(nxt[0], nxt[1], cost)
          if self.doing_sample and nxt[0][0] <= 8:
            print("keep new head:", n, new_head, '\n  ', len(path), [p for p in sorted(path)])

          # But we also have been here before
          if prev_cost == cost:
            other_path = new_paths.get(new_head) or []
            if self.doing_sample:
              print("===== join at", nxt, cost,
                    '\n', len(path), [p for p in sorted(path)], 
                    '\n', len(other_path), [p for p in sorted(other_path)],
              )
            path = path.union(other_path) 
          new_paths[new_head] = path
          visited[nxt] = cost

          if nxt[0] == self.end:
            # print("===================== end", nxt, cost, len(path))
            end_costs[cost] = end_costs[cost].union(path)
            if best_end < 0 or cost < best_end:
              best_end = cost
      paths = new_paths
    return len(end_costs[best_end])


  def possible_moves(self, path):
    """Return list of possible moves from path.pos.

    Moves are tuple of ((pos, dir), cost)
    """
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
  day16.run_and_check('input.txt', expect1=85420, expect2=492)
