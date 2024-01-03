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
    Brick.n_bricks = 0
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
      if self.doing_sample:
        print("Landed", brick)

  def compute_support(self):
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
              if self.doing_sample:
                print('%3s' % brick.name, 'supports', other.name, 'at', x, y, 'z', other.z)
              brick.supports.add(other)
              other.supported_by.add(brick)


  def part1(self):
    print('===== Start part 1')
    if self.doing_sample:
      for b in self.bricks:
        print(b)
    self.drop_them()
    self.compute_support()

    can_dis = set(self.bricks)
    for brick in self.bricks:
      if len(brick.supported_by) == 1:
        for sup in brick.supported_by:
          # print(sup, 'is only support for', brick)
          can_dis.discard(sup)

    ret = len(can_dis)
    for brick in can_dis:
      if len(brick.supports) == 0:
        continue
      # print("check", brick)
      for other in brick.supports:
        assert brick in other.supported_by
        assert len(other.supported_by) > 1
    return ret

  def part2(self):
    print('===== Start part 2')
    self.drop_them()
    self.compute_support()

    def do_the_chain(brick, dissed):
      more_dissed = []
      for other in brick.supports:
        who_holds_me_up = other.supported_by - dissed
        if len(who_holds_me_up) == 0:
          dissed.add(other)
          more_dissed.append(other)
      for other in more_dissed:
        do_the_chain(other, dissed)
      return len(dissed)

    ret = 0
    for brick in self.bricks:
      will_fall = set()
      dissed = set([brick])
      will_fall = do_the_chain(brick, dissed) - 1
      if self.doing_sample:
        print(brick.name, 'drops', will_fall)
      ret = ret + will_fall

    if ret <= 1213:
      print("TOO LOW", ret)
    return ret


day22.sample_test("""
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""", expect1=5, expect2=7, recreate=False)


if __name__ == '__main__':
  day22.run_and_check('input.txt', expect1=446, expect2=60287)
