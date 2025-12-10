#!/usr/bin/env python3
"AOC 2025: day 10"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

def combos(buttons):
  for x in buttons:
    yield [x]
  for size in range(2, len(buttons)+1):
    for x in itertools.combinations(buttons, size):
      yield x


class Machine(object):

  def __init__(self, line):
    # [#..###] (0,1,3,4,5) (3,4) (1,2,3,4) (3,5) (1,3,4,5) (4) (1,4,5) {1,48,11,53,68,40}
    parts = line.split(' ')
    self.lights = parts[0][1:-1]
    self.lt = [light == '#' for light in self.lights]
    self.buttons = []
    for b in parts[1:-1]:
      self.buttons.append([int(n) for n in b[1:-1].split(',')])
    self.joltage = [int(n) for n in parts[-1][1:-1].split(',')]

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f"[{self.lights}]: {self.buttons} {self.joltage}"

  def push(self, n, state):
    ns = copy(state)
    toggles = self.buttons[n]
    for light_i in toogles:
      ns[i] = not state[i]
    return ns

  def run_sequence(self, flips):
    lights = [False] * len(self.lights)
    for flip in flips:
      for to_flip in flip:
        lights[to_flip] = not lights[to_flip]
    return lights

  def try_combos(self):
    for flips in combos(self.buttons):
      l = self.run_sequence(flips)
      # print(flips, '==>', l)
      if self.lt == l:  # we win
        return len(flips)


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
    self.machines = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    machine = Machine(line)
    if self.doing_sample:
      print(str(machine))
    self.machines.append(machine)

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for mach in self.machines:
       ret += mach.try_combos()
    print('XXXX', ret)
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day10.sample_test("""
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""", expect1=7, expect2=None)


if __name__ == '__main__':
  day10.run_and_check('input.txt', expect1=473, expect2=None)
