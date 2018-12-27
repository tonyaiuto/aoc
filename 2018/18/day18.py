"""aoc 2018 day 12"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import sys
import time


class Forest(object):

  OPEN = '.'
  TREES = '|'
  YARD = '#'

  def __init__(this):
    this.gen = 0
    this.width = 0
    this.height = 0
    this.rows = [None]

  @staticmethod
  def Load(inp):
    that = Forest()
    for line in inp:
      that.rows.append([' '] + [c for c in line.strip()] + [' '])
      that.height += 1
    that.width = len(that.rows[1]) - 2
    dummy_row = [' '] * (that.width + 2)
    that.rows[0] = dummy_row
    that.rows.append(dummy_row)
    return that

  def Print(this):
    print('gen:%d' % this.gen)
    for y in range(1, this.height+1):
      print(''.join(this.rows[y][1:this.width+1]))


  def Gen(this):
    # An open acre will become filled with trees if three or more adjacent
    # acres contained trees. Otherwise, nothing happens.  An acre filled
    # with trees will become a lumberyard if three or more adjacent acres
    # were lumberyards. Otherwise, nothing happens.  An acre containing
    # a lumberyard will remain a lumberyard if it was adjacent to at least
    # one other lumberyard and at least one acre containing trees.
    # Otherwise, it becomes open.  These changes happen across all acres
    # simultaneously, each of them using the state of all acres at the
    # beginning of the minute and changing to their new form by the end
    # of that same minute. Changes that happen during the minute don't
    # affect each other.
    this.gen += 1
    nboard = [this.rows[0]]
    for y in range(1, this.height+1):
      nrow = [' ']
      for x in range(1, this.width+1):
        nt = ny = 0
        for dx, dy in [ (-1, -1), (0, -1), (1, -1),
                        (-1, 0),          (1, 0),
                        (-1, 1), (0, 1), (1, 1)]:
          cell = this.rows[y+dy][x+dx]
          if cell == Forest.TREES:
            nt += 1
          elif cell == Forest.YARD:
            ny += 1
        cell = this.rows[y][x]
        if cell == Forest.OPEN and nt >= 3:
          cell = Forest.TREES
        elif cell == Forest.TREES and ny >= 3:
          cell = Forest.YARD
        elif cell == Forest.YARD:
          if nt < 1 or ny < 1:
            cell = Forest.OPEN
        nrow.append(cell) 
      nrow.append(' ')
      nboard.append(nrow)
    nboard.append(this.rows[0])
    this.rows = nboard


def part1(forest):
  for i in range(10):
    forest.Gen()
    forest.Print()
  # Multiplying the number of wooded acres by the number of lumberyards
  # gives the total resource value after ten minutes: 37 * 31 = 1147.
  ny = nt = 0
  for y in range(1, forest.height+1):
    for x in range(1, forest.width+1):
      cell = forest.rows[y][x]
      if cell == Forest.TREES:
        nt += 1
      elif cell == Forest.YARD:
        ny += 1
  print('gen:%d, wooded:%d, yards:%d => %d' % (forest.gen, nt, ny, nt * ny))


if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-2':
      do_part2 = True
      iarg += 1
    elif sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    else:
      break
  with open(sys.argv[iarg]) as inp:
    forest = Forest.Load(inp)
  forest.Print()

  part1(forest)
