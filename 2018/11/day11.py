from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import sys

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)


@memoized
def Power(x, y, serial):
  x1 = x + 10
  h = int((((x1 * y) + serial) * x1) / 100) % 10
  return h - 5


def SquarePower(x, y, size, serial):
  sum = 0
  for xi in range(size):
    for yi in range(size):
      sum += Power(x+xi, y+yi, serial)
  return sum

@memoized
def ColumnPower(x, to_y, serial):
  sum = 0
  for y in range(1, to_y):
    p = Power(x, y, serial)
    sum += p
    # print('cp %d,%d (%d) => %s' % (x, y, p, sum))
  return sum

@memoized
def RowPower(to_x, y, serial):
  sum = 0
  for x in range(1, to_x):
    sum += Power(x, y, serial)
  return sum

@memoized
def IncrementalSquarePower(x, y, size, serial, verbose=False):
  # size = current size
  # add x+size for all y
  # add y+size for all x
  if size == 0:
    return 0
  if size == 1:
    return Power(x, y, serial)

  power = IncrementalSquarePower(x, y, size-1, serial)
  #for i in range(size):
  #  # print('add %d,%d' % (x+i, y+size))
  #  power += Power(x+i, y+size, serial)
  #  # print('add %d,%d' % (x+size, y+i))
  #  power += Power(x+size, y+i, serial)

  cp = ColumnPower(x+size-1, y+size-1, serial) - ColumnPower(x+size-1, y, serial)
  rp = RowPower(x+size-1, y+size-1, serial) - RowPower(x, y+size-1, serial)
  corner = Power(x+size-1, y+size-1, serial)
  # print('add corner %d,%d' % (x+size, y+size))
  ret = power + cp + rp + corner
  if verbose:
    print("isp: %d,%d x %d, power:%d + cp:%d + rp:%d + %d => %d" % (
        x, y, size, power, cp, rp, corner, ret))
  return ret


def Part1Best(serial):
  best_x = best_y = 1
  max_power = -100
  for x in range(1, 298):
    for y in range(1, 298):
      p = SquarePower(x, y, 3, serial)
      if p > max_power:
        max_power = p
        best_x = x
        best_y = y
  return best_x, best_y, max_power


def tests():
  assert Power(3, 5, 8) == 4
  assert Power(122, 79, 57) == -5
  assert Power(217, 196, 39) == 0
  assert Power(101, 153, 71) == 4

  assert ColumnPower(2, 5, 18) == 1
  assert ColumnPower(2, 10, 18) == -5 
  # -1  4 -1  4  0 -4  2 -1 -3  4  2 0 -1 -2 -2 -2 -2 -1  0  1
  assert RowPower(10, 19, 18) == 0
  assert RowPower(21, 19, 18) == -3

  print('.test ISP')
  assert IncrementalSquarePower(21, 61, 1, 42, True) == 4
  assert IncrementalSquarePower(21, 61, 2, 42, True) == 13
  assert IncrementalSquarePower(21, 61, 3, 42, True) == 30
  assert IncrementalSquarePower(33, 45, 3, 18, True) == 29

  x, y, width, p = part2(18, grid_max=50, width_max=3)
  print('part2(18, 50) => %d,%d x %d == %d' % (x, y, width, p))
  assert (x, y, width) == (33, 45, 3)


def part1():
  ans = Part1Best(5719)
  print(ans)
  assert ans == (21, 34, 29)


def part2(serial, grid_max=300, width_max=300):
  best_x = best_y = best_width = 1
  max_power = -100
  for y in range(1, grid_max+1):
    print('row %d' % y)
    for x in range(1, grid_max+1):
      sq_power = IncrementalSquarePower(x, y, 1, serial)
      if sq_power > max_power:
        max_power = sq_power
        best_x = x
        best_y = y
        best_width = 1
      size_max = min(grid_max+1 - x, grid_max+1 - y, width_max+1)
      if x % 50 == 1:
        print('  col %d, size_max=%d' % (x, size_max))
      for o_size in range(2, size_max):
        verbose = x % 10 == 0 and y % 10 == 0
        sq_power = IncrementalSquarePower(x, y, o_size, serial, verbose)
        if sq_power > max_power:
          max_power = sq_power 
          best_x = x
          best_y = y
          best_width = o_size
          print('=> new max at %d,%d size:%d = %d' % (best_x, best_y,
                                                      best_width, max_power))
  print('serial %d => %d,%d x %d power:%d' % (serial, best_x, best_y,
                                              best_width, max_power))
  return best_x, best_y, best_width, max_power


def showgrid(size, serial):
  for y in range(1, size+1):
    for x in range(1, size+1):
      sys.stdout.write(' %2d' % Power(x, y, serial))
    print('')

if __name__ == '__main__':
  # showgrid(20, 18)
  tests()
  # part1()

  x, y, s, m = part2(5719)
