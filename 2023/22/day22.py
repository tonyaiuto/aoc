#!/usr/bin/env python3
"AOC 2023: day 22"

from collections import defaultdict
import copy
import heapq
import itertools
from operator import attrgetter

from tools import aoc
from tools import gridutils

X = 0
Y = 1
Z = 2


class Brick(object):

  n_bricks = 0

  def __init__(self, s):
    tmp = s.split('~')
    a = tuple([int(x) for x in tmp[0].split(',')])
    b = tuple([int(x) for x in tmp[1].split(',')])
    if a[Z] <= b[Z]:
      self.a = a
      self.b = b
    else:
      self.a = b
      self.b = a
    self.z = self.a[Z]
    self.height = self.b[Z] - self.a[Z] + 1
    n = Brick.n_bricks
    Brick.n_bricks += 1
    self.name = ""
    while True:
      c = chr(ord("A") + (n % 26))
      self.name = self.name + c
      n = n // 26
      if n == 0:
        break
    self.supports = set()
    self.supported_by = set()

  def __repr__(self):
    return str(self)

  def __str__(self):
    return '%-3s %3d,%3d,%3d - %3d,%3d,%3d @ %3d' % (self.name,
        self.a[X], self.a[Y], self.a[Z], self.b[X], self.b[Y], self.b[Z],
        self.z)


class day22(aoc.aoc):

  def __init__(self):
    super(day22, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.bricks = []
    self.space = set()

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    brick = Brick(line)
    self.bricks.append(brick)
    for x in aoc.visit_range(brick.a[X], brick.b[X]):
      for y in aoc.visit_range(brick.a[Y], brick.b[Y]):
        for z in aoc.visit_range(brick.a[Z], brick.b[Z]):
          self.space.add((x, y, z))

  def post_load(self):
    # order by Z
    self.bricks = sorted(self.bricks, key=attrgetter('z'))

  def drop_them(self):
    filled = {}
    self.occupied = defaultdict(list)
    height = {}
    at_z = 0
    last_z = -1
    for brick in self.bricks:
      assert brick.z >= last_z
      last_z = brick.z

      to_h = 0
      for x in aoc.visit_range(brick.a[X], brick.b[X]):
        for y in aoc.visit_range(brick.a[Y], brick.b[Y]):
          assert brick not in self.occupied[(x,y)]
          self.occupied[(x,y)].append(brick)
          to_h = max(to_h, height.get((x, y), 0))
      brick.z = to_h + 1
      for x in aoc.visit_range(brick.a[X], brick.b[X]):
        for y in aoc.visit_range(brick.a[Y], brick.b[Y]):
          height[(x,y)] = to_h + brick.height
          # Make sure we are not screwing up
          for z in range(brick.z, brick.z + brick.height):
            clash = filled.get((x, y, z))
            if clash:
              print("CLASH", clash, brick)
              assert False
            filled[(x, y, z)] = brick
      print("Landed", brick)


  def part1(self):
    print('===== Start part 1')
    if True or self.doing_sample:
      for b in self.bricks:
        print(b)
    self.drop_them()

    for brick in self.bricks:
      for x in aoc.visit_range(brick.a[X], brick.b[X]):
        for y in aoc.visit_range(brick.a[Y], brick.b[Y]):
          oz = -1
          foo = False
          for other in self.occupied[(x,y)]:
            # assert that it is sorted
            assert other.z >= oz
            oz = other.z

            if other == brick:
              continue
            assert other.z != brick.z

            if other.z == brick.z + brick.height:
              print('%3s' % brick.name, 'supports', other.name, 'at', x, y, 'z', other.z)
              brick.supports.add(other)
              other.supported_by.add(brick)
            """
            if other.z < brick.z:
              # print('does', brick.name, 'is above', other)
              if foo:
                print('got low brick', other, 'after supporting ', brick)
              continue
            elif other.z == brick.z:
              print('ERR collision', brick, other)
              assert False
            elif other.z == brick.z + 1:
              print('%3s' % brick.name, 'supports', other.name, 'at', x, y, 'z', other.z)
              brick.supports.add(other)
              other.supported_by.add(brick)
            elif other.z > brick.z + 1:
              # print('does', brick.name, 'cant support anything else at', x, y)
              foo = True
              continue
            """

    can_dis = set(self.bricks)
    for brick in self.bricks:
      if len(brick.supported_by) == 1:
        for sup in brick.supported_by:
          print(sup, 'is only support for', brick)
          can_dis.discard(sup)

    ret = len(can_dis)
    if ret >= 503:
      print("TOO HIGH", ret)
    for brick in can_dis:
      if len(brick.supports) == 0:
        continue
      print("check", brick)
      for other in brick.supports:
        assert brick in other.supported_by
        assert len(other.supported_by) > 1
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day22.sample_test("""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""", expect1=5, expect2=333)


if __name__ == '__main__':
  day22.run_and_check('input.txt', expect1=446, expect2=None)
