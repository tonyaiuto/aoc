"AOC 2020: day 20"

from collections import defaultdict
import math
from functools import reduce

from tools import reader


def sample_test(s, expect, expect2=None):
  puzz = day20()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    # puzz = day20()
    # puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day20()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  # puzz = day20()
  # puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res

def hsig(v):
  res = 0
  for c in v:
    res <<= 1
    if c == '#':
      res |= 1
  return res

def vsig(grid, col):
  res = 0
  for row in grid:
    res <<= 1
    if row[col] == '#':
      res |= 1
  return res

def revsig(sig):
  res = 0
  for bit in range(10):
    res <<= 1
    if sig & 1:
      res |= 1
    sig >>= 1
  return res
    

assert revsig(0x321) == 0x213


class Tile(object):

  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

  rot2right = [RIGHT, TOP, LEFT, BOTTOM]

  trace_create = True

  def __init__(self, number, grid):
    self.number = number
    self.grid = grid
    # compare order is hi 
    self.t = hsig(grid[0])
    self.l = vsig(grid, 0)
    self.b = hsig(grid[9])
    self.r = vsig(grid, 9)
    self.sigs = [self.t, self.r, self.b, self.l]

    self.fgrid = [row[::-1] for row in self.grid]
    print(self.fgrid)


    #Create all the rotations
    # h/l == high/low bit on original pattern
    #   h0l        l3h
    #  h   h      h   h
    #  3   1  ->  2   0
    #  l   l      l   l
    #   h2l        l1h
    self.rots = [self.sigs]
    for _ in range(1,4):
      rlast = self.rots[-1]
      self.rots.append([revsig(rlast[3]), rlast[0], revsig(rlast[1]), rlast[2]])
 
    # Horizontal flip the initial tile
    self.rots.append([revsig(self.t), self.l, revsig(self.b), self.r])
    for _ in range(1,4):
      rlast = self.rots[-1]
      self.rots.append([revsig(rlast[3]), rlast[0], revsig(rlast[1]), rlast[2]])
    assert len(self.rots) == 8
    if Tile.trace_create:
      print('tile: %d, t=%03x, b=%03x, l=%03x, r=%03x' %
           (number, self.t, self.b, self.l, self.r))


  def __repr__(self):
    return 'tile: %d' % self.number

  def __str__(self):
    return 'tile: %d' % self.number

  @staticmethod
  def from_text(text):
    number = int(text[0][5:9])
    return Tile(number, text[1:])

  def all_sigs(self):
    return [self.t, self.b, self.l, self.r,
            revsig(self.t), revsig(self.b), revsig(self.l), revsig(self.r)]

  def topsig(self, rot):
    return self.rots[rot][0]

  def leftsig(self, rot):
    return self.rots[rot][3]

  def rightsig(self, rot):
    return self.rots[rot][1]

  def botsig(self, rot):
    return self.rots[rot][2]

  def get_slice(self, gr, rot):
    grd = self.grid
    if rot > 3:
     grd = self.fgrid
     rot -= 4

    if rot == 0:
      v = grd[gr][1:9]
    elif rot == 1:
      v = ''.join([grd[row][gr] for row in range(1,9)])
      v = v[::-1]
    elif rot == 2:
      v = grd[9-gr][1:9]
      v = v[::-1]
    else:
      v = ''.join([grd[row][9-gr] for row in range(1,9)])

    #if hflip:
    #  return v[::-1]
    return v




