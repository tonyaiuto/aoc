#!/usr/bin/env python3
"AOC 2021: day 05"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils
from tools import qparser


class Move(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day05(aoc.aoc):

  def __init__(self):
    super(day05, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': False,
            'verbose': False,
        })
    self.trace = True
    # This is overkill, but I am refreshing memory of how to use it.
    self.parser = qparser.QParser([
        qparser.Literal('move'),
        qparser.Number('q'),
        qparser.Literal('from'),
        qparser.Number('f'),
        qparser.Literal('to'),
        qparser.Number('t'),
        ])

  def do_line(self, line):
    # called for each line of input
    pass

  def part1(self):
    print('===== Start part 1')
    self.load_stacks(self.all_input[0])
    # print('============')
    # print(s
    for move in self.all_input[1]:
      self.do_move(move)

    ret = ''.join(s[-1] for s in self.stacks[1:])
    return ret

  def load_stacks(self, si):
    self.n_stacks = (len(si[-1].split(' ')) + 2) // 3
    rows = len(si) - 1
    print(self.n_stacks, 'stacks')
    self.stacks = []
    for i in range(self.n_stacks+1):
      self.stacks.append('')
 
    for ri in range(rows):
      l = si[rows - ri - 1]
      # print('=====', l)
      for c in range(self.n_stacks):
         # print('col', c)
         container = l[c * 4 + 1]
         if container != ' ':
           # print(c+1, container)
           self.stacks[c+1] += container
    print('STACKS:', self.stacks)

  def do_move(self, move, rev=True):
    m = Move()
    self.parser.parse(m, move)
    # print('MOVE:', m.q, ':', m.f, '->', m.t)
    md = self.stacks[m.f][-m.q:]
    if rev:
      md = md[::-1]
    new_len_f = len(self.stacks[m.f]) - m.q
    self.stacks[m.f] = self.stacks[m.f][0:new_len_f]
    self.stacks[m.t] += md
    # print(md, self.stacks[m.f], self.stacks[m.t])
    # print('  >> Stacks:', self.stacks)

  def part2(self):
    print('===== Start part 2')
    self.load_stacks(self.all_input[0])
    for move in self.all_input[1]:
      self.do_move(move, rev=False)
    ret = ''.join(s[-1] for s in self.stacks[1:])
    return ret


day05.sample_test("""
.   [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""", expect1='CMZ', expect2='MCD')


if __name__ == '__main__':
  day05.run_and_check('input.txt', expect1='HBTMTBSDC', expect2='PQTJRSHWS')
