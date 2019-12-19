#!/usr/bin/env python3

import sys
import textwrap

# from elf_image import ElfImage
import intcode

class Droid(object):

  def __init__(self, program):
    self.program = list(program)
    self.probed = {}

  def probe(self, x, y):
    pos = (x, y)
    tractor = self.probed.get(pos) or -1
    if tractor < 0:
      droid = intcode.IntCode(list(self.program))
      droid.push_input([x, y])
      tractor = droid.run_until_output()
      self.probed[pos] = tractor
    return tractor


def part1():
  program = intcode.load_intcode('input_19.txt')
  droid = Droid(program)

  n_pulled = 0
  for y in range(50):
    for x in range(50):
      tractor = droid.probe(x, y)
      if tractor == 1:
        n_pulled += 1
        print(x, y, tractor)

  print('part1:', n_pulled)
  assert 189 == n_pulled


def span_on_line(droid, y, x_start=1):
  # find start and width of line on row y
  x = x_start
  x_end = x_start + 1000
  n_in_row = 0
  while x < x_end:
    tractor = droid.probe(x, y)
    # print(x, y, tractor)
    if tractor == 1:
      if n_in_row == 0:
        n_x = x
        x = x + 90
        n_in_row = 90
      n_in_row += 1
      x_end = x + 20
    else:
      if n_in_row > 1:
        n_in_row = x - n_x
        # print('(%3d, %3d) for %2d need (%3d, %3d)' % (
        #    n_x, y, n_in_row, n_x + n_in_row - 100, y+100))
        return n_x, n_in_row
    x = x + 1


def part2():
  program = intcode.load_intcode('input_19.txt')
  droid = Droid(program)

  probed = {}
  # (415, 621) for 99 need (414, 721)
  # (1185, 1774) for 281 need (1366, 1874)
  y = 1750
  x_start = 1150

  y = 870
  x_start = 500

  x_end = x_start + 200
  need = set()
  while y < 3000:
    n_in_row = 0
    x, n_in_row = span_on_line(droid, y, x_start)
    print('row', y, x, n_in_row)
    if n_in_row > 100:
      bottom_x = x + n_in_row - 100
      bottom_y = y + 99
      msg = '(%3d, %3d) for %2d need (%3d, %3d)' % (
          x, y, n_in_row, bottom_x, bottom_y)
      lower_x, lower_n_in_row = span_on_line(droid, bottom_y, x_start)
      print(msg, '=> (%d, %d) for %d' % (lower_x, bottom_y, lower_n_in_row))

      shift = lower_x - bottom_x
      if shift == 0:
        print(msg, ': win at ', bottom_x, y)
        win = bottom_x * 10000 + y
        break
      elif shift < 0:
        print(msg, ': back up at', bottom_x, bottom_y, shift)
      else:
        if shift > 10:
          print(msg, ': not possible, shifting down', shift)
          y += (shift - 2)

      if (x, y) in need:
        print('found match: lower left=', x, y)
        return
      need.add((x + n_in_row - 100, y+100))
    y = y + 1

  print('part2:', win)
  assert 7621042 == win


if __name__ == '__main__':
  # part1()
  part2()
