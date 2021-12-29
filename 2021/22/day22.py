#!/usr/bin/env python3
"AOC 2021: day 22"

from collections import defaultdict
import copy
import heapq
import itertools
import math
import sys

from tools import aoc
from tools import gridutils
from tools import qparser


class Cube(object):

  def __init__(self, n=-1, x_low=0, x_high=0, y_low=0, y_high=0, z_low=0, z_high=0):
    self.on_off = 'off'
    self.n = n
    self.x_low = x_low
    self.x_high = x_high
    self.y_low = y_low
    self.y_high = y_high
    self.z_low = z_low
    self.z_high = z_high
    self.validate()

  def validate(self):
    assert self.on_off in ('on', 'off')
    assert self.x_low <= self.x_high
    assert self.y_low <= self.y_high
    assert self.z_low <= self.z_high

    self.on = self.on_off == 'on'
    self.volume = ((self.x_high - self.x_low + 1)
                   * (self.y_high - self.y_low + 1)
                   * (self.z_high - self.z_low + 1))

  def __str__(self):
    return str('%s  %d..%d, %d..%d, %d..%d' % (
        'on' if self.on else 'off', self.x_low, self.x_high, self.y_low, self.y_high, self.z_low, self.z_high))

  def intersect(self, other):
    xl = max(self.x_low, other.x_low)
    yl = max(self.y_low, other.y_low)
    zl = max(self.z_low, other.z_low)
    xh = min(self.x_high, other.x_high)
    yh = min(self.y_high, other.y_high)
    zh = min(self.z_high, other.z_high)
    if xl > xh or yl > yh or zl > zh:
      return None
    overlap = Cube(x_low=xl, x_high=xh, y_low=yl, y_high=yh, z_low=zl, z_high=zh)
    assert overlap.volume <= self.volume
    assert overlap.volume <= other.volume
    return overlap

  def points(self, clamp):
     for x,y,z in itertools.product(
         range(max(self.x_low, -clamp), min(self.x_high+1, clamp+1)),
         range(max(self.y_low, -clamp), min(self.y_high+1, clamp+1)),
         range(max(self.z_low, -clamp), min(self.z_high+1, clamp+1))):
       yield x, y, z

  def chopout(self, other):
    """Return cubiods that would result from removing other from self."""

    xl = max(self.x_low, other.x_low)
    yl = max(self.y_low, other.y_low)
    zl = max(self.z_low, other.z_low)
    xh = min(self.x_high, other.x_high)
    yh = min(self.y_high, other.y_high)
    zh = min(self.z_high, other.z_high)
    # Make sure we really intersect
    assert xl <= xh and yl <= yh and zl <= zh

    reduced = copy.copy(self)
    ret = []
    #  self...
    #    other...
    #  NC
    if self.x_low < other.x_low:
      nc = Cube(x_low=reduced.x_low, x_high=other.x_low-1,
                y_low=reduced.y_low, y_high=reduced.y_high,
                z_low=reduced.z_low, z_high=reduced.z_high)
      reduced.x_low = other.x_low
      ret.append(nc)
    #  .....self
    #  ..other..
    #         NC
    if self.x_high > other.x_high:
      nc = Cube(x_low=other.x_high+1, x_high=reduced.x_high,
                y_low=reduced.y_low, y_high=reduced.y_high,
                z_low=reduced.z_low, z_high=reduced.z_high)
      reduced.x_high = other.x_high
      ret.append(nc)
    if self.y_low < other.y_low:
      nc = Cube(x_low=reduced.x_low, x_high=reduced.x_high,
                y_low=reduced.y_low, y_high=other.y_low-1,
                z_low=reduced.z_low, z_high=reduced.z_high)
      reduced.y_low = other.y_low
      ret.append(nc)
    if self.y_high > other.y_high:
      nc = Cube(x_low=reduced.x_low, x_high=reduced.x_high,
                y_low=other.y_high+1, y_high=reduced.y_high,
                z_low=reduced.z_low, z_high=reduced.z_high)
      reduced.y_high = other.y_high
      ret.append(nc)
    if self.z_low < other.z_low:
      nc = Cube(x_low=reduced.x_low, x_high=reduced.x_high,
                y_low=reduced.y_low, y_high=reduced.y_high,
                z_low=reduced.z_low, z_high=other.z_low-1)
      reduced.z_low = other.z_low
      ret.append(nc)
    if self.z_high > other.z_high:
      nc = Cube(x_low=reduced.x_low, x_high=reduced.x_high,
                y_low=reduced.y_low, y_high=reduced.y_high,
                z_low=other.z_high+1, z_high=reduced.z_high)
      reduced.z_high = other.z_high
      ret.append(nc)

    reduced.validate()
    nv = sum([c.volume for c in ret])
    assert nv + reduced.volume == self.volume, 'FOO'
    return ret



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
    self.parser = qparser.QParser([
        qparser.Text('on_off'),
        qparser.Literal('x='),
        qparser.Number('x_low'),
        qparser.Literal('..'),
        qparser.Number('x_high'),

        qparser.Literal(','),

        qparser.Literal('y='),
        qparser.Number('y_low'),
        qparser.Literal('..'),
        qparser.Number('y_high'),

        qparser.Literal(','),

        qparser.Literal('z='),
        qparser.Number('z_low'),
        qparser.Literal('..'),
        qparser.Number('z_high'),
    ])
    self.cubes = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    cube = Cube(n=len(self.cubes))
    self.parser.parse(cube, line)
    cube.validate()
    print(cube)
    self.cubes.append(cube)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.core = set()
    for c in self.cubes:
      self.flip(c)

    return len(self.core)

  def flip(self, c):
    if c.on:
      for x,y,z in c.points(clamp=50):
        self.core.add((x,y,z))
    else:
      for x,y,z in c.points(clamp=50):
        self.core.discard((x,y,z))

  def part2(self):
    print('===== Start part 2')
    self.reset()

    tot_on = 0
    turned_on = []
    turned_off = []
    on_overlaps = []
    for c in self.cubes:
      if c.on:
        print('--', c.n, ':', c, 'volume:', c.volume)
        new_on = c.volume
        n_over = []
        for other in turned_on:
          overlap = c.intersect(other)
          if overlap:
            assert other.on
            print('  overlap %d,%d: reducing %d by %d' % (
                c.n, other.n, new_on, overlap.volume))

            r = c.chopout(overlap)
            new_on -= overlap.volume
            n_over.append(overlap)
            if overlap.volume >= c.volume:
              print('  ', c, 'is containtained in', other)
              new_on = -1
              break
            if new_on <= 0:
              print('  ', c, 'is consumed')
              break
        for other in turned_off:
          overlap = c.intersect(other)
          if overlap:
            assert not other.on
            print('  overlap off region %d,%d: reducing %d by %d' % (
                c.n, other.n, new_on, overlap.volume))
          

        if new_on > 0:
          tot_on += new_on
          turned_on.append(c)
          on_overlaps.extend(n_over)
      else:
        new_off = 0
        for other in turned_on:
          overlap = c.intersect(other)
          if overlap:
            assert other.on
            new_off += overlap.volume
            turned_off.append(overlap)

            # off_overlaps.append(overlap)

        for oo in overlaps(c, on_overlaps):
          new_off -= oo.volume

        #for oo in overlaps(c, turned_off):
        #  new_off -= oo.volume


        if new_off > 0:
          tot_on -= new_off
          turned_off.append(c)
    return tot_on


def overlaps(c, cubes):
  ret = []
  for other in cubes:
    nc = c.intersect(other)
    if nc:
      ret.append(nc)
  return ret


day22.sample_test("""
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""", expect1=39, expect2=None)

day22.sample_test("""
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""", expect1=590784, expect2=None)


day22.sample_test("""
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
""", expect1=474140, expect2=2758514936282235)
#                            13384162962341495
#                            2520680994726215
#                            4138427008945247
#                            4629186521757653
#                            3833378129870011
#                            668816323008700

if __name__ == '__main__':
  day22.run_and_check('input.txt', expect1=581108, expect2=None)
  pass

# 58348137614586
# 88414503579336
