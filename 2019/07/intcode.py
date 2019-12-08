#!/usr/bin/env python3

class IntCode(object):

  def __init__(self, mem, input=None):
    self.pc = 0
    self.mem = mem
    self.input = input
    self.input_pos = 0

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
    output = []

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
        break
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
        self.mem[arg1] = self.input[self.input_pos]
        self.input_pos += 1
      elif op == 4:
        arg1 = self.fetch_p(p1_mode)
        output.append(arg1)
        # print(arg1)
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
    return output


def load_intcode(inp_path):
  with open(inp_path, 'r') as inp:
    return [int(i) for i in inp.read().split(',')]
  return None


def check(mem, expect_mem=None, input=None, expect_out=None):
  ic = IntCode(mem, input=input)
  out = ic.run()
  if expect_mem:
    for i in range(len(expect_mem)):
      if mem[i] != expect_mem[i]:
        print('FAIL: %s !=> %s' % (mem, expect_mem))
        return False
  if expect_out:
    for i in range(len(expect_out)):
      if out[i] != expect_out[i]:
        print('FAIL: output %s !=> %s' % (out, expect_out))
        return False
  return True


def test05():
  mem = load_intcode('../05/input_05.txt')
  return check(mem, expect_mem=[3], input=[1],
               expect_out=[0, 0, 0, 0, 0, 0, 0, 0, 0, 9938601])


def self_check():
  assert check([1,0,0,0,99], expect_mem=[2,0,0,0,99])
  assert check([2,3,0,3,99], expect_mem=[2,3,0,6,99])
  assert check([2,4,4,5,99,0], expect_mem=[2,4,4,5,99,9801])
  assert check([1,1,1,4,99,5,6,0,99], expect_mem=[30,1,1,4,2,5,6,0,99])
  assert check([1002,4,3,4,33], expect_mem=[1002,4,3,4,99])
  assert test05()
  print('PASS: intcode self_check')

self_check()
