#!/usr/bin/env python3

import intcode


def part1():
  # The BOOST program will ask for a single input; run it in test mode
  # by providing it the value 1. It will perform a series of checks on
  # each opcode, output any opcodes (and the associated parameter modes)
  # that seem to be functioning incorrectly, and finally output a BOOST
  # keycode.

  # Once your Intcode computer is fully functional, the BOOST program
  # should report no malfunctioning opcodes when run in test mode;
  # it should only output a single value, the BOOST keycode. What
  # BOOST keycode does it produce?
  mem = intcode.load_intcode('input_09.txt')
  ic = intcode.IntCode(list(mem), input=[1])
  output = ic.run()
  print('part1: boost keycode =', output[0])
  assert 3533056970 == output[0]


def part2():
  # The program runs in sensor boost mode by providing the input
  # instruction the value 2. Once run, it will boost the sensors
  # automatically, but it might take a few seconds to complete the
  # operation on slower hardware. In sensor boost mode, the program
  # will output a single value: the coordinates of the distress signal.

  # Run the BOOST program in sensor boost mode. What are the coordinates
  # of the distress signal?
  mem = intcode.load_intcode('input_09.txt')
  ic = intcode.IntCode(list(mem), input=[2])
  output = ic.run()
  print('part2: distress =', output[0])
  assert 72852 == output[0]

if __name__ == '__main__':
  part1()
  part2()
