#!/usr/bin/env python3

def load_intcode(inp_path):
  with open(inp_path, 'r') as inp:
    return [int(i) for i in inp.read().split(',')]
  return None


class IntCode(object):

  def __init__(self, mem, input=None):
    self.pc = 0
    self.mem = mem
    self.input = input

  def fetch_p(self, mode):
    word = self.mem[self.pc]
    self.pc += 1
    if mode == 0:
      return self.mem[word]
    elif mode == 1:
      return word
    else:
      assert mode in [0, 1]


  def run(self):
    self.pc = 0

    while True:
      word = self.mem[self.pc]
      op = word % 100
      p1_mode = (word // 100) % 10
      p2_mode = (word // 1000) % 10
      p3_mode = (word // 10000) % 10
      if p3_mode > 0:
        print('immediate p3:', word)

      self.pc += 1
      if op == 99:
        # print('STOP')
        return
      elif op == 1:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.mem[self.pc]
        self.pc = self.pc + 1
        self.mem[store] = arg1 + arg2
      elif op == 2:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.mem[self.pc]
        self.pc = self.pc + 1
        self.mem[store] = arg1 * arg2
      elif op == 3:
        arg1 = self.mem[self.pc]
        self.pc = self.pc + 1
        self.mem[arg1] = self.input
      elif op == 4:
        arg1 = self.fetch_p(p1_mode)
        print(arg1)
      elif op == 5:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        if arg1 != 0:
          self.pc = arg2
      elif op == 6:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        if arg1 == 0:
          self.pc = arg2
      elif op == 7:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.mem[self.pc]
        self.pc = self.pc + 1
        if arg1 < arg2:
          self.mem[store] = 1
        else:
          self.mem[store] = 0
      elif op == 8:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.mem[self.pc]
        self.pc = self.pc + 1
        if arg1 == arg2:
          self.mem[store] = 1
        else:
          self.mem[store] = 0
      else:
        print('illegal op:%d at %d' % (op, self.pc-1))
        return


def check(mem, expect_mem):
  ic = IntCode(mem)
  ic.run()
  for i in range(len(mem)):
    if mem[i] != expect_mem[i]:
      print('FAIL: %s !=> %s' % (mem, expect_mem))


check([1,0,0,0,99], [2,0,0,0,99])
check([2,3,0,3,99], [2,3,0,6,99])
check([2,4,4,5,99,0], [2,4,4,5,99,9801])
check([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
check([1002,4,3,4,33], [1002,4,3,4,99])


def part1():
  mem = load_intcode('input_05.txt')
  ic = IntCode(mem, input=1)
  ic.run()
  print('part1:', mem[0])
  # part1: 5482655

def part2():
  mem = load_intcode('input_05.txt')
  ic = IntCode(mem, input=5)
  ic.run()


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
