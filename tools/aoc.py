"""aoc core."""

import sys
import time
from typing import List

from tools import reader

def run_func(func, expect=None, tag=None):
  t_start = time.perf_counter()
  res = func()
  t_end = time.perf_counter()
  print('%s:  %-15s   solve: %.5fms' % (tag, str(res), 1000*(t_end-t_start)))
  if expect and  expect != res:
    print('FAIL: %s:' % tag, 'expect', expect, 'got', res)
    sys.exit(1)
  print('-----')
  return res


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
    print('Reusing solver from part1')

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
    print('You must implement part2()')

  @classmethod
  def run_and_check(cls, input, expect1=None, expect2=None, tag=None, recreate=True):
    solver = cls()
    tag = tag or type(solver).__name__

    start = time.perf_counter()
    solver.load_file(input)
    load_done = time.perf_counter()
    print('part1:  %-15s     load: %.5fms' % (' ', 1000*(load_done-start)))
    solver.result1 = run_func(
        solver.part1, expect=expect1, tag=tag+'.part1')

    if recreate:
      solver = cls()
      start = time.perf_counter()
      solver.load_file(input)
      load_done = time.perf_counter()
    else:
      solver.reset()
    solver.result2 = run_func(
        solver.part2, expect=expect2, tag=tag+'.part2')

  @classmethod
  def sample_test(cls, input, expect1=None, expect2=None, tag=None, recreate=True, is_file=False):
    solver = cls()
    solver.trace_sample = True
    tag = tag or (type(solver).__name__ + '.sample')
    if is_file:
      solver.load_file(input)
    else:
      solver.load_str(input)
    _ = run_func(solver.part1, expect=expect1, tag=tag+'.part1')

    if recreate:
      solver = cls()
      solver.trace_sample = True
      if is_file:
        solver.load_file(input)
      else:
        solver.load_str(input)
    else:
      solver.reset()
    _ = run_func(solver.part2, expect=expect2, tag=tag+'.part2')
    print('%s: PASS' % tag)

  @classmethod
  def do(solver_cls, func, input, expect=None, tag=None):
    solver = solver_cls()
    tag = tag or func.__name__

    start = time.perf_counter()
    solver.load_file(input)
    load_done = time.perf_counter()
    res = func(solver)
    part1_done = time.perf_counter()
    solver.result1 = res
    print('%s:  %-15s     load: %.5fms, solve: %.5fms' % (
        tag, str(res), 1000*(load_done-start), 1000*(part1_done-load_done)))
    if expect and  expect != res:
      print('%s: FAIL:' % tag, 'expect', expect, 'got', res)
      sys.exit(1)


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
