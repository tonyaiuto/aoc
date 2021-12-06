"""aoc core."""

import sys
import time
from typing import List

from tools import reader


class aoc(object):

  def __init__(self, reader_params={}):
    self.result1 = None
    self.result2 = None
    self.trace = False
    self.trace_sample = False
    self.all_input = None
    self.reader_params = {
        'by_group': False,
        'skip_first_blank': True,
        'strip_lines': True,
        'verbose': False,
    }
    self.reader_params.update(reader_params)

  def reset(self):
    pass

  def load_file(self, file):
    self.reader = reader.FileReader(file, **self.reader_params)
    self.all_input = self.reader.load()
    for x in self.all_input:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    self.reader = reader.StringReader(s, **self.reader_params)
    self.all_input = self.reader.load()
    for x in self.all_input:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    pass

  def post_load(self):
    pass

  def part1(self):
    print('You must implement part1()')

  def part2(self):
    print('You must implement part1()')

  @classmethod
  def run_and_check(cls, input, expect1=None, expect2=None, tag=None):
    solver = cls()
    tag = tag or type(solver).__name__

    start = time.perf_counter()
    solver.load_file(input)
    load_done = time.perf_counter()
    res = solver.part1()
    part1_done = time.perf_counter()
    solver.result1 = res
    print('part1:  %-15s     load: %.5fms, solve: %.5fms' % (
        str(res), 1000*(load_done-start), 1000*(part1_done-load_done)))
    if expect1 and  expect1 != res:
      print('FAIL: %s.part1:' % tag, 'expect', expect1, 'got', res)
      assert expect1 == res

    solver = cls()
    start = time.perf_counter()
    solver.load_file(input)
    load_done = time.perf_counter()
    res = solver.part2()
    part1_done = time.perf_counter()
    solver.result2 = res
    print('part2:  %-15s     load: %.5fms, solve: %.5fms' % (
        str(res), 1000*(load_done-start), 1000*(part1_done-load_done)))
    if expect2 and  expect2 != res:
      print('FAIL: %s.part2:' % tag, 'expect', expect2, 'got', res)
      assert expect2 == res

  @classmethod
  def sample_test(cls, s, expect1=None, expect2=None, tag=None):
    solver = cls()
    solver.trace_sample = True
    tag = tag or (type(solver).__name__ + '.sample')
    solver.load_str(s)
    res = solver.part1()
    if expect1 != res:
      print('%s.part1: FAIL:' % tag, 'expect', expect1, 'got', res)
      # assert expect1 == res
      sys.exit(1)

    if expect2:
      solver = cls()
      solver.trace_sample = True
      solver.load_str(s)
      res = solver.part2()
      if expect2 != res:
        print('%s.part2: FAIL:' % tag, 'expect', expect2, 'got', res)
        # assert expect2 == res
        sys.exit(1)
    print('%s: PASS' % tag)


def visit_range(start: int, end: int) -> List[int]:
  """Iterator that returns all integers from start to end, in order.

  It might move backwards.
  """
  if start <= end:
    while start != end+1:
      yield start
      start += 1
  else:
    while start != end-1:
      yield start
      start -= 1


def direction(start: int, end: int) -> int:
  return 1 if start <= end else -1


def self_check():
  # Test visit_range
  assert [2, 3, 4] == [i for i in visit_range(2, 4)]
  assert [4, 3, 2] == [i for i in visit_range(4, 2)]
  assert 1 == direction(2, 2)
  assert 1 == direction(2, 4)
  assert -1 == direction(4, 2)


if __name__ == '__main__':
  self_check()
  print('PASS:', __file__)
