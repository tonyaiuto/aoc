#!/usr/bin/env python3

def load_intcode(inp_path):
  with open(inp_path, 'r') as inp:
    return [int(i) for i in inp.read().split(',')]
  return None


def interp(mem):
  pc = 0
  while True:
    op = mem[pc]
    pc += 1
    if op == 99:
      # print('STOP')
      return
    elif op == 1:
      arg1 = mem[mem[pc]]
      arg2 = mem[mem[pc+1]]
      store = mem[pc+2]
      mem[store] = arg1 + arg2
      pc = pc + 3
    elif op == 2:
      arg1 = mem[mem[pc]]
      arg2 = mem[mem[pc+1]]
      store = mem[pc+2]
      mem[store] = arg1 * arg2
      pc = pc + 3
    else:
      print('illegal op:%d at %d' % (op, pc-1))
      return


def check(mem, expect_mem):
  interp(mem)
  for i in range(len(mem)):
    if mem[i] != expect_mem[i]:
      print('FAIL: %s !=> %s' % (mem, expect_mem))


check([1,0,0,0,99], [2,0,0,0,99])
check([2,3,0,3,99], [2,3,0,6,99])
check([2,4,4,5,99,0], [2,4,4,5,99,9801])
check([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])


def part1():
  mem = load_intcode('input_02.txt')
  assert len(mem) == 129
  mem[1] = 12
  mem[2] = 2
  interp(mem)
  print('part1:', mem[0])
  # part1: 5482655

def part2():
  orig_mem = load_intcode('input_02.txt')
  expect = 19690720

  for noun in range(100):
    for verb in range(100):
      mem = list(orig_mem)
      mem[1] = noun
      mem[2] = verb
      # print('%2d %2d' % (noun, verb))
      interp(mem)
      if mem[0] == expect:
        print('part2: %d' % (noun * 100 + verb))
        return


if __name__ == '__main__':
  part1()
  part2()

"""
"With terminology out of the way, we're ready to proceed. To complete
the gravity assist, you need to determine what pair of inputs produces
the output 19690720."

The inputs should still be provided to the program by replacing the values
at addresses 1 and 2, just like before. In this program, the value placed
in address 1 is called the noun, and the value placed in address 2 is
called the verb. Each of the two input values will be between 0 and 99,
inclusive.

Once the program has halted, its output is available at address 0, also
just like before. Each time you try a pair of inputs, make sure you first
reset the computer's memory to the values in the program (your puzzle
input) - in other words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output
19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2,
the answer would be 1202.)
"""
