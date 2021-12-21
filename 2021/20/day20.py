#!/usr/bin/env python3
"AOC 2021: day 20"

from collections import defaultdict

from tools import aoc
from tools import gridutils


def count_pixels(image, skip=0):
  ret = 0
  for y in range(image.min_y+skip, image.max_y-skip+1):
    for x in range(image.min_x+skip, image.max_x-skip+1):
      if image.points.get((x, y)) == '1':
        ret += 1
  return ret

class day20(aoc.aoc):

  def __init__(self):
    super(day20, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.alg = None
    self.grid = [0, 0]
    self.image = gridutils.Grid(
        default_cell='0',
        in_map={'.': '0', '#': '1'})


  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    if not line:
      return
    if self.alg is None:
      self.alg = line.replace('.', '0').replace('#', '1')
      return

    self.image.add_row(line)

    line = line.replace('.', '0')
    line = line.replace('#', '1')
    self.grid.append('00' + line + '00')

  def post_load(self):
    # called after all input is read
    assert len(self.alg) == 512

    filler = '0' * len(self.grid[2])
    self.grid[0] = filler
    self.grid[1] = filler
    self.grid.append(filler)
    self.grid.append(filler)
    self.w = len(filler) - 1
    self.h = len(self.grid) - 1

  def print_grid(self):
    self.image.print(margin=2)
    # for row in self.grid:
    #  print(row)

  def part1(self):
    print('===== Start part 1')
    self.reset()


    if self.trace_sample:
      self.print_grid()

    self.mx = self.image.min_x - 12
    self.my = self.image.min_y - 12
    self.xx = self.image.max_x + 13
    self.xy = self.image.max_y + 13

    for i in range(2):
      self.mx -= 1
      self.my -= 1
      self.xx += 1
      self.xy += 1
      self.cycle()
      if True or self.trace_sample:
        print('after cycle', i)
        self.print_grid()

    return count_pixels(self.image, skip=5)

  def cycle(self):
    i = self.image
    edge_grow = 3
    ni = gridutils.Grid(default_cell='0')
    #for y in range(i.min_y-edge_grow, i.max_y+edge_grow+1):
    #  for x in range(i.min_x-edge_grow, i.max_x+edge_grow+1):
    for y in range(self.my, self.xy):
      for x in range(self.mx, self.xx):
        b = ''.join([
            i.get(x+dx, y+dy)
            for dx, dy in [(-1, -1), (0, -1), (1, -1),
                           (-1,  0), (0,  0), (1,  0),
                           (-1,  1), (0,  1), (1,  1)]])
        index = int(b, 2)
        # print(' index', x, y, index)
        ni.set(x, y, self.alg[index])
    self.image = ni

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day20.sample_test("""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""", expect1=35, expect2=None)
# input
####...###.###.##.##.##..###..##.#.##.#...####..##...#..#..#....#..#..##.##..#.#.####.######.#..#.##..##....#.####.##...#.#..#.####.#.#.#..###.##..#.#.#.#...#.....###.#.#...#..#....#######....#..#...###.##.........#.#.##.#........##...#..##.......####.#.#.#.#.#.####..#..........#.##......##......###.#..##.#.#.....###.#..#...###.##........#..#.##.#.###.#..#####..##..#..#.#.#...###..##..#.###.##...#.##.#.....#.#..........#..##.#########.#.#..##.#.##..######.....####...###..###.#..##########.#.#.....###.##.##.

# Merged
#.###.######.#.#.#.###.##.#...###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.###..#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#...
day20.sample_test("""
####...###.###.##.##.##..###..##.#.##.#...####..##...#..#..#....#..#..##.##..#.#.####.######.#..#.##..##....#.####.##...#.#..#.####.#.#.#..###.##..#.#.#.#...#.....###.#.#...#..#....#######....#..#...###.##.........#.#.##.#........##...#..##.......####.#.#.#.#.#.####..#..........#.##......##......###.#..##.#.#.....###.#..#...###.##........#..#.##.#.###.#..#####..##..#..#.#.#...###..##..#.###.##...#.##.#.....#.#..........#..##.#########.#.#..##.#.##..######.....####...###..###.#..##########.#.#.....###.##.##.

.....
.....
.....
.....
.....
""", expect1=None, expect2=None)

if __name__ == '__main__':
  # Not: 5414, 5274
  # 5286 is too high
  # 5698 is too high
  day20.run_and_check('input.txt', expect1=None, expect2=None)
