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
    this.res_to_gen = {}
    this.gen_to_res = {}
    this.last_periods = [0] * 5

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
    # Multiplying the number of wooded acres by the number of lumberyards
    # gives the total resource value after ten minutes: 37 * 31 = 1147.
    ny = nt = 0
    for y in range(1, this.height+1):
      for x in range(1, this.width+1):
        cell = this.rows[y][x]
        if cell == Forest.TREES:
          nt += 1
        elif cell == Forest.YARD:
          ny += 1
    res = nt * ny
    print('gen:%d, wooded:%d, yards:%d => %d' % (this.gen, nt, ny, nt * ny))
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
    start = time.time()
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
    finish = time.time()
    this.gen_time = int(finish - start)

    ny = nt = 0
    for y in range(1, this.height+1):
      for x in range(1, this.width+1):
        cell = this.rows[y][x]
        if cell == Forest.TREES:
          nt += 1
        elif cell == Forest.YARD:
          ny += 1
    res = nt * ny
    this.gen_to_res[this.gen] = res

    o_gen = this.res_to_gen.get(res)
    if o_gen:
      s_period = this.gen - o_gen
      print('Suspect period of %d at gen %d' % (s_period, this.gen))
      found = True
      for p in this.last_periods:
        if p != s_period:
          found = False
          break
      if found:
        print('This is it')
        target = 1000000000 
        #  gen + period * N = target
        N = int((target - this.gen) / s_period) + 1
        #  period * N = target - gen
        want_gen = target - s_period * N
        print('res at gen %d => %d' % (want_gen, this.gen_to_res[want_gen]))
        sys.exit(0)
      this.last_periods = this.last_periods[1:] + [s_period]
    this.res_to_gen[res] = this.gen


def part1(forest):
  for i in range(10):
    forest.Gen()
    forest.Print()

def part2_phase1(forest):
  for l in range(10):
    start = time.time()
    for i in range(1000):
      forest.Gen()
    forest.Print()
    finish = time.time()
    print('speed: %d/1000' % int(finish - start))

def part2(forest):
  for l in range(10):
    start = time.time()
    for i in range(100):
      forest.Gen()
    forest.Print()
    finish = time.time()
    print('speed: %d' % int(finish - start))


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

  if do_part2:
    part2(forest)
  else:
    part1(forest)
