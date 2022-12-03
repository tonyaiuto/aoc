#!/usr/bin/env python3
"AOC 2021: day 02"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

SCORES = {
 'A': 1,  # rock
 'B': 2,  # paper
 'C': 3,  # scissors
}


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)

def winner(them, me):
  if them == me:
    return 3
  if them == 'A':
    if me == 'B':
      return 6
    else:
      return 0
  if them == 'B':
    if me == 'C':
      return 6
    else:
      return 0
  if them == 'C':
    if me == 'A':
      return 6
    else:
      return 0


def score(them, me):
  s = SCORES[me]
  w = winner(them, me)
  return s + w


def pick_it(them, outcome):
  if outcome == 1:
    return them
  if outcome == 0:
    if them == 'A':
      return 'C'
    elif them == 'B':
      return 'A'
    else:
      return 'B'

  assert outcome == 2
  if outcome == 2:
    if them == 'A':
      return 'B'
    elif them == 'B':
      return 'C'
    else:
      return 'A'


class day02(aoc.aoc):

  def __init__(self):
    super(day02, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.rounds = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    s = line.split(' ')
    l2i = {'X': 0, 'Y': 1, 'Z': 2}
    s[1] = l2i[s[1]]
    self.rounds.append(s)
    pass

  def post_load(self):
    # called after all input is read 
    # print(self.rounds)
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()
    strat = ['A', 'B', 'C']
    s = 0
    for r in self.rounds:
       s += score(r[0], strat[r[1]])
    return s


  def part2(self):
    print('===== Start part 2')
    self.reset()
    
    s = 0
    for r in self.rounds:
       play = pick_it(r[0], r[1])
       s += score(r[0], play)
    return s

    """
    for strat in [['A', 'B', 'C'], ['A', 'C', 'B'],
                  ['B', 'A', 'C'], ['B', 'C', 'A'],
                  ['C', 'A', 'B'], ['C', 'B', 'A']]:
      s = 0
      for r in self.rounds:
         s += score(r[0], strat[r[1]])
    return 42
    """


day02.sample_test("""
A Y
B X
C Z
""", expect1=15, expect2=12)


if __name__ == '__main__':
  day02.run_and_check('input.txt', expect1=9651, expect2=None)
