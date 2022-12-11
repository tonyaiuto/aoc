#!/usr/bin/env python3
"AOC 2021: day 11"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

MONKEYS = {}

class Monkey(object):

  lcm = 1

  def __init__(self, lines):
    assert lines[0].startswith('Monkey ')
    self.monkey = int(lines[0][7:-1])
    self.mul = 0
    self.add = 0
    self.square = False
    self.inspected = 0
    for line in lines[1:]:
      parts = line.lstrip().split(':')
      if parts[0] == 'Starting items':
         self.items = [int(s) for s in parts[1].split(',')]
      if parts[0] == 'Operation':
         op = parts[1][11:]
      if parts[0] == 'Test':
         if op[0] == '+':
           self.add = int(op[2:])
         elif op[0] == '*':
           if op == '* old':
              self.square = True
           else:
              self.mul = int(op[2:])
         assert parts[1].startswith(' divisible by ')
         self.div = int(parts[1][14:])
      if parts[0] == 'If true':
        self.true_to = int(parts[1][-1])
      if parts[0] == 'If false':
        self.false_to = int(parts[1][-1])

    assert self.true_to != self.monkey
    assert self.false_to != self.monkey
    MONKEYS[self.monkey] = self
    Monkey.lcm *= self.div
    print(self)

  def __str__(self):
    op = 'x ' 
    if self.mul :
      op += '* %d' % self.mul
    if self.add :
      op += '+ %d' % self.add
    if self.square :
      op += '* x'
    return 'm %d: %s, div %d, %s , t:%d, f:%d' % (self.monkey, self.items, self.div, op, self.true_to, self.false_to)

  def turn(self, round2=False):
    for item in self.items:
      self.inspected += 1
      if self.mul :
        item = item * self.mul
      elif self.add :
        item = item + self.add
      elif self.square :
        item = item * item
      if not round2:
        item = item // 3

      if item % self.div == 0:
        mt = MONKEYS[self.true_to]
      else:
        mt = MONKEYS[self.false_to]
      mt.items.append(item % Monkey.lcm)
      # mt.items.append(item)
    self.items = []


class day11(aoc.aoc):

  def __init__(self):
    super(day11, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.monkeys = []

  def reset(self):
    # for future use
    pass

  def do_line(self, group):
    # called for each line of input
    self.monkeys.append(Monkey(group))
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    for i in range(20):
      for m in self.monkeys:
        m.turn()
    top = sorted([m.inspected  for m in self.monkeys])[-2:]
    return top[0] * top[1]


  def part2(self):
    print('===== Start part 2')
    self.reset()

    for i in range(10000):
      for m in self.monkeys:
        m.turn(round2=True)
    for m in self.monkeys:
      print(m)
    top = sorted([m.inspected  for m in self.monkeys])[-2:]
    return top[0] * top[1]

    return 42


day11.sample_test("""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""", expect1=10605, expect2=2713310158)


if __name__ == '__main__':
  day11.run_and_check('input.txt', expect1=108240, expect2=25712998901)
