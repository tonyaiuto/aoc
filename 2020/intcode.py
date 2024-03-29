"""AOC 2020: intcode interpreter."""

_DEFAULT_TRACE = False

class Ins(object):

  def __init__(self, opcode, arg):
    self.opcode = opcode
    self.arg = int(arg)

  def __repr__(self):
    return '%s %d' % (self.opcode, self.arg)


class Intcode(object):

  def __init__(self, trace=False):
    self.mem = []
    self.pc = 0
    self.acc = 0
    self.trace = trace or _DEFAULT_TRACE
    self.halted = False

    """
    self.input = input or []
    self.get_input = get_input
    self.rel_base = 0
    self.extra_output = None
    self.out_buf = []
    """

  @property
  def is_halted(self):
    return self.halted

  def reset(self):
    self.halted = False
    self.pc = 0

  def set_trace(self, trace):
    ret = self.trace
    self.trace = trace
    return ret

  def Xsave_output(self, word):
    self.out_buf.append(word)

  def Xread_output(self):
    ret = self.out_buf
    self.out_buf = []
    return ret


  def run(self, loop_detect=False):
    self.pc = 0
    self.acc = 0
    n_cycles = 0
    if loop_detect:
      seen = set()
    while self.pc != len(self.mem):
      n_cycles += 1
      if n_cycles > 1000:
        # print('====== infinite loop')
        return 'loop'
      if loop_detect:
        if self.pc in seen:
          print('Loop', self.acc)
          return
        seen.add(self.pc)
      op = self.mem[self.pc]
      if self.trace:
        print('pc', self.pc, 'acc', self.acc, op)
      self.step(op)
    return


  def step(self, op):
    save_pc = self.pc
    if op.opcode == 'nop':
      self.pc += 1
      return
    elif op.opcode == 'acc':
      self.acc += op.arg
      self.pc += 1
      return
    elif op.opcode == 'jmp':
      self.pc += op.arg
      return
    else:
      print('bad opcode', op)
      raise Exception('illegal op:%s at %d' % (op, saved_pc))
    return None



def make_proc(s):
  proc = Intcode()
  for line in s.split('\n'):
    line = line.strip()
    if line:
      x = line.split(' ')
      proc.mem.append(Ins(x[0], x[1]))
  return proc


def self_check():
   proc = make_proc("""
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""")
   proc.run(loop_detect=True)
   assert proc.acc == 5


if __name__ == '__main__':
  self_check()
  print('PASS:', __file__)

