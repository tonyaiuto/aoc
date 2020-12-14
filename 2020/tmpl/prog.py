"AOC 2020: day @N@"

from collections import defaultdict
import math

from tools import reader


def sample_test(s, expect, expect2=None):
  puzz = day@N@()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day@N@()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day@N@()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day@N@()
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
    return str(self)



class day@N@(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True

  def reset(self):
    pass

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
    pass

  def post_load(self):
    pass



  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.result1 = None



    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = None


    print('part2', self.result2)
    return self.result2



sample_test("""

""", None, None)



if __name__ == '__main__':
  main('input.txt', None, None)
