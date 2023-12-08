#!/usr/bin/env python3
"AOC 2023: day 08"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Node(object):

  def __init__(self, line):
    # AAA = (BBB, CCC)
    parts = [x for x in line.split(' ') if x]
    self.name = parts[0]
    self.l = parts[2][1:-1]
    self.l2 = self.l[2]
    self.r = parts[3][0:-1]
    self.r2 = self.r[2]
    self.is_z = self.name[2] == 'Z'

  def __str__(self):
    return '%s[%s, %s]' % (self.name, self.l, self.r)

  def __repr__(self):
    return '%s[%s, %s]' % (self.name, self.l, self.r)


class day08(aoc.aoc):

  def __init__(self):
    super(day08, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.lr = None
    self.nodes = {}
    self.paths = defaultdict(list)

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    if not line:
      return
    if not self.lr:
      self.lr = line
      return
    node = Node(line)
    self.nodes[node.name] = node
    self.paths[node.name[2]].append(node)

  def post_load(self):
    # called after all input is read
    for name, node in self.nodes.items():
      node.fast_l = self.nodes[node.l]
      node.fast_r = self.nodes[node.r]

  def part1(self):
    print('===== Start part 1')
    # print(self.nodes)
    
    at = self.nodes['AAA']
    zzz = self.nodes['ZZZ']
    steps = 0
    while at != zzz:
      for dir in self.lr:
        if at == zzz:
          break
        steps += 1
        if dir == 'L':
          at = at.fast_l
        else:
          at = at.fast_r
        # at = self.nodes[nxt]
    return steps

  def dirs_forever(self):
    while True:
      for dir in self.lr:
        yield dir

  def part2(self):
    print('===== Start part 2')
    self.reset()

    starts = [node for node in self.paths['A']]
    cur = [node for node in self.paths['A']]
    cycles = [0] * len(cur)
    zat = [0] * len(cur)
    zcycle = [0] * len(cur)

    for ni in range(len(cur)):
      start = starts[ni]
      node = start
      zs = {}
      steps = 0
      for dir in self.dirs_forever():
        if dir == 'L':
          node = node.fast_l
        else:
          node = node.fast_r
        steps += 1
        if node == start:
          cycles[ni] = steps
          assert zat[ni] != 0
          break
        if node.is_z:
          if zat[ni] == 0:
            zat[ni] = steps
          # print("zat:", node.name, steps)
          if node in zs:
            zcycle[ni] = steps - zs[node]
            break
          zs[node] = steps
      print(start.name, '%7d' % zat[ni],
            '%7d' % zcycle[ni], '%7d' % cycles[ni],
            ['%s:%d' % (z.name, zs[z]) for z in zs])

    lcm = zcycle[0]
    for i in zcycle[1:]:
      lcm = lcm * i // math.gcd(lcm, i)
    return lcm

  def mv_all(self, cur, dir):
    for ni in range(len(cur)):
      node = cur[ni]
      if dir == 'L':
        nxt = node.l
      else:
        nxt = node.r
      cur[ni] = self.nodes[nxt]

def all_z(nodes):
  for node in nodes:
    if node.name[2] != 'Z':
      return False
  return True


day08.sample_test("""
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""", expect1=2, expect2=None)

day08.sample_test("""
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""", skip1=True, expect2=6)


if __name__ == '__main__':
  day08.run_and_check('input.txt', expect1=20221, expect2=None)
