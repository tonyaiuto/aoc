"AOC 2020: day 12"

from collections import defaultdict
import math

from tools import reader


def sample_test(s, expect, expect2):
  puzz = day12()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res
  res = puzz.part2()
  if expect2 != res:
    print('FAIL: expect', expect2, 'got', res)
    assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day12()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res



class day12(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.dir = 0
    self.x = 0
    self.y = 0
    self.wx = 0
    self.wy = 0
    self.moves = []
    self.trace = True

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    all = reader.StringReader(s).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    if line:
      self.moves.append(line)
    pass

  def post_load(self):
    pass

  def turn1(self, turn, degrees):
    if turn == 'L':
      self.dir += degrees
    elif turn == 'R':
      self.dir -= degrees
    else:
      print('bad turn', turn, degrees)
      assert False
    self.dir = self.dir % 360
    if self.trace:
      print('turn:', turn, degrees, '->', self.dir)

  def move1(self, dir, dist):
    if dir == 'N':
      self.y += dist
    elif dir == 'S':
      self.y -= dist
    elif dir == 'E':
      self.x += dist
    elif dir == 'W':
      self.x -= dist
    elif dir == 'F':
      rad = math.radians(self.dir)
      # print(self.dir, '->', rad, math.cos(rad), math.sin(rad))
      self.x += math.cos(rad) * dist
      self.y += math.sin(rad) * dist
    else:
      print('bad turn', dir, dist)
      assert False
    if self.trace:
      print('move:', dir, dist, '->', self.x, self.y)

  def part1(self):
    for move in self.moves:
      if move[0] in ('N', 'S', 'E', 'W', 'F'):
        self.move1(move[0], int(move[1:]))
      elif move[0] in ('L', 'R'):
        self.turn1(move[0], int(move[1:]))
      else:
        print('JUNK:', move)
        assert False
    self.result1 = int(abs(self.x) + abs(self.y) + 0.00000001)
    return self.result1



  def move2(self, dir, dist):
    if dir == 'N':
      self.wy += dist
    elif dir == 'S':
      self.wy -= dist
    elif dir == 'E':
      self.wx += dist
    elif dir == 'W':
      self.wx -= dist
    elif dir == 'F':
      rad = math.radians(self.dir)
      # print(self.dir, '->', rad, math.cos(rad), math.sin(rad))
      dx = self.wx - self.x
      dy = self.wy - self.y
      self.x += dx * dist 
      self.y += dy * dist
      self.wx = self.x + dx
      self.wy = self.y + dy
    else:
      print('bad turn', dir, dist)
      assert False
    if self.trace:
      print('move:', dir, dist, '->', self.x, self.y, 'way:', self.wx, self.wy)


  def turn2(self, turn, degrees):
    if turn == 'R':
      degrees = -degrees
    rad = math.radians(degrees)

    tx = self.wx - self.x
    ty = self.wy - self.y
    self.wx = self.x + (tx * math.cos(rad) - ty * math.sin(rad))
    self.wy = self.y + (tx * math.sin(rad) + ty * math.cos(rad))
    if self.trace:
      print('turn:', turn, degrees, '->', self.x, self.y, 'way:', self.wx, self.wy)

  def part2(self):
    print('============= start 2')
    self.result2 = None
    self.dir = 0
    self.x = 0
    self.y = 0
    self.wx = 10
    self.wy = 1
    for move in self.moves:
      if move[0] in ('N', 'S', 'E', 'W', 'F'):
        self.move2(move[0], int(move[1:]))
      elif move[0] in ('L', 'R'):
        self.turn2(move[0], int(move[1:]))
      else:
        print('JUNK:', move)
        assert False
    self.result2 = int(abs(self.x) + abs(self.y) + 0.00000001)
    return self.result2


sample_test("""
F10
N3
F7
R90
F11""", 25, 286)


if __name__ == '__main__':
  main('input.txt', 1589, 23960)
