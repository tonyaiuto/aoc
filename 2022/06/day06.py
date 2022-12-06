#!/usr/bin/env python3
"AOC 2021: day 06"

from collections import defaultdict
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


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

  def part1(self):
    print('===== Start part 1')
    data = self.all_input[0]
    have = [c for c in data[0:3]]
    for ci in range(3, len(data)):
       c = data[ci]
       # print('have:', have, 'check', c)
       if not c in have and all_diff(have):
         return ci + 1
       have = have[1:] + [c]
    return -1


  def part2(self):
    print('===== Start part 2')
    data = self.all_input[0]
    have = [c for c in data[0:13]]
    for ci in range(13, len(data)):
       c = data[ci]
       # print('have:', have, 'check', c)
       if not c in have and all_diff(have):
         return ci + 1
       have = have[1:] + [c]
    return -1

def all_diff(s):
  x = set(s)
  return len(x) == len(s)

def all_diff1(s):
  if s[0] == s[1] or s[0] == s[2]:
    return False
  if s[1] == s[2]:
    return False
  return True


day06.sample_test("""
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""", expect1=7, expect2=19)

day06.sample_test("""
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
""", expect1=11, expect2=26)


if __name__ == '__main__':
  day06.run_and_check('input.txt', expect1=1155, expect2=2789)
