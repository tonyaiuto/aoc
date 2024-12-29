#!/usr/bin/env python3
"AOC 2023: day 23"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Comp(object):

  _by_name = {}

  def __init__(self, name):
    assert not name in Comp._by_name
    Comp._by_name[name] = self
    self.name = name
    self.connects = set()

  @staticmethod
  def get(name):
    ret = Comp._by_name.get(name)
    if not ret:
      ret = Comp(name)
    return ret

  @staticmethod
  def all():
    return Comp._by_name.values()

  @staticmethod
  def all_names():
    return Comp._by_name.keys()

  @staticmethod
  def reset():
    Comp._by_name = {}

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.name)

  @property
  def connections(self):
    return self.connects

  def add_connection(self, comp):
    self.connects.add(comp)

  def connects_to(self, comp):
    return comp in self.connects


class day23(aoc.aoc):

  def __init__(self):
    super(day23, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    Comp.reset()

  def do_line(self, line):
    # called for each line of input
    parts = line.split('-')
    a = Comp.get(parts[0])
    b = Comp.get(parts[1])
    assert a != b
    a.add_connection(b)
    b.add_connection(a)
    assert len(Comp.all()) == len(Comp.all_names())

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      print(Comp.all())
    print("len_comp", len(Comp.all()))

  def part1(self):
    print('===== Start part 1')
    self.reset()

    triplets = set()
    for comp in Comp.all():
      if comp.name[0] != 't':
        continue
      for other in comp.connections:
        # print(comp, 'checking', other)
        assert comp != other
        for third in other.connections:
          if third.connects_to(comp):
            key = ','.join(sorted([comp.name, other.name, third.name]))
            # print('adding', key, 'for', comp.name, other.name, third.name)
            triplets.add(key)

    # print(sorted(triplets))
    return len(triplets)


  def part2(self):
    print('===== Start part 2')

    return 42


day23.sample_test("""
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""", expect1=7, expect2=None)


if __name__ == '__main__':
  # part1: 1420 too high
  day23.run_and_check('input.txt', expect1=None, expect2=None)
