"AOC 2020: day 24"

from collections import defaultdict
import math

from tools import reader

dirs = ['e', 'se', 'sw', 'w', 'nw', 'ne']
shifts = [(0, 1), (-1,1), (-1, 0),  (0,-1), (1, 0), (1,1), None, None,
          (0, 1), (-1,0), (-1,-1),  (0,-1), (1,-1), (1,0), None, None]

E = 0
SE = 1
SW = 2
W = 3
NW = 4
NE = 5

def pdir(dir):
  return ' '.join([dirs[i] for i in dir])

def dirsplit(dir):
  i = 0
  ret = []
  while i < len(dir):
    c = dir[i]
    if c == 'e':
      d = E
    elif c == 'w':
      d = W
    else:
      n = dir[i+1]
      if c == 's':
        if n == 'e':
          d = SE
        else:
          assert n == 'w'
          d = SW
        i+= 1
      elif c == 'n':
        if n == 'e':
          d = NE
        else:
          assert n == 'w'
          d = NW
        i += 1
    ret.append(d)
    i += 1
  return ret

def move(pos, dir):
  row = pos[0]
  c = pos[1]

  shifts = (dir | (row & 1))
  return (row+shifts[0], c+shifts[1])


def check_move(dirs, dst):
  path = dirsplit(dirs)
  # print(pdir(path))
  pos = (0,0)
  for m in path:
    pos = move(pos, m)
    print(dirs[m], '=>', pos)
  if pos != dst:
    print('expected', dst, 'got', pos)
    assert pos == dst


check_move('nwwswee', (0,0))


TRACE=1

def trace(*args, **kwargs):
  level = kwargs.get('level', 99)
  depth = kwargs.get('depth', 0)
  if level <= TRACE:
    print(' '*depth, *args)

def sample_test(s, expect, expect2=None):
  puzz = day24()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    # puzz = day24()
    # puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day24()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  # puzz = day24()
  # puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Foo(object):


  def __init__(self):
    pass

  def __str__(self):
    return 'FOO'

  @staticmethod
  def fromString(s):
    pass


class day24(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.by_group = False
    self.trace = True

  def reset(self):
    pass

  def load_file(self, file):
    self.all = reader.FileReader(file, by_group=self.by_group).load()
    for x in self.all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    self.all = reader.StringReader(s, by_group=self.by_group).load()
    for x in self.all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    pass

  def post_load(self):
    pass

  def follow(self, dir):
    path = dirsplit(dir)
    # print(pdir(path))
    pos = (0,0)
    for m in path:
      pos = move(pos, m)
      # print('   ', dirs[m], '=>', pos)
    return pos


  def part1(self):
    trace('===== Start part 1')
    self.reset()

    self.blacks = set()
    for dir in self.all:
      final_pos = self.follow(dir)
      # print('final', final_pos)
      if final_pos in self.blacks:
        self.blacks.remove(final_pos)
      else:
        self.blacks.add(final_pos)

    self.result1 = len(self.blacks)
    print('part1', self.result1)
    return self.result1



  def part2(self):
    trace('===== Start part 2')
    self.reset()

    def neighbors(pos):
      return [move(pos, d) for d in range(6)]

    def do_day():
      toscan = set()
      for b in self.blacks:
        toscan.add(b)
        for n in neighbors(b):
          toscan.add(n)

      nblacks = set()
      for tile in toscan:
        nbk = 0
        for n in neighbors(tile):
          if n in self.blacks:
            nbk += 1
        if tile in self.blacks:
          if nbk > 0 and nbk <= 2:
            nblacks.add(tile)
        else:
          if nbk == 2:
            nblacks.add(tile)
      self.blacks = nblacks

    for day in range(100):
      do_day()
      print('Day %d: %s' % (day, len(self.blacks)))

    self.result2 = len(self.blacks)
    print('part2', self.result2)
    return self.result2


sample_test("""
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""", 10, 2208)



if __name__ == '__main__':
  main('input.txt', 244, 3665)
  pass
