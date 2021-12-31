#!/usr/bin/env python3
"AOC 2021: day 24"

from collections import defaultdict
import copy
import heapq
import itertools
import math
import sys

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
    hash_pos = line.find('#')
    if hash_pos >= 0:
      line = line[0:hash_pos].strip()
    if not line:
      return
    try:
      op = Op.parse(line)
      self.alu.mem_append(op)
    except Exception as e:
      print('bad input', line)
      raise e

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()

    #self.check1()

    row = 0
    for d1, d2, d3, d5, d6, d8, d10 in itertools.product(
          range(9, 10),
          range(9, 10),
          range(5, 10),
          # range(4, 8),
          range(8, 10),
          range(8, 10),
          # range(3, 5),
          range(1, 10),
          # range(7, 9),
          range(1, 10),
          # range(2, 4),
          # range(7, 9),
          # range(3, 6),
          # range(1, 10),
          ):
        z1 = d1 + 8
        z2 = z1 * 26 + d2 + 8
        z3 = z2 * 26 + d3 + 12

        assert (z3 // 26) == z2
        # if d4 == d3 + 4:
        d4 = z3 % 26 - 8
        if d4 < 1 or d4 > 9:
          continue
        if d4 == z3 % 26 - 8:
          z4 = z3 // 26
          # z4 = z2
        else:
          assert False
          # z4 = z2 * 26 + d4 + 10
          z4 = (z3 // 26) * 26 + d4 + 10

        z5 = z4 * 26 + d5 + 2
        z6 = z5 * 26 + d6 + 8

        d7 = z6 % 26 - 11
        if d7 < 1 or d7 > 9:
          continue
        if d7 == z6 % 26 - 11:
          # z7 = z5
          z7 = z6 // 26
        else:
          assert False
          # z7 = z5 * 26 + d7 + 4
          z7 = (z6 // 26) * 26 + d7 + 4
        z8 = z7 * 26 + d8 + 9
        assert (z8 // 26) == z7

        d9 = z8 % 26 - 3
        if d9 < 1 or d9 > 9:
          continue
        if d9 == z8 % 26 - 3:
          # z9 = z7
          z9 = z8 // 26
        else:
          # z9 = z7 * 26 + d9 + 10
          z9 = (z8 // 26) * 26 + d9 + 10
        z10 = z9 * 26 + d10 + 3

        assert (z10 // 26) == z9
        d11 = z10 % 26 - 3
        if d11 < 1 or d11 > 9:
          continue
        if d11 == z10 % 26 - 3:
          z11 = z9
          z11 = z10 // 26
        else:
          z11 = (z10 // 26) * 26 + d11 + 7

        #if z11 // 26 != z10:
        #  print('d8-11', d8, d9, d10, d11)
        #  print("wtf", z11, z11//26, z10, z9)
        #  assert (z11 // 26) == z10

        # if d12 == d11 + 6:
        d12 = z11 % 26 - 1
        if d12 < 1 or d12 > 9:
          continue
        if d12 == z11 % 26 - 1:
          z12 = z11 // 26
        else:
          # z12 = z9 * 26 + d12 + 7
          z12 = (z11 // 26) * 26 + d12 + 7

        d13 = z12 % 26 - 10
        if d13 < 1 or d13 > 9:
          continue
        if d13 == z12 % 26 - 10:  # d13 == d12 - 3:
          z13 = z12 // 26
        else:
          z13 = (z12 // 26) * 26 + d13 + 2

        d14 = (z13 % 26) - 16
        if d14 < 1 or d14 > 9:
          continue
        if d14 == (z13 % 26) - 16:
          z14 = z13 // 26
        else:
          assert False
          z14 = z13 // 26 * 26 + 2
        model_inp = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14]
        self.alu.reset()
        self.alu.push_input(model_inp)
        self.alu.expectz = [0,
                            z1, z2,  z3,  z4,  z5,  z6,  z7,
                            z8, z9, z10, z11, z12, z13, z14]
        row += 1
        # print(row, model_inp, self.alu.expectz)
        try:
          self.alu.run()
        except ALU.ZCheck as e:
          print(row, model_inp, self.alu.expectz)
          print(e.message)
          sys.exit(1)
        z = self.alu.reg('z')
        if z == 0:
          print("GOT ZERO")
          print(row, model_inp, self.alu.expectz)
          ret = model_inp

    return int(''.join([str(d) for d in ret]))



  def check1(self):
    row = 0
    for d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14 in itertools.product(
          range(1, 3),
          range(1, 4),
          range(3, 5),
          # range(4, 8),
          range(1, 4),
          range(5, 7),
          range(3, 5),
          range(1, 3),
          range(7, 9),
          range(1, 3),
          range(2, 4),
          range(7, 9),
          range(3, 6),
          range(1, 2),
          ):

        z1 = d1 + 8
        z2 = z1 * 26 + d2 + 8
        z3 = z2 * 26 + d3 + 12

        if d4 == z3 % 26 - 8:
          z4 = z3 // 26
          # z4 = z2
        else:
          # z4 = z2 * 26 + d4 + 10
          z4 = (z3 // 26) * 26 + d4 + 10

        z5 = z4 * 26 + d5 + 2
        z6 = z5 * 26 + d6 + 8
        #if d7 == d6 - 3:
        if d7 == z6 % 26 - 11:
          # z7 = z5
          z7 = z6 // 26
        else:
          # z7 = z5 * 26 + d7 + 4
          z7 = (z6 // 26) * 26 + d7 + 4
        z8 = z7 * 26 + d8 + 9
        assert (z8 // 26) == z7
        # if d9 == d8 + 6:
        if d9 == z8 % 26 - 3:
          # z9 = z7
          z9 = z8 // 26
        else:
          # z9 = z7 * 26 + d9 + 10
          z9 = (z8 // 26) * 26 + d9 + 10
        z10 = z9 * 26 + d10 + 3
        assert (z10 // 26) == z9
        if d11 == z10 % 26 - 3:
          z11 = z9
          z11 = z10 // 26
        else:
          z11 = (z10 // 26) * 26 + d11 + 7

        #if z11 // 26 != z10:
        #  print('d8-11', d8, d9, d10, d11)
        #  print("wtf", z11, z11//26, z10, z9)
        #  assert (z11 // 26) == z10

        # if d12 == d11 + 6:
        if d12 == z11 % 26 - 1:
          z12 = z11 // 26
        else:
          # z12 = z9 * 26 + d12 + 7
          z12 = (z11 // 26) * 26 + d12 + 7

        if d13 == z12 % 26 - 10:  # d13 == d12 - 3:
          z13 = z12 // 26
        else:
          z13 = (z12 // 26) * 26 + d13 + 2

        x = (z13 % 26) - 16
        z = z13 // 26
        if d14 == x:
          z14 = z
        else:
          z14 = z * 26 + 2
        model_inp = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14]
        self.alu.reset()
        self.alu.push_input(model_inp)
        self.alu.expectz = [0,
                            z1, z2,  z3,  z4,  z5,  z6,  z7,
                            z8, z9, z10, z11, z12, z13, z14]
        row += 1
        # print(row, model_inp, self.alu.expectz)
        try:
          self.alu.run()
        except ALU.ZCheck as e:
          print(row, model_inp, self.alu.expectz)
          print(e.message)
          sys.exit(1)
        z = self.alu.reg('z')
        if z == 0:
          print("GOT ZERO")
          print(row, model_inp, self.alu.expectz)
          return model_inp

    return 5

  def zcheck(self, expect):
    z = self.alu.reg('z')
    if z == expect:
      return
    print('zcheck: expected %d, got %d' % (expect, z))

  def part2(self):
    print('===== Start part 2')
    self.reset()
    row = 0
    for d1, d2, d3, d5, d6, d8, d10 in itertools.product(
          range(1, 10),
          range(1, 4),
          range(1, 10),
          # range(4, 8),
          range(1, 10),
          range(1, 10),
          # range(3, 5),
          range(1, 10),
          # range(7, 9),
          range(1, 10),
          # range(2, 4),
          # range(7, 9),
          # range(3, 6),
          # range(1, 10),
          ):
        z1 = d1 + 8
        z2 = z1 * 26 + d2 + 8
        z3 = z2 * 26 + d3 + 12

        assert (z3 // 26) == z2
        # if d4 == d3 + 4:
        d4 = z3 % 26 - 8
        if d4 < 1 or d4 > 9:
          continue
        if d4 == z3 % 26 - 8:
          z4 = z3 // 26
          # z4 = z2
        else:
          assert False
          # z4 = z2 * 26 + d4 + 10
          z4 = (z3 // 26) * 26 + d4 + 10

        z5 = z4 * 26 + d5 + 2
        z6 = z5 * 26 + d6 + 8

        d7 = z6 % 26 - 11
        if d7 < 1 or d7 > 9:
          continue
        if d7 == z6 % 26 - 11:
          # z7 = z5
          z7 = z6 // 26
        else:
          assert False
          # z7 = z5 * 26 + d7 + 4
          z7 = (z6 // 26) * 26 + d7 + 4
        z8 = z7 * 26 + d8 + 9
        assert (z8 // 26) == z7

        d9 = z8 % 26 - 3
        if d9 < 1 or d9 > 9:
          continue
        if d9 == z8 % 26 - 3:
          # z9 = z7
          z9 = z8 // 26
        else:
          # z9 = z7 * 26 + d9 + 10
          z9 = (z8 // 26) * 26 + d9 + 10
        z10 = z9 * 26 + d10 + 3

        assert (z10 // 26) == z9
        d11 = z10 % 26 - 3
        if d11 < 1 or d11 > 9:
          continue
        if d11 == z10 % 26 - 3:
          z11 = z9
          z11 = z10 // 26
        else:
          z11 = (z10 // 26) * 26 + d11 + 7

        #if z11 // 26 != z10:
        #  print('d8-11', d8, d9, d10, d11)
        #  print("wtf", z11, z11//26, z10, z9)
        #  assert (z11 // 26) == z10

        # if d12 == d11 + 6:
        d12 = z11 % 26 - 1
        if d12 < 1 or d12 > 9:
          continue
        if d12 == z11 % 26 - 1:
          z12 = z11 // 26
        else:
          # z12 = z9 * 26 + d12 + 7
          z12 = (z11 // 26) * 26 + d12 + 7

        d13 = z12 % 26 - 10
        if d13 < 1 or d13 > 9:
          continue
        if d13 == z12 % 26 - 10:  # d13 == d12 - 3:
          z13 = z12 // 26
        else:
          z13 = (z12 // 26) * 26 + d13 + 2

        d14 = (z13 % 26) - 16
        if d14 < 1 or d14 > 9:
          continue
        z = z13 // 26
        if d14 == (z13 % 26) - 16:
          z14 = z
        else:
          z14 = z * 26 + 2
        model_inp = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14]
        self.alu.reset()
        self.alu.push_input(model_inp)
        self.alu.expectz = [0,
                            z1, z2,  z3,  z4,  z5,  z6,  z7,
                            z8, z9, z10, z11, z12, z13, z14]
        row += 1
        # print(row, model_inp, self.alu.expectz)
        try:
          self.alu.run()
        except ALU.ZCheck as e:
          print(row, model_inp, self.alu.expectz)
          print(e.message)
          sys.exit(1)
        z = self.alu.reg('z')
        if z == 0:
          print("GOT ZERO")
          print(row, model_inp, self.alu.expectz)
          ret = model_inp
          break

    return int(''.join([str(d) for d in ret]))


def sample():
  prog = day24()
  prog.load_file('input.txt')
  prog.alu.push_input([int(c) for c in '13579246899999'])
  prog.alu.trace = True
  prog.alu.run()
  # assert 0 == prog.alu.reg('z')

# sample()

if __name__ == '__main__':
  day24.run_and_check('input_orig.txt', expect1=99598963999971, expect2=93151411711211)
  pass
