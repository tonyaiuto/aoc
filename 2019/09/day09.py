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
  ic.set_trace(True)
  output = ic.run()
  print('part1: boost keycode =', output[0])
  assert 3533056970 == output[0]


if __name__ == '__main__':
  part1()
  # part2()
