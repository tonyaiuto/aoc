#!/usr/bin/env python3
"AOC 2025: day 03"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc


def max_jolt(bank):
  digs_by_value = sorted([(v, -i) for i, v in enumerate(bank[0:-1])], reverse=True)
  d1, p1 = digs_by_value[0]
  p1 = -p1
  d2 = max(bank[p1+1:])
  p2 = 0
  for i, v in enumerate(bank[p1+1:]):
    if v == d2:
       p2 = p1 + i + 1
       break
  px = [str(d) for d in bank]
  print("=>", d1, d2, ':', ''.join(px[0:p1]), px[p1], ''.join(px[p1+1:p2]), px[p2], ''.join(px[p2+1:]))
  return d1*10 + d2

def max_jolt2(bank, n_digits=12):
  if len(bank) == 1:
    return [bank[0]]
  digs_by_value = sorted([(v, -i) for i, v in enumerate(bank[0:-(n_digits-1)])], reverse=True)
  if not digs_by_value:
    return [bank[0]]
  d1, p1 = digs_by_value[0]
  p1 = -p1
  rest = max_jolt2(bank[p1+1:], n_digits-1)
  """
  p2 = 0
  for i, v in enumerate(bank[p1+1:]):
    if v == d2:
       p2 = p1 + i + 1
       break
  px = [str(d) for d in bank]
  print("=>", d1, d2, ':', ''.join(px[0:p1]), px[p1], ''.join(px[p1+1:p2]), px[p2], ''.join(px[p2+1:]))
  """
  return [d1] + rest

class day03(aoc.aoc):

  def __init__(self):
    super(day03, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.banks = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    self.banks.append([int(c) for c in line.strip()])


  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for bank in self.banks:
       ret += max_jolt(bank)
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for bank in self.banks:
       v = max_jolt2(bank)
       print(v)
       ret += int(''.join(v))
       result = reduce(lambda acc, x: acc * 10 + x, data)
    return ret


day03.sample_test("""
987654321111111
811111111111119
234234234234278
818181911112111
""", expect1=357, expect2=3121910778619)

# low 17138 

if __name__ == '__main__':
  day03.run_and_check('input.txt', expect1=17144, expect2=None)
