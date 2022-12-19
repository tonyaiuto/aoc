#!/usr/bin/env python3
"AOC 2021: day 18"

from tools import aoc

XL=0x01
XH=0x02
YL=0x04
YH=0x08
ZL=0x10
ZH=0x20

class Cube(object):

  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.open = 6
    self.ext_sides = 0

  def __str__(self):
    return str('%2d,%2d,%2d, free:%d' % (self.x, self.y, self.z, self.open))

  def point(self):
    return (self.x, self.y, self.z)

  def neighbors(self):
    return [(self.x-1, self.y,   self.z  ), (self.x+1, self.y,   self.z),
            (self.x,   self.y-1, self.z  ), (self.x  , self.y+1, self.z),
            (self.x,   self.y,   self.z-1), (self.x  , self.y,   self.z+1)]


class day18(aoc.aoc):

  def __init__(self):
    super(day18, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.cubes = []
    self.ci = {}
    # bounding box
    self.min_x = 100
    self.max_x = 0
    self.min_y = 100
    self.max_y = 0
    self.min_z = 100
    self.max_z = 0

  def do_line(self, line):
    # called for each line of input
    x, y, z = [int(p) for p in line.split(',')]
    cube = Cube(x, y, z)
    self.cubes.append(cube)
    self.ci[(x, y, z)] = cube
    self.min_x = min(self.min_x, x)
    self.max_x = max(self.max_x, x)
    self.min_y = min(self.min_y, y)
    self.max_y = max(self.max_y, y)
    self.min_z = min(self.min_z, z)
    self.max_z = max(self.max_z, z)

  def post_load(self):
    # called after all input is read
    #print('box-x', self.min_x, self.max_x)
    #print('box-y', self.min_y, self.max_y)
    #print('box-z', self.min_z, self.max_z)
    for c in self.cubes:
      assert self.ci.get((c.x, c.y, c.z)) == c

  def part1(self):
    print('===== Start part 1')
    ret = 0
    for c in self.cubes:
      for n in c.neighbors():
        other = self.ci.get(n)
        if other:
          c.open -= 1
      ret += c.open
    return ret

  def part2(self):
    visited = set()
    frontier = [(0, 0, 0)]
    self.surface = 0
    while len(frontier) > 0:
      new_f = self.do_frontier(frontier, visited)
      # print('f', frontier)
      # print('nf', new_f)
      # print('v', visited)
      frontier = new_f

    return self.surface


  def do_frontier(self, frontier, visited):
    new_f = set()
    for cell in frontier:
      if cell in visited:
        continue
      visited.add(cell)
      x = cell[0]
      y = cell[1]
      z = cell[2]

      if x >= 0:
        self.check_side(x-1, y, z, XH, new_f)
      if x <= self.max_x + 1:
        self.check_side(x+1, y, z, XL, new_f)
      if y >= 0:
        self.check_side(x, y-1, z, YH, new_f)
      if y <= self.max_y + 1:
        self.check_side(x, y+1, z, YL, new_f)
      if z >= 0:
        self.check_side(x, y, z-1, ZH, new_f)
      if z <= self.max_z + 1:
        self.check_side(x, y, z+1, ZL, new_f)
    return new_f


  def check_side(self, x, y, z, side, frontier):
    c = self.ci.get((x, y, z))
    if c and c.ext_sides & side == 0:
      c.ext_sides |= side
      self.surface += 1
    else:
      frontier.add((x, y, z))


  def part2_not_good(self):
    # single non-convex hull: no overlaps in z plane
    print('===== Start part 2')
   
    for x in range(self.min_x, self.max_x+1):
      for y in range(self.min_y, self.max_y+1):
        low_shell = None
        holes = []
        n_low = 0
        print('=== new z')
        for z in range(self.min_z, self.max_z+1):
          c = self.ci.get((x, y, z))
          if not c:
            if low_shell:
              holes.append((x, y, z))
          else:
            print('     cube', c)
            if not low_shell:
              low_shell = c
              n_low += 1
              print('low_shell', low_shell, '#####' if n_low > 1 else '')
            else:  #
              if holes:
                print('low_shell', low_shell, 'holes at', holes)
                low_shell = None
                for h in holes:
                  self.ci[h] = 1
                holes = []
        if holes:
          print('holes at', holes)
          for h in holes:
            self.ci[h] = 1

    big = self.part1()
    return big


day18.sample_test("""
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""", expect1=64, expect2=58)


if __name__ == '__main__':
  # part2 > 2541
  day18.run_and_check('input.txt', expect1=4348, expect2=2546)
