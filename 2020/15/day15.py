"AOC 2020: day 15"

from collections import defaultdict
import math

from tools import reader


def sample_test(s, expect, expect2=None):
  puzz = day15()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day15()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day15()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day15()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class N(object):

  def __init__(self, n, turn):
    self.n = int(n)
    self.first = turn
    self.turn = turn
    self.diff = -1


  def __str__(self):
    return '%4d[first:%d, turn:%d, diff:%d]' % (self.n, self.first, self.turn, self.diff)

  def __repr__(self):
    return '%4d[first:%d, turn:%d, diff:%d]' % (self.n, self.first, self.turn, self.diff)

  
  def speak(self, turn):
    self.diff = turn - self.turn
    self.turn = turn
    print('speak: %d at turn %d' % (self.n, self.turn))


class day15(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True

  def reset(self):
    pass

  def load_file(self, file):
    self.all = reader.FileReader(file).load()
    for x in self.all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    self.all = reader.StringReader(s).load()
    for x in self.all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    pass

  def post_load(self):
    self.spoken = {}
    self.numbers = self.all[0].split(',')
    for i in range(len(self.numbers)):
      n = int(self.numbers[i])
      new_n = N(n, i+1)
      self.spoken[n] = new_n
    print(self.numbers)
    print(self.spoken)


  def part1(self, limit=2020):
    print('===== Start part 1')
    self.reset()
    self.result1 = None

    last = self.spoken[int(self.numbers[-1])]
    turn = last.turn
    while turn < limit:
      #if turn < 20 or turn > 2010:
      if turn % 100000 == 0:
        print('last spoke: turn %d = %d' % (turn, last.n))
      if last.diff < 0:
        if turn < 20:
          print('  -> first time spoken')
        # first time spoken
        next_n = 0
      else:
        next_n = last.diff
        if next_n <= 0:
          print('FAIL:', last)

      # speak
      turn = turn + 1
      last = self.spoken.get(next_n)
      if last:
        last.diff = turn - last.turn
        last.turn = turn
      else:
        last = N(next_n, turn)
        self.spoken[next_n] = last
      self.result1 = last.n

    print('last is ', last)

    self.result1 = last.n
    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = self.part1(limit=30000000)

    print('part2', self.result2)
    return self.result2




sample_test("""
0,3,6
""", 436, None)

sample_test("""
1,3,2
""", 1, None)

sample_test("""
2,1,3
""", 10, None)

sample_test("""
3,1,2
""", 1836, None)



if __name__ == '__main__':
  sample_test('16,12,1,0,15,7,11', 403, 6823)