"""
From 2019
#!/usr/bin/env python3

import collections

OpCode = collections.namedtuple('OpCode', 'mnemonic op n_args n_store')

_DEFAULT_TRACE = False

class IntCode(object):

  opcodes = {op.op: op for op in [
    OpCode('+', 1, 2, 1),
    OpCode('*', 2, 2, 1),
    OpCode('INPUT', 3, 0, 1),
    OpCode('OUTPUT', 4, 1, 0),
    OpCode('BNE', 5, 2, 0),
    OpCode('BEQ', 6, 2, 0),
    OpCode('LT', 7, 2, 1),
    OpCode('EQ', 8, 2, 1),
    OpCode('RELBASE', 9, 1, 0),
    OpCode('HALT', 99, 0, 0),
  ]}

  modifiers = ['', '#', 'rel+']

  def __init__(self, mem, input=None, get_input=None):
    self.pc = 0
    self.mem = mem
    self.input = input or []
    self.get_input = get_input
    self.halted = False
    self.rel_base = 0
    self.extra_output = None
    self.trace = _DEFAULT_TRACE
    self.out_buf = []

  def reset(self):
    self.halted = False
    self.pc = 0

  def set_trace(self, trace):
    ret = self.trace
    self.trace = trace
    return ret

  def save_output(self, word):
    self.out_buf.append(word)

  def read_output(self):
    ret = self.out_buf
    self.out_buf = []
    return ret

  def extend_mem(self, max_addr):
    if len(self.mem) < max_addr + 1:
      # print("EXTEND: from %d to %d" % (len(self.mem), max_addr))
      self.mem += [0] * (max_addr + 1 - len(self.mem))
      # print("EXTEND: New len", len(self.mem))

  def poke(self, address, value):
    self.mem[address] = value

  def push_input(self, more_input):
    if isinstance(more_input, list):
      self.input.extend(more_input)
    else:
      self.input.append(more_input)

  # Fetch parameter
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
      addr = self.rel_base + word
      self.extend_mem(addr)
      return self.mem[addr]
    else:
      assert mode in [0, 1, 2]

  def fetch_store(self, mode):
    store = self.mem[self.pc]
    self.pc = self.pc + 1
    if mode == 2:
      store = self.rel_base + store
    else:
      assert mode in [0, 2]
    self.extend_mem(store)
    return store

  def run(self):
    ret = []
    while True:
      out = self.run_until_output()
      if self.halted:
        return ret
      else:
        ret.append(out)

  def run_until_newline(self):
    return self.run_until_terminator(self, ['\n'])

  def run_until_terminator(self, terminators):
    line = []
    terminators = [ord(c) for c in terminators]
    while True:
      word = self.run_until_output()
      if not word:
        break
      if word in terminators:
        if word >= ord(' '):
          line.append(chr(word))
        break
      if word > ord('z'):
        print('Unexpected word', word)
        self.extra_output = word
        break
      line.append(chr(word))
    return ''.join(line)

  def run_until_output(self):
    out = []
    while not self.halted:
      out = self.step()
      if self.out_buf:
        ret = self.out_buf[0]
        self.out_buf = self.out_buf[1:]
        return ret
    return None

  def step(self, output=None):
    if not output:
      output = lambda word: self.save_output(word)
    if self.halted:
      return None
    op_start = self.pc
    word = self.mem[self.pc]
    self.pc += 1
    op = word % 100
    mode = word // 100

    opcode = IntCode.opcodes[op]
    msg = 'OP: pc=%d, %s %s' % (self.pc-1, opcode.mnemonic, self.mem[self.pc-1])
    if opcode.n_args >= 1:
      arg1 = self.fetch_p(mode % 10)
      msg += ' %s%d (=%d)' % (IntCode.modifiers[mode % 10], self.mem[self.pc-1], arg1)
      mode = mode // 10
    if opcode.n_args >= 2:
      arg2 = self.fetch_p(mode % 10)
      msg += ' %s%d (=%d)' % (IntCode.modifiers[mode % 10], self.mem[self.pc-1], arg2)
      mode = mode // 10
    if opcode.n_store >= 1:
      store = self.fetch_store(mode % 10)
      msg += ' %s%d (=%d)' % (IntCode.modifiers[mode % 10], self.mem[self.pc-1], store)
      mode = mode // 10
    if self.trace:
      print(msg)

    if op == 99:
      self.halted = True
      return None
    elif op == 1:
      self.mem[store] = arg1 + arg2
    elif op == 2:
      self.mem[store] = arg1 * arg2
    elif op == 3:
      if not self.input:
        assert self.get_input
        self.push_input(self.get_input())
      self.mem[store] = self.input[0]
      self.input = self.input[1:]
    elif op == 4:
      if self.trace:
        print('output: ', arg1)
      output(arg1)
    elif op == 5:
      if arg1 != 0:
        self.pc = arg2
    elif op == 6:
      if arg1 == 0:
        self.pc = arg2
    elif op == 7:
      if arg1 < arg2:
        self.mem[store] = 1
      else:
        self.mem[store] = 0
    elif op == 8:
      if arg1 == arg2:
        self.mem[store] = 1
      else:
        self.mem[store] = 0
    elif op == 9:
      self.rel_base += arg1
    else:
      raise Exception('illegal op:%d at %d' % (op, self.pc-1))
    return None


def load_intcode(inp_path):
  with open(inp_path, 'r') as inp:
    return [int(i) for i in inp.read().split(',')]
  return None


def code_to_ascii(code, sep=',', verbose=False):
  ret = []
  for word in code:
    if ret:
      ret.append(ord(sep))
    if isinstance(word, str):
      for c in word:
        ret.append(ord(c))
    else:
      for c in str(word):
        ret.append(ord(c))
  # assert len(ret) <= 20
  ret.append(10)
  if verbose:
    print('%s => %s' % (code, ret))
  return ret

def print_final_output(self):
  line = ''
  while True:
    out = self.run_until_output()
    if self.is_halted:
      break
    c = chr(out)
    if c == '\n':
      print(line)
      line = ''
    else:
      line += c
  if line:
    print(line)


def asc_to_str(s):
  try:
    return ''.join(chr(c) for c in s)
  except ValueError as e:
    return s


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
"""
