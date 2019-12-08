#!/usr/bin/env python3

import intcode


def run_phases(mem, phases):
  amp= []
  thrust = 0
  for phase in phases:
    ic = intcode.IntCode(list(mem), input=[phase, thrust])
    output = ic.run()
    thrust = output[0]
  # print('== Phases:', phases, 'thrust:', thrust)
  return thrust


def check_07(mem, phases, expect_thrust):
  thrust = run_phases(mem, phases)
  assert thrust == expect_thrust

check_07([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0], 43210)


check_07([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
         [0,1,2,3,4],
         54321)

check_07([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
          1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
         [1,0,4,3,2],
         65210)


def find_maximum_thrust(phase_choices, mem, amp_runner):
  max_thrust = 0
  phases = [-1] * 5
  for a in phase_choices:
    phases[0] = a
    for b in phase_choices:
      if b  == a:
        continue
      phases[1] = b
      for c in phase_choices:
        if c  == a or c == b:
          continue
        phases[2] = c
        for d in phase_choices:
          if d  == a or d == b or d == c:
            continue
          phases[3] = d
          for e in phase_choices:
            if e  == a or e == b or e == c or e == d:
              continue
            phases[4] = e
            thrust = amp_runner(mem, phases)
            if thrust > max_thrust:
              max_thrust = thrust
              max_phases = list(phases)
              print('new max', max_phases, max_thrust)
  return max_thrust, max_phases


def part1():
  mem = intcode.load_intcode('input_07.txt')
  max_thrust, max_phases = find_maximum_thrust([0, 1, 2, 3, 4], mem, run_phases)
  assert max_phases == [0, 3, 4, 2, 1]
  assert max_thrust == 65464
  print('part1:', max_phases, max_thrust)


def run_phases_feedback(mem, phases):
  amp= []
  thrust = 0
  while True:
    for phase in phases:
      ic = intcode.IntCode(list(mem), input=[phase, thrust])
      output = ic.run()
      thrust = output[0]
    # print('== Phases:', phases, 'thrust:', thrust)
  return thrust


def check_07_feedback(mem, phases, expect_thrust):
  # thrust = run_phases_feedback(mem, phases)
  # assert thrust == expect_thrust
  pass


check_07_feedback(mem=[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                       27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
                  phases=[9,8,7,6,5],
                  expect_thrust=139629729)


def part2():
  mem = intcode.load_intcode('input_07.txt')
  max_thrust, max_phases = find_maximum_thrust([5, 6, 7, 8, 9], mem, run_phases_feedback)
  print('part2:', max_phases, max_thrust)
  #assert max_phases == [0, 3, 4, 2, 1]
  #assert max_thrust == 65464


if __name__ == '__main__':
  part1()
  # part2()
