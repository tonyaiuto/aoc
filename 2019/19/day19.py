#!/usr/bin/env python3

import sys
import textwrap

# from elf_image import ElfImage
import intcode


def part1():
  mem = intcode.load_intcode('input_19.txt')
  n_pulled = 0
  for y in range(50):
    for x in range(50):
      droid = intcode.IntCode(list(mem))
      droid.push_input([x, y])
      out = droid.run_until_output()
      if out == 1:
        n_pulled += 1
        print(x, y, out)

  print('part1:', n_pulled)
  assert 189 == n_pulled




def part2():
  mem = intcode.load_intcode('input_19.txt')
  probed = {}
  # (415, 621) for 99 need (414, 721)
  # (1185, 1774) for 281 need (1366, 1874)
  y = 1700
  next_start = 1100
  x_end = next_start + 200
  need = set()
  while y < 3000:
    n_in_row = 0
    x = next_start
    while x < x_end:
      #tractor = probed.get((x, y)) or -1
      #if tractor < 0:
      droid = intcode.IntCode(list(mem))
      droid.push_input([x, y])
      tractor = droid.run_until_output()
      # probed[(x, y)] = tractor

      # print(x, y, tractor)
      if tractor == 1:
        if n_in_row == 0:
          n_x = x
          next_start = x
          n_y = y
          x = x + 90
          n_in_row = 90
        n_in_row += 1
        x_end = x + 20
      else:
        if n_in_row > 100:
          n_in_row = x - n_x
          print('(%3d, %3d) for %2d need (%3d, %3d)' % (
              n_x, n_y, n_in_row, n_x + n_in_row - 100, n_y+100))
          n_in_row = 0
          if (n_x, n_y) in need:
            print('found match: lower left=', n_x, n_y)
            return
          need.add((n_x + n_in_row - 100, n_y+100))
         
      x = x + 1
    y = y + 1

  # print('part2:', n_pulled)
  # assert 189 == n_pulled


if __name__ == '__main__':
  # part1()
  part2()
