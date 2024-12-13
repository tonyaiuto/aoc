#!/usr/bin/env python3
"AOC 2023: day 13"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils
from tools import qparser


class Button(object):

  button_parser = qparser.QParser([
          qparser.Literal('Button'),
          qparser.Text(name='button', eat_leading_ws=True),
          qparser.Literal(': X+'),
          qparser.Number(name='x'),
          qparser.Literal(', Y+'),
          qparser.Number(name='y'),
        ])

  def __init__(self, line):
    self.button = ''
    self.x = 0
    self.y = 0
    Button.button_parser.parse(self, line)

  def __repr__(self):
    return str(self.__dict__)

  def __str__(self):
    return '%s %d %d' % (self.button, self.x, self.y)


class Prize(object):

  prize_parser = qparser.QParser([
          qparser.Literal('Prize: X='),
          qparser.Number(name='x'),
          qparser.Literal(', Y='),
          qparser.Number(name='y'),
        ])

  def __init__(self, line, a, b):
    Prize.prize_parser.parse(self, line)
    self.a = a
    self.b = b

  def set_a(self, line):
    Prize.button_parser.parse(self, line)

  def __repr__(self):
    return 'prize: %5d %5d' % (self.x, self.y)

  def __str__(self):
    return '%s %s %s' % (self.__repr__(), self.a, self.b)

  def least_cost1(self, verbose=False):
    if verbose:
      print(self)

    # self.x = self.a.x * a_press + self.b.x * b_press
    a_max = min(100, min(self.x // self.a.x, self.y // self.a.y))
    b_max = min(100, min(self.x // self.b.x, self.y // self.b.y))
    least_cost = -1
    for a_press in range(a_max):
      left = self.x - self.a.x * a_press
      b_press = left // self.b.x
      if b_press <= b_max:
        if b_press * self.b.x == left:
          cost = 3 * a_press + b_press
          if verbose:
            print(' prize at %d %d => cost: %d' % (a_press, b_press, cost))
          if least_cost > 0:
            least_cost = min(cost, least_cost)
          else:
            least_cost = cost
    return least_cost


class day13(aoc.aoc):

  def __init__(self):
    super(day13, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.prizes = []
    

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    a = Button(line[0])
    b = Button(line[1])
    prize = Prize(line[2], a, b)
    if self.doing_sample:
      print(prize)
    self.prizes.append(prize)

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for prize in self.prizes:
      cost = prize.least_cost1(verbose=self.doing_sample)
      if cost > 0:
        ret += cost

    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day13.sample_test("""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

""", expect1=480, expect2=7)


if __name__ == '__main__':
  # 26923 low part1
  day13.run_and_check('input.txt', expect1=27105, expect2=None)
