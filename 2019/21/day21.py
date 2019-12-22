#!/usr/bin/env python3

import sys
import textwrap

# from elf_image import ElfImage
import intcode

def asc_to_str(s):
  try:
    return ''.join(chr(c) for c in s)
  except ValueError as e:
    return s


class SpringDroid(object):

  def __init__(self, mem):
    self.computer = intcode.IntCode(list(mem))

  def send_program(self, prog):
    assert len(prog) <= 15
    for cmd in prog:
      print(cmd)
      ascii_code = intcode.code_to_ascii(cmd, sep=' ')
      self.computer.push_input(ascii_code)


def part1():
  mem = intcode.load_intcode('input_21.txt')
  robot = SpringDroid(list(mem))

  while not robot.computer.is_halted:
    print(robot.computer.run_until_newline())
    robot.send_program([
        ['NOT', 'B', 'J'],
        ['AND', 'A', 'J'],
        ['NOT', 'C', 'T'],
        ['AND', 'A', 'T'],
        ['AND', 'B', 'T'],
        ['OR',  'T', 'J'],
        ['NOT', 'A', 'T'],
        ['OR',  'T', 'J'],
        ['AND', 'D', 'J'],
        ])
    robot.send_program([['WALK']])
    while True:
      disp = robot.computer.run_until_newline()
      if disp.strip() or robot.computer.extra_output:
        break
    print(disp)
    if disp == 'Walking...':
      disp = robot.computer.run_until_newline()
    else:
      out = robot.computer.run()
      print(asc_to_str(out))
      break
    if robot.computer.extra_output:
      break

  damage = robot.computer.extra_output
  print('part1: damage', damage)
  assert 19352638 == damage

def part2():
  mem = intcode.load_intcode('input_21.txt')
  robot = SpringDroid(list(mem))

  while not robot.computer.is_halted:
    print(robot.computer.run_until_newline())
    robot.send_program([
	['NOT', 'E', 'J'],
	['NOT', 'F', 'T'],
	['AND', 'T', 'J'],
	['NOT', 'G', 'T'],
	['AND', 'T', 'J'],
	['AND', 'H', 'J'],   # ????...#
	['NOT', 'B', 'T'],
	['OR',  'T', 'J'],
	['NOT', 'C', 'T'],
	['OR',  'T', 'J'],
	['AND', 'D', 'J'],   # ???D...#
	['AND', 'H', 'J'],   # ???D...#
	['NOT', 'A', 'T'],
	['OR',  'T', 'J'],   # .???????
        ])


    robot.send_program([['RUN']])
    while True:
      disp = robot.computer.run_until_newline()
      if disp.strip() or robot.computer.extra_output:
        break
    print(disp)
    if disp == 'Walking...':
      disp = robot.computer.run_until_newline()
    else:
      out = robot.computer.run()
      for word in out:
        if word > 255:
          damage = word
          break
      print(asc_to_str(out))
      break
    if robot.computer.extra_output:
      damage = robot.computer.extra_output

  print('part2: damage', damage)
  assert 1141251258 == damage


if __name__ == '__main__':
  part1()
  part2()
