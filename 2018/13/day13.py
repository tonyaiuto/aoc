"""aoc 2018 day 13"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys


class Map(object):

  def __init__(this):
    this.width = 0
    this.height = 0
    this.rows = []

  def AddRow(this, text):
    this.rows.append(text)
    this.height += 1
    this.width = max(this.width, len(text))

  def Print(this, cars):
    for y in range(this.height):
      row = this.rows[y]
      out_row = ''
      for x in range(len(row)):
        car = cars.Get(x, y)
        if car:
          c = car.dir
        else:
          c = row[x]
        out_row += c
      print(out_row)


class Car(object):

  LEFT = '<'
  RIGHT = '>'
  UP = '^'
  DOWN = 'v'

  def __init__(this, x, y, initial_dir):
    this.x = x
    this.y = y
    this.dir = initial_dir
    this.turn_count = 0

  def __str__(this):
    return '%d,%d.%c' % (this.x, this.y, this.dir)

  def __lt__(this, other):
    return ((this.y < other.y) or (this.y == other.y and this.x < other.x))
  def __eq__(this, other):
    return this.y == other.y and this.x == other.x
  def __ne__(this, other):
    return not this == other
  def __gt__(this, other):
    return other < this
  def __ge__(this, other):
    return not this < other
  def __le__(this, other):
    return not other < this


class Cars(object):

  def __init__(this):
    this.cars = []
    this.pos = {}

  def Add(this, car):
    this.cars.append(car)
    this.pos[(car.x, car.y)] = car

  def Get(this, x, y):
    return this.pos.get((x,y))

  def MoveOrdered(this):
    for c in sorted(this.cars):
      yield c


def Load(inp):
  map = Map()
  cars = Cars()
  for line in inp:
    lastc = ''
    row = ''
    for x in range(len(line.strip())):
      c = line[x]
      if c == '<' or c == '>':
        row += '-'
        car = Car(x, map.height, c)
        cars.Add(car)
      elif c == '^' or c == 'v':
        row += '|'
        car = Car(x, map.height, c)
        cars.Add(car)
      else:
        row += c
    map.AddRow(row)
  return map, cars


def part1(map, cars):
  while True:
    pass


if __name__ == '__main__':
  verbose = False
  iarg = 1
  if sys.argv[iarg] == '-v':
    verbose = True
    iarg += 1
  with open(sys.argv[iarg]) as inp:
    map, cars = Load(inp)

  if verbose:
    print([str(c) for c in cars.cars])
    map.Print(cars)
    print([str(c) for c in cars.cars])
    print([str(c) for c in cars.MovedOrdered()])
  # part1(map, cars)
