"AOC 2020: day 17"

from collections import defaultdict
import itertools
import math

from tools import reader
from tools import elf_image


def sample_test(s, expect, expect2=None):
  puzz = day17()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day17()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day17()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day17()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Cube(object):

  def __init__(self, map):
    self.cycle = 0
    self.state = set()
    self.active = 0
    self.hyper = False

    # print(map)
    w = 0
    z = 0
    y = 0
    for row in map:
      x = 0
      for c in row:
        if c == '#':
          self.state.add((w,x,y,z))
        x += 1
      y += 1
    self.print()

  def __str__(self):
    return str(self.state)

  def print(self):
    print('==== cycle %d, %d active' % (self.cycle, self.active))
    self.get_bounds()
    self.printz(0)

  def printz(self, z):
    for y in range(self.min_y, self.max_y+1):
      l = ''
      for x in range(self.min_x, self.max_x+1):
        if (0,x,y,z) in self.state:
          l += '#'
        else:
          l += '.'
      print(l)

  def get_bounds(self):
    self.min_w = 0
    self.max_w = 0
    self.min_x = 0
    self.max_x = 0
    self.min_y = 0
    self.max_y = 0
    self.min_z = 0
    self.max_z = 0
    for w,x,y,z in self.state:
      self.min_w = min(self.min_w, w)
      self.max_w = max(self.max_w, w)
      self.min_x = min(self.min_x, x)
      self.max_x = max(self.max_x, x)
      self.min_y = min(self.min_y, y)
      self.max_y = max(self.max_y, y)
      self.min_z = min(self.min_z, z)
      self.max_z = max(self.max_z, z)


  def do_cycle(self):
    self.cycle += 1
    self.get_bounds()
    ns = set()
    active = 0
    if self.hyper:
      w_range = [i for i in range(self.min_w-1, self.max_w+2)]
    else:
      w_range = [0]
    for z,y,x,w in itertools.product(
        range(self.min_z-1, self.max_z+2),
        range(self.min_y-1, self.max_y+2),
        range(self.min_x-1, self.max_x+2),
        w_range):
      is_active = (w,x,y,z) in self.state
      tot = self.count_near(w, x, y, z)
      if is_active:
        #if z == 0:
        #  print(w,x,y,z, 'active, #neigh', tot)
        if tot == 2 or tot == 3:
          ns.add((w,x,y,z))
          active += 1
      elif tot == 3:
        #if z == 0:
        #  print(w,x,y,z, 'inactive, #aeigh', tot)
        ns.add((w,x,y,z))
        active += 1
    self.state = ns
    self.active = active

  def count_near(self, w, x, y, z):
    tot = 0
    if self.hyper:
      w_range = [w-1, w, w+1]
    else:
      w_range = [0]
    for dz,dy,dx,dw in itertools.product(
        [z-1, z, z+1],
        [y-1, y, y+1],
        [x-1, x, x+1],
        w_range):
      if (dw, dx, dy, dz) != (w, x, y, z):
        if (dw,dx,dy,dz) in self.state:
          #if self.cycle < 2:
          #  print(dw,dx,dy,dz, 'tot', tot)
          tot += 1
          if tot > 3:
            break
    return tot


class day17(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True

  def reset(self):
    pass

  def load_file(self, file):
    all = reader.FileReader(file).load()
    self.cube = Cube(all)

  def load_str(self, s):
    all = reader.StringReader(s).load()
    self.cube = Cube(all)

  def do_line(self, line):
    pass

  def post_load(self):
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    for c in range(6):
      self.cube.do_cycle()
      self.cube.print()

    self.result1 = self.cube.active
    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.cube.hyper = True
    for c in range(6):
      self.cube.do_cycle()
      self.cube.print()
    self.result2 = self.cube.active

    print('part2', self.result2)
    return self.result2



sample_test("""
.#.
..#
###
""", 112, 848)



if __name__ == '__main__':
  main('input.txt', 298, 1792)
  pass
