#!/usr/bin/env python3
"AOC 2021: day 04"

from tools import aoc
from tools import gridutils


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day04(aoc.aoc):

  def __init__(self):
    super(day04, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
 
  def part1(self):
    print('===== Start part 1')
    self.reset()
    conts = 0
    for span in self.all_input:
      ls, rs = self.do_spans(span)
      # print(ls, rs)
      if contains(ls, rs):
        conts += 1
    return conts

  def do_spans(self, spans):
    ret = 0
    l, r =  spans.split(',')
    ls = [int(x) for x in l.split('-')]
    rs = [int(x) for x in r.split('-')]
    return ls, rs


  def part2(self):
    print('===== Start part 2')
    ret = 0
    spans = []
    for span in self.all_input:
      ls, rs = self.do_spans(span)
      # print(ls, rs)
      if overlap(ls, rs):
        ret += 1
    return ret

def contains(a, b):
  if a[0] > b[1]:
    return False
  if a[1] < b[0]:
    return False
  if a[0] >= b[0] and a[1] <= b[1]:
    return True
  if b[0] >= a[0] and b[1] <= a[1]:
    return True
  return False

def overlap(a, b):
  if a[0] > b[1]:
    return False
  if a[1] < b[0]:
    return False
  return True


day04.sample_test("""
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""", expect1=2, expect2=4)


if __name__ == '__main__':
  day04.run_and_check('input.txt', expect1=490, expect2=921)
