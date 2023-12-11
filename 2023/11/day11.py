#!/usr/bin/env python3
"AOC 2023: day 11"

from tools import aoc
from tools import gridutils


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day11(aoc.aoc):

  def __init__(self):
    super(day11, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = gridutils.Grid(default_cell=' ')

  def do_line(self, line):
    # called for each line of input
    self.grid.add_row(line)
    pass

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.grid.print()
    self.galaxies = []
    g2 = self.expand()
    # g2.print()
    return self.sum_distances()

  def sum_distances(self):
    ng = len(self.galaxies)
    ret = 0
    for i, g in enumerate(self.galaxies):
      for o_i in range(i+1, ng):
        other = self.galaxies[o_i]
        dist = abs(g[0] - other[0]) + abs(g[1] - other[1])
        ret += dist
    return ret


  def expand(self, expansion=1):
    expand_rows = []
    expand_cols = []
    g = self.grid
    for row in range(g.min_y, g.max_y+1):
      clear = True
      for col in range(g.min_x, g.max_x+1):
         if g.get(col, row) == '#':
           clear = False
           break
      if clear:
        expand_rows.append(row)
    for col in range(g.min_x, g.max_x+1):
      clear = True
      for row in range(g.min_y, g.max_y+1):
         if g.get(col, row) == '#':
           clear = False
           break
      if clear:
        expand_cols.append(col)
    print(expand_rows, expand_cols)

    expand_rows.append(g.max_y+1)
    expand_cols.append(g.max_x+1)

    r_inc = 0
    ret = gridutils.Grid(default_cell=' ')
    r_exp = list(expand_rows)
    for row in range(g.min_y, g.max_y+1):
      if row == r_exp[0]:
        r_inc += expansion
        r_exp = r_exp[1:]
      c_inc = 0
      c_exp = list(expand_cols)
      for col in range(g.min_x, g.max_x+1):
        if col == c_exp[0]:
          c_inc += expansion
          c_exp = c_exp[1:]
        was = g.get(col, row)
        if was == '#':
          ret.set(col+c_inc, row+r_inc, was)
          self.galaxies.append((col+c_inc, row+r_inc))
    return ret

  def part2(self):
    print('===== Start part 2')

    # self.grid.print()
    self.galaxies = []
    # g2 = self.expand(expansion=10-1)
    g2 = self.expand(expansion=1000000-1)
    # g2.print()
    return self.sum_distances()


day11.sample_test("""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""", expect1=374, expect2=82000210)


if __name__ == '__main__':
  day11.run_and_check('input.txt', expect1=9370588, expect2=746207878188)
