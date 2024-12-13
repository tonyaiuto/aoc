#!/usr/bin/env python3
"AOC 2023: day 12"

from collections import defaultdict
import itertools

from tools import aoc
from tools import gridutils

X = 0
Y = 1

def find_edge(a, b):
  ax = a[0]
  ay = a[1]
  bx = b[0]
  by = b[1]
  if ax == bx:
    # same column
    assert abs(ay - by) == 1
    min_x = min(ax, bx)
    return ((min_x, max(ay, by)), (min_x+1, max(ay, by)))
  # same row
  assert abs(ax - bx) == 1
  min_y = min(ay, by)
  return ((max(ax, bx), min_y), (max(ax, bx), min_y+1))

assert find_edge((3, 4), (3, 5)) == ((3, 5), (4, 5))
assert find_edge((42, 17), (43, 17)) == ((43, 17), (43, 18))

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
      region, perimeter, _ = self.find_region(pos, crop)
      ret += len(region) * perimeter
      done.update(region)
    return ret


  def find_region(self, pos, crop):
    region = set()
    frontier = set([pos])
    perimeter = 0
    edges = set()
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
            edge = find_edge(pos, npos)
            edges.add(edge)
            assert self.grid.get_pos(pos) == crop

      frontier = nf
    if self.doing_sample:
      print("region", crop, "area", len(region), "perimeter", perimeter)
      # print(edges)
    return region, perimeter, edges
    
  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    done = set()
    for pos in self.grid.points:
      if pos in done:
        continue
      crop = self.grid.get_pos(pos)
      region, perimeter, edges = self.find_region(pos, crop)
      perimeter = self.how_many_sides(edges, crop)
      ret += len(region) * perimeter
      done.update(region)
    return ret

  def how_many_sides(self, edges, crop):
    ends = defaultdict(set)
    for edge in edges:
      ends[edge[0]].add(edge)
      # assert len(ends[edge[0]]) <= 2
      ends[edge[1]].add(edge)
      # assert len(ends[edge[1]]) <= 2

    did_a_join = True
    while did_a_join:
      did_a_join = False
      for end_point in list(ends.keys()):
        connections = list(ends[end_point])
        # assert len(connections) in (0, 2)
        if len(connections) == 0:
          continue
        for pair in itertools.combinations(connections, 2):
          edge = pair[0]
          other = pair[1]
          new_edge = self.can_merge(pair[0], pair[1], crop)
          if not new_edge:
            continue
          # print('comp', edge, other, '=>', new_edge)
          ends[edge[0]].remove(edge)
          ends[edge[1]].remove(edge)
          ends[other[0]].remove(other)
          ends[other[1]].remove(other)
          ends[new_edge[0]].add(new_edge)
          ends[new_edge[1]].add(new_edge)
          did_a_join = True
          break

    edges = set([edge
                 for conns in ends.values()
                 for edge in conns
                ])
    # print('After reduce', edges)
    return len(edges)

  def can_merge(self, a, b, crop):
    """
    AAA
    ABA   Do not merge AB CA
    CAA
    """
    a_head = a[0]
    a_tail = a[1]
    b_head = b[0]
    b_tail = b[1]
    if a_head == b_head or a_tail == b_tail:
      return None
    if a_head[X] == a_tail[X]:
      if a_head[X] == b_head[X] and b_head[X] == b_tail[X]:
        a_crop_right = self.grid.get_pos(a_head)
        b_crop_right = self.grid.get_pos(b_head)
        if not (crop == a_crop_right and crop == b_crop_right):
          a_crop_left = self.grid.get_pos((a_head[X]-1, a_head[Y]))
          b_crop_left = self.grid.get_pos((b_head[X]-1, b_head[Y]))
          if not (crop == a_crop_left and crop == b_crop_left):
            return False
        # colinear in column
        y_min = min(a_head[Y], a_tail[Y], b_head[Y], b_tail[Y])
        y_max = max(a_head[Y], a_tail[Y], b_head[Y], b_tail[Y])
        return ((a_head[X], y_min), (a_head[X], y_max))
    if a_head[Y] == a_tail[Y]:
      if a_head[Y] == b_head[Y] and b_head[Y] == b_tail[Y]:
        # colinear in row
        a_crop_below = self.grid.get_pos(a_head)
        b_crop_below = self.grid.get_pos(b_head)
        if not (crop == a_crop_below and crop == b_crop_below):
          a_crop_above = self.grid.get_pos((a_head[X], a_head[Y]-1))
          b_crop_above = self.grid.get_pos((b_head[X], b_head[Y]-1))
          if not (crop == a_crop_above and crop == b_crop_above):
            return False
        x_min = min(a_head[X], a_tail[X], b_head[X], b_tail[X])
        x_max = max(a_head[X], a_tail[X], b_head[X], b_tail[X])
        return ((x_min, a_head[Y]), (x_max, a_head[Y]))
    return None

# assert can_merge(((1, 1), (2, 1)), ((0, 1), (1, 1))) == ((0, 1), (2, 1))

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
""", expect1=1930, expect2=1206)


if __name__ == '__main__':
   # 855340 low part2
  day12.run_and_check('input.txt', expect1=1402544, expect2=862486)
