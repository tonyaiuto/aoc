#!/usr/bin/env python3
"AOC 2021: day 24"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


from intcode import ALU
from intcode import Op

class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)


class day24(aoc.aoc):

  def __init__(self):
    super(day24, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.alu = ALU()

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    op = Op.parse(line)
    self.alu.mem_append(op)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    for op in self.alu.mem:
      print(op)

    self.alu.push_input([int(c) for c in '13579246899999'])
    self.alu.run()
    return self.alu.reg('z')


  def part2(self):
    print('===== Start part 2')
    self.reset()
    return 42


def sample():
  prog = day24()
  prog.load_file('input.txt')
  prog.alu.push_input([int(c) for c in '13579246899999'])
  prog.alu.trace = True
  prog.alu.run()
  assert 0 == prog.alu.reg('z')


sample()

if __name__ == '__main__':
  # day24.run_and_check('input.txt', expect1=None, expect2=None)
  pass
