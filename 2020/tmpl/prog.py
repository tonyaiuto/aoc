"AOC 2020: day @N@"

from collections import defaultdict


def sample_test(s, expect):
  puzz = day@N@()
  puzz.load_str(s)
  res = puzz.part1()
  if expect == res:
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
    pass

  def load_file(self, file):
    with open(file, 'r') as inp:
      for line in inp:
        self.do_line(line.strip())


  def load_str(self, s):
    for line in s.split('\n'):
      self.do_line(line.strip())


  def do_line(self, line):
    pass

  def part1(self):
    return None

  def part2(self):
    return None





if __name__ == '__main__':
  main('input.txt')
