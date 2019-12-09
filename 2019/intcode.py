#!/usr/bin/env python3

class IntCode(object):

  def __init__(self, mem, input=None):
    self.pc = 0
    self.mem = mem
    self.input = input
    self.halted = False
    self.rel_base = 0

  def extend_mem(self, max_addr):
    if len(self.mem) < max_addr + 1:
      # print("EXTEND: from %d to %d" % (len(self.mem), max_addr))
      self.mem += [0] * (max_addr + 1 - len(self.mem))
      # print("EXTEND: New len", len(self.mem))

  def push_input(self, more_input):
    self.input.append(more_input)

  @property
  def is_halted(self):
    return self.halted

  def fetch_p(self, mode):
    word = self.mem[self.pc]
    self.pc += 1
    if mode == 0:
      if word > len(self.mem):
        return 0
      self.extend_mem(word)
      return self.mem[word]
    elif mode == 1:
      return word
    elif mode == 2:
      addr = self.rel_base+word
      self.extend_mem(addr)
      return self.mem[addr]
    else:
      assert mode in [0, 1]

  def fetch_store(self):
    store = self.mem[self.pc]
    self.pc = self.pc + 1
    self.extend_mem(store)
    return store

  def run(self):
    self.pc = 0
    ret = []
    while True:
      out = self.run_until_output()
      if self.halted:
        return ret
      else:
        ret.append(out)

  def run_until_output(self):
    if self.halted:
      return None
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
        self.halted = True
        break
      elif op == 1:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.fetch_store()
        self.mem[store] = arg1 + arg2
      elif op == 2:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.fetch_store()
        self.mem[store] = arg1 * arg2
      elif op == 3:
        store = self.fetch_store()
        self.mem[store] = self.input[0]
        self.input = self.input[1:]
      elif op == 4:
        arg1 = self.fetch_p(p1_mode)
        # print(arg1)
        return arg1
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
        store = self.fetch_store()
        if arg1 < arg2:
          self.mem[store] = 1
        else:
          self.mem[store] = 0
      elif op == 8:
        arg1 = self.fetch_p(p1_mode)
        arg2 = self.fetch_p(p2_mode)
        store = self.fetch_store()
        if arg1 == arg2:
          self.mem[store] = 1
        else:
          self.mem[store] = 0
      elif op == 9:
        self.rel_base += self.mem[self.pc]
        self.pc = self.pc + 1
      else:
        raise Exception('illegal op:%d at %d' % (op, self.pc-1))


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
    msg = None
    for i in range(len(expect_out)):
      if i > len(out) - 1:
        msg = 'expected output is longer (%d) than actual output(%d)' % (
            len(expect_out), len(out))
      elif out[i] != expect_out[i]:
        msg = 'FAIL: at pos %d, output %s !=> %s' % (i, out, expect_out)
    if msg:
      print(msg)
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
  print('PASS: intcode self_check_01')
  assert test05()
  print('PASS: intcode self_check_05')

  # takes no input and produces a copy of itself as output.
  prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
  assert check(list(prog), expect_out=prog)
  ic = IntCode(mem=[1102,34915192,34915192,7,4,7,99,0])
  output = ic.run()
  assert 16 == len(str(output[0]))
  # 104,1125899906842624,99 should output the large number in the middle.
  assert check([104,1125899906842624,99], expect_out=[1125899906842624])
  print('PASS: intcode self_check_09')


self_check()
