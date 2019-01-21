"""aoc 2018 day 13"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys


_PART2 = False

class Map(object):

  def __init__(this):
    this.width = 0
    this.height = 0
    this.rows = []
    this.crash_x = -1
    this.crash_y = -1

  def AddRow(this, text):
    this.rows.append(text)
    this.height += 1
    this.width = max(this.width, len(text))

  def Get(this, x, y):
    return this.rows[y][x]

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
        if this.crash_x == x and this.crash_y == y:
          c = 'X'
        out_row += c
      print(out_row)
    print('')

  def Crash(this, x, y):
    global _PART2
    if _PART2:
      return
    this.crash_x = x
    this.crash_y = y


class Car(object):

  LEFT = '<'
  RIGHT = '>'
  UP = '^'
  DOWN = 'v'

  id = 1

  def __init__(this, x, y, initial_dir):
    Car.id += 1
    this.id = Car.id
    this.x = x
    this.y = y
    this.dir = initial_dir
    this.turn_count = 0

  def __str__(this):
    return '%d,%d.%c#%d' % (this.x, this.y, this.dir, this.id)

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

  def Move(this, map):

    if this.dir == Car.LEFT:
      this.x -= 1 
    elif this.dir == Car.RIGHT:
      this.x += 1 
    elif this.dir == Car.UP:
      this.y -= 1 
    elif this.dir == Car.DOWN:
      this.y += 1 
    else:
      raise ValueError('bad car direction: %s' % this)

    m = map.Get(this.x, this.y)

    if m == '|':
      if not (this.dir == Car.UP or this.dir == Car.DOWN):
        raise Exception('Impossible move on | for %s' % this)
    elif m == '-':
      if not (this.dir == Car.LEFT or this.dir == Car.RIGHT):
        raise Exception('Impossible move on - for %s' % this)
    elif m == '/':
      if this.dir == Car.UP:
        this.dir = Car.RIGHT
      elif this.dir == Car.DOWN:
        this.dir = Car.LEFT
      elif this.dir == Car.LEFT:
        this.dir = Car.DOWN
      elif this.dir == Car.RIGHT:
        this.dir = Car.UP
      else:
        raise Exception('Impossible move on / for %s' % this)
    elif m == '\\':
      if this.dir == Car.UP:
        this.dir = Car.LEFT
      elif this.dir == Car.DOWN:
        this.dir = Car.RIGHT
      elif this.dir == Car.LEFT:
        this.dir = Car.UP
      elif this.dir == Car.RIGHT:
        this.dir = Car.DOWN
      else:
        raise Exception('Impossible move on / for %s' % this)
    elif m == '+':
       this.Turn()
    else:
      raise Exception('Impossible map marking %c' % m)


  def Turn(this):
    ret = None
    if this.turn_count % 3 == 0:
      # turn left
      if this.dir == Car.LEFT:
        this.dir = Car.DOWN
      elif this.dir == Car.RIGHT:
        this.dir = Car.UP
      elif this.dir == Car.UP:
        this.dir = Car.LEFT
      elif this.dir == Car.DOWN:
        this.dir = Car.RIGHT
      else:
        assert Exception('WTF')
    elif this.turn_count % 3 == 2:
      # turn right
      if this.dir == Car.LEFT:
        this.dir = Car.UP
      elif this.dir == Car.RIGHT:
        this.dir = Car.DOWN
      elif this.dir == Car.UP:
        this.dir = Car.RIGHT
      elif this.dir == Car.DOWN:
        this.dir = Car.LEFT
      else:
        assert Exception('WTF')
    this.turn_count += 1

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

  def Turn(this, map):
    print('=== %d cars left' % len(this.cars))
    ret = None
    to_drop = []
    for car in this.MoveOrdered():
      old_x = car.x
      old_y = car.y
      car.Move(map)
      del this.pos[(old_x, old_y)]
      other_car = this.pos.get((car.x, car.y))
      if other_car:
        map.Crash(car.x, car.y)
        ret = 'Crash: %d,%d = %s,%s' % (car.x, car.y, car, other_car)
        to_drop.append(other_car)
        to_drop.append(car)
      else:
        this.pos[(car.x, car.y)] = car
    for car in to_drop:
      print('Droping car: %s' % car)
      if (car.x, car.y) in this.pos:
        del this.pos[(car.x, car.y)]
    if to_drop:
      new_car_list = []
      for car in this.cars:
        if not car in to_drop:
          new_car_list.append(car)
      this.cars = new_car_list
    return ret

def Load(inp):
  map = Map()
  cars = Cars()
  for line in inp:
    lastc = ''
    row = ''
    for x in range(len(line)):
      c = line[x]
      if c == '<' or c == '>':
        row += '-'
        car = Car(x, map.height, c)
        cars.Add(car)
      elif c == '^' or c == 'v':
        row += '|'
        car = Car(x, map.height, c)
        cars.Add(car)
      elif c != '\n':
        row += c
    map.AddRow(row)
    # print('loaded "%sXXX"' % row)
  # print("last is '%s'" % line)
  return map, cars


# stop on first crash
def part1(map, cars, verbose):
  while True:
    crash = cars.Turn(map)
    # print([str(c) for c in cars.MoveOrdered()])
    if verbose:
      map.Print(cars)
    if crash:
      print(crash)
      break


# stop on last cart
def part2(map, cars, verbose):
  while len(cars.cars) > 1:
    crash = cars.Turn(map)
    if verbose:
      map.Print(cars)
    if crash:
      print(crash)
  
  print('Last car is %s' % cars.cars[0])
  crash = cars.Turn(map)
  print('Final pos is %s' % cars.cars[0])


if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      do_part2 = True
      _PART2 = True
      iarg += 1
  with open(sys.argv[iarg]) as inp:
    map, cars = Load(inp)

  if verbose:
    print([str(c) for c in cars.cars])
    map.Print(cars)
    # print([str(c) for c in cars.cars])
    # print([str(c) for c in cars.MoveOrdered()])
  if do_part2:
    part2(map, cars, verbose)
  else:
    part1(map, cars, verbose)
