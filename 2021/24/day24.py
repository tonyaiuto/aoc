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
    self.alu = ALU(terminate_on_end_of_input=True)
  
  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    if not line:
      return
    if line.startswith('#'):
      return
    op = Op.parse(line)
    self.alu.mem_append(op)

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.alu.push_input([int(c) for c in '13579246899999'])
    # self.alu.run()
    # return self.alu.reg('z')

    # self.alu.zexpect[0] = 0

    for d1, d2, d3, d4, d5, d6 in itertools.product(
            range(8, 10),
            range(8, 10),
            range(1, 3),
            range(5, 8),
            range(1, 4),
            range(3, 8),
            ):
        d1z = d1 + 8
        d2z = d1z * 26 + d2 + 8
        d3z = d2z * 26 + d3 + 12
        if d3 + 4 == d4:
          # d4z = d3z // 26
          d4z = d2z
        else:
          # d4z = d3z // 26 * 26 + d4 + 10
          d4z = d2z * 26 + d4 + 10
        d5z = d4z * 26 + d5 + 2
        d6z = d5z * 26 + d6 + 8

        model_inp = [d1, d2, d3, d4, d5, d6]
        print(model_inp)
        self.alu.reset()
        self.alu.push_input(model_inp)
        self.alu.expectz = [0, d1z, d2z, d3z, d4z, d5z, d6z]
        self.alu.run()
        self.zcheck(d6z)


    """
    loop = 0
    for model_inp in models():
      loop += 1
      if loop % 10000 == 0:
        print('loop', loop)
      self.alu.reset()
      self.alu.push_input(model_inp)
      self.alu.run()
      z = self.alu.reg('z')
      if loop % 100 == 0:
        print(model_inp, '->', z)
      if z == 0:
        return ''.join(model_inp)
    """
    return 5

  def zcheck(self, expect):
    z = self.alu.reg('z')
    if z == expect:
      return
    print('zcheck: expected %d, got %d' % (expect, z))

  def part2(self):
    print('===== Start part 2')
    self.reset()
    return 42


def models():
  for a, b, c, d, e,  f, g, h, i, j,  k, l, m, o in itertools.product(
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1),
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1),
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1),
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1),
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1),
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1),
      range(9, 0, -1),
      range(1, 2),  #range(9, 0, -1)
      ):
    yield [a, b, c, d, e,  f, g, h, i, j,  k, l, m, o]

def sample():
  prog = day24()
  prog.load_file('input.txt')
  prog.alu.push_input([int(c) for c in '13579246899999'])
  prog.alu.trace = True
  prog.alu.run()
  # assert 0 == prog.alu.reg('z')

# sample()

if __name__ == '__main__':
  day24.run_and_check('input.txt', expect1=None, expect2=None)
  pass
