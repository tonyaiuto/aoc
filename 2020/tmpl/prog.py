"AOC 2020: day @N@"

from collections import defaultdict
import reader


def sample_test(s, expect):
  puzz = day@N@()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res


def main(input):
  puzz = day@N@()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  res = puzz.part2()
  print('part2', res)


class Foo(object):

  def __init__(self):
    pass


  def __str__(self):
    return str(self)



class day@N@(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    pass

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)

  def load_str(self, s):
    all = reader.StringReader(file).load()
    for x in all:
      self.do_line(x)

  def do_line(self, line):
    pass

  def part1(self):
    self.result1 = None
    return None

  def part2(self):
    self.result2 = None
    return None


# sample_test("""   """, expect):


if __name__ == '__main__':
  main('input.txt')
