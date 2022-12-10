#!/usr/bin/env python3
"AOC 2021: day 10"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class CPU(object):

  def __init__(self):
    self.verbose = 0
    self.inst = []
    self.cycle = 0
    self.pc = -1 
    self.x = 1

  def reset(self):
    self.cycle = 0
    self.pc = -1
    self.x = 1

  def __str__(self):
    return str(self)

  def add_inst(self, line):
    x = line.split(' ')
    if x[0] == 'addx':
      arg = int(x[1])
      self.inst.append(arg)
      if arg == 0: 
        print('watch out for zero', line)
    elif x[0] == 'noop':
      self.inst.append(None)
    else:
      print('WTF:', line)
      sys.exit(0)

  def do_inst(self):
    self.pc += 1
    if self.pc >= len(self.inst):
      print("==== LOOP")
      self.pc = 0
    what = self.inst[self.pc]

    if what is None:
      if self.verbose > 1:
        print('noop')
      self.cycle += 1
      signal = self.cycle * self.x
      yield (self.cycle, signal, self.x)
      return

    if self.verbose > 1:
      print("ADDX", what)
    self.cycle += 1
    signal = self.cycle * self.x
    yield (self.cycle, signal, self.x)

    self.cycle += 1
    signal = self.cycle * self.x
    yield (self.cycle, signal, self.x)
    self.x += what


class day10(aoc.aoc):

  def __init__(self):
    super(day10, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.cpu = CPU()

  def do_line(self, line):
    # called for each line of input
    self.cpu.add_inst(line)

  def part1(self):
    print('===== Start part 1')
    want = set([20, 60, 100, 140, 180, 220])
    ret = 0
    for i in range(250):
      for (c, s, x) in self.cpu.do_inst():
        if c in want:
          print(c, s, x)
          ret += s
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.cpu.reset()
    self.cpu.verbose = 0
    ret = 0
    row = ['  '] * 40
    pos = 0
    for i in range(200):
      for (cycle, s, x) in self.cpu.do_inst():
        if cycle > 250:
          break
        #if cycle < 20:
        #  print('pos: %3d, cycle: %3d, x: %3d: %s' % (
        #      pos, cycle, x, ''.join(row)))
        #else:
        #  self.cpu.verbose = 0
        if x-1 <= pos and pos <= x+1:
          row[pos % 40] = '##'
        pos += 1
        if pos % 40 == 0:
          print('%3d' % pos, ''.join(row))
          row = ['  '] * 40
          pos = 0
    return ret


day10.sample_test("""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""", expect1=13140, expect2=None)


if __name__ == '__main__':
  day10.run_and_check('input.txt', expect1=14520, expect2='PZBGZEKB')
