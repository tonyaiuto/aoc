#!/usr/bin/env python3
"AOC 2025: day 06"

from collections import defaultdict
from functools import reduce

from tools import aoc


class Foo(object):

  def __init__(self):
    pass

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.__dict__)



class day06(aoc.aoc):

  def __init__(self):
    super(day06, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.rows = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    x = line.strip().replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
    assert '  ' not in x
    if x[0].isdigit(): 
       self.rows.append([int(n) for n in x.split(' ')])
    else:
       self.ops = x.split(' ')

  def post_load(self):
    # called after all input is read
    self.vectors = defaultdict(list)
    for row in self.rows:
      for col_i, value in enumerate(row):
        self.vectors[col_i].append(value) 


  def part1(self):
    print('===== Start part 1')
    self.reset()
    print(self.ops)
    # print(self.vectors)
    ret = 0
    for i, op in enumerate(self.ops):
      if op == '+':
        result = reduce(lambda acc, n: acc + n, self.vectors[i])
      if op == '*':
        result = reduce(lambda acc, n: acc * n, self.vectors[i])
      ret += result
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day06.sample_test("""
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   + 
""", expect1=4277556, expect2=None)


if __name__ == '__main__':
  day06.run_and_check('input.txt', expect1=6378679666679, expect2=None)