class day20(object):

  def __init__(self):
    self.groups = True
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.tiles = []

  def reset(self):
    pass

  def load_file(self, file):
    all = reader.FileReader(file, by_group=self.groups).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    all = reader.StringReader(s, by_group=self.groups).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    self.tiles.append(Tile.from_text(line))

  def post_load(self):
    self.size = int(math.sqrt(len(self.tiles)))
    assert self.size in (3, 12)
    self.gather_by_sig()


  def gather_by_sig(self):
    self.tops = defaultdict(list)
    self.lefts = defaultdict(list)
    for rot in range(8):
      for tile in self.tiles:
        self.tops[tile.topsig(rot)].append((tile, rot))
        self.lefts[tile.leftsig(rot)].append((tile, rot))
    if self.size < 4:
      print('== top sigs== ')
      print(self.tops)
      print('== left sigs== ')
      print(self.lefts)
      print('===============')


  def try_in_ul(self, tile):
    """Try tile in upper left."""

    trace = 1

    left2rot = [3,2,1,0]
    rot2right = [Tile.RIGHT, Tile.TOP, Tile.LEFT, Tile.BOTTOM]

    def match_right(left, more, row_above=None, visited=None):
      if more == 0:
        yield []
      rightmost = left[-1]
      rightmost_tile = rightmost[0]
      sig = rightmost_tile.rightsig(rightmost[1])
      possible = [p for p in self.lefts.get(sig,[]) if p[0] not in visited]
      if not possible:
        return
      if trace > 2:
        print(' '*more, 'possible matches for sig %03x:' % sig, possible)

      col = len(left)
      assert col  == self.size - more

      if row_above:
        above_me = row_above[col]
        print('=== something above me', row_above)

        if col == 1:
          above_left = row_above[0]
          assert (above_left[0].botsig(above_left[1]) ==
                  rightmost_tile.topsig(rightmost[1]))
      else:
        above_me = None

      more -= 1
      left_tiles = [x[0] for x in left]
      for pos in possible:
        try_right, rot = pos
        if try_right in left_tiles:
          continue
        if above_me:
          if try_right.topsig(rot) != above_me[0].botsig(above_me[1]):
            print('====skipping because not right above')
            continue

        assert try_right.leftsig(rot) == sig
        if trace > 1:
          print(' '*more, 'match tile %d <%03x> %d need %d more' % (
                rightmost_tile.number, sig, try_right.number, more))

        if more == 0:
          yield [pos]
        else:
          for rest in match_right(left + [pos], more, visited=visited):
             yield [pos] + rest
      # end match_right

    def match_down(rows, more, visited=None):
      bottom_edge = rows[-1]
      print('>>>>>>bottom', bottom_edge)
      left_one = bottom_edge[0]
      sig = left_one[0].botsig(left_one[1])
      possible_leftmosts = [p for p in self.tops.get(sig, []) if p not in visited]
      if not possible_leftmosts:
        return

      more -= 1
      for pos in possible_leftmosts:
        try_first, rot = pos
        if trace > 0:
          print('Try row %d with %s rot:%d  ' % (self.size - more, try_first, rot))
        vs = set(visited)
        vs.add(try_first)
        for rest in match_right([pos], self.size-1, visited=vs, row_above=bottom_edge):
          new_row = [pos] + rest
          # print('   === new potential bottom row', new_row)

          if more == 0:
             print("   >> final row")
             yield [new_row]
          vs = vs.union([t[0] for t in new_row])

          for rest_down in match_down(rows + [new_row], more, visited=vs):
            # print(rest)
            yield [new_row] + rest_down
      # end match_down


    for rot in range(8):
      print('Trying tile %d in rot %d' % (tile.number, rot))
      visited = set([tile])
      for x in match_right([(tile, rot)], self.size-1, visited=visited):
        if len(x) == self.size - 1:
          first_row = [(tile, rot)] + x
          print(' === done with FIRST row', first_row)
          visited = visited.union([t[0] for t in first_row])
          print(' === visited', visited)
          for dwn in match_down([first_row], self.size-1, visited=visited):
            print("   XX --- maybe --- ", len(dwn), self.size)
            print('   XX', first_row)
            for d in dwn:
              print('   XX', d)
            print("   --------- --- ")
            if len(dwn) == self.size-1:
              return [first_row] + dwn
    return None


  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.result1 = None

    for tile in self.tiles:
      result = self.try_in_ul(tile)

      if result:
        print(result)
        first_row = result[0]
        last_row = result[self.size-1]
        corners = [
          first_row[0][0].number,
          first_row[self.size-1][0].number,
          last_row[0][0].number,
          last_row[self.size-1][0].number]
        prd = reduce((lambda x,y: x*y), corners)
        print('ZZ corners', corners, prd)
        self.result1 = prd
        self.picture = result
        break

    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()


    for row in self.picture:
      print([x[0].number for x in row])

    # make image
    image = []

    for row in self.picture:
      for gr in range(1, 9):
        out = ''
        for tile,rot in row:
          out += tile.get_slice(gr, rot)
        image.append(out)
    print('=========== image:')
    for r in image:
      print(r)

    print('part2', self.result2)
    return self.result2



sample_test("""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""", 20899048083289, 273)

"""
By rotating, flipping, and rearranging them, you can find a square arrangement that causes all adjacent borders to line up:

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....

1951    2311    3079
2729    1427    2473
2971    1489    1171

"""



if __name__ == '__main__':
  main('input.txt', 29584525501199, None)
  pass


"""
.####...###.#......###..
....#..#.#.#.....#.###..
...#####...#..#.#.##..#.
##.#....##..##.######..#
###.#####.####..#..####.
##.##.#####.#.#...#.#..#
###....##.####...####.##
.#.#..#.#..#.##..#.#.###
#..#....#..#.##..##...#.
...##..##.##.#..##..##..
###.#....#.#.##..#...#..
#.##.###...#...#####...#
#...#.##..##..##..#.#.#.
#.#.#..#..#.####..#.#.#.
.#....#.#.####.##.#...##
##...#.#.#..###..##.##.#
#..#####..#.##....##.#..
.#.......##..#..#.#..#.#
#####...#####.#.###.####
###.#..##...#.#..###.###
#...#.############....##
.#####.####.#..##...####
.#.###..#######..##.####
.#......#...##.####..#..
"""
