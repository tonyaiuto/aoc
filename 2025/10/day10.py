#!/usr/bin/env python3
"AOC 2025: day 10"

from collections import defaultdict
import copy
import heapq
import itertools

from tools import aoc

def combos(buttons):
  for x in buttons:
    yield [x]
  for size in range(2, len(buttons)+1):
    for x in itertools.combinations(buttons, size):
      yield x

def all_values(width, max_n):
  for i in range(0, max_n+1):
    if width == 1:
      yield [i]
    else:
      for v in all_values(width-1, max_n):
        yield [i] + v

"""
for v in all_values(4, 3):
  print(v)
"""

NOT_SOLVED = 0
SOLVED = 1
TOO_FAR = 2

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
    assert len(self.lt) == len(self.joltage)

    # part2 stuff
    self.n_lights = len(self.joltage)
    self.max_press = max(self.joltage)
    self.units = []
    for button in self.buttons:
      self.units.append([1 if flp in button else 0 for flp in range(len(self.joltage))])

  def __repr__(self):
    return str(self)

  def __str__(self):
    return f"[{self.lights}]: {self.buttons} {self.joltage}"

  def run_sequence(self, flips):
    lights = [False] * len(self.lights)
    for flip in flips:
      for to_flip in flip:
        lights[to_flip] = not lights[to_flip]
    return lights

  def try_combos1(self):
    for flips in combos(self.buttons):
      l = self.run_sequence(flips)
      # print(flips, '==>', l)
      if self.lt == l:  # we win
        return len(flips)

  def is_solved(self, jolts):
   for light in range(self.n_lights):
     if jolts[light] > self.joltage[light]:
       return TOO_FAR
     if jolts[light] < self.joltage[light]:
       return NOT_SOLVED
   return SOLVED

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

  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for mach in self.machines:
       ret += mach.try_combos1()
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for machine in self.machines[0:4]:
      ret += do_part2(machine, verbose=self.doing_sample)
    return ret


def do_part2(machine, verbose=False):
  jolts = [0] * machine.n_lights
  best = machine.max_press * len(machine.buttons) + 1
  for solution in get_solutions(machine=machine, state=jolts, button=len(machine.buttons)-1, others=[], verbose=verbose):
     possible_solution = sum(solution)
     if possible_solution < best:
       best = possible_solution
     print("GOT", solution, 'best', best)
  return best
  

def get_solutions(machine, state, button, others, verbose):
  if button < 0:
    return
  #if button == 0:
  #  print("get solutions", state, button, others)
  # press this button all the possible times.
  for n_press in range(0, machine.max_press+1):
    jolts = [state[i] + machine.units[button][i] * n_press for i in range(machine.n_lights)]
    s = machine.is_solved(jolts)
    if s == TOO_FAR:
      return
    if s == SOLVED:
      print("SOLVED: button=%d:" % button, [n_press] + others)
      yield [n_press] + others
      return

    if button > 0:
      for sol in get_solutions(machine=machine, state=jolts, button=button-1, others=[n_press] + others, verbose=verbose):
         yield sol

[##..#.] (2) (4,5) (3,5) (0,5) (1,5) (1,2,4,5) {4,135,127,8,135,155}



day10.sample_test("""
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""", expect1=7, expect2=33)


if __name__ == '__main__':
  day10.run_and_check('input.txt', expect1=473, expect2=None)
