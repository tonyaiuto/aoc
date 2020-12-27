"AOC 2020: day 25"

from collections import defaultdict
import math

from tools import reader


TRACE = 1


def trace(*args, **kwargs):
  level = kwargs.get('level', 99)
  depth = kwargs.get('depth', 0)
  if level <= TRACE:
    print(' '*depth, *args)

def sample_test(s, expect, expect2=None):
  puzz = day25()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day25()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day25()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day25()
  puzz.load_file(input)
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


class day25(object):

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
    self.cardpub = int(self.all[0])
    self.doorpub = int(self.all[1])

  def handshake(self, sub, loop_size):
    n = 1
    for i in range(loop_size):
      n *= sub
      n = n % 20201227
    return n

  def pub2loop(self, pubkey):
    print('pub2loop', pubkey)
    loop = 0
    n = 1
    while True and loop <= 20201228:
      loop += 1
      if loop % 1000 == 0:
        trace('loop', loop, 'n', n, level=0)
      n = (n * 7) % 20201227
      if pubkey == n:
        print(' pub2loop', pubkey, '=>', loop)
        return loop

 

  def part1(self):
    trace('===== Start part 1')
    self.reset()

    cardpub = 5764801
    doorpub = 17807724
    cardloop = d.pub2loop(5764801)
    doorloop = d.pub2loop(17807724)

    assert 14897079 == self.handshake(doorpub, cardloop)

    # 2634053600
    cardloop = self.pub2loop(self.cardpub)
    # cl = self.pub2loop(self.doorpub)

    self.result1 = self.handshake(self.doorpub, cardloop)

    # card 13135480
    # door 8821721

    print('part1', self.result1)
    return self.result1



  def part2(self):
    trace('===== Start part 2')
    self.reset()
    self.result2 = None


    print('part2', self.result2)
    return self.result2


d = day25()
assert 8 == d.pub2loop(5764801)
assert 11 == d.pub2loop(17807724)


"""
sample_test(5764801, 5764801, 
"""




if __name__ == '__main__':
  main('input.txt', 8329514, None)
  pass
