"""AOC 2020: intcode interpreter."""

import sys

_DEFAULT_TRACE = False

class Ins(object):

  def __init__(self, opcode, arg):
    self.opcode = opcode
    self.arg = int(arg)

  def __repr__(self):
    return '%s %d' % (self.opcode, self.arg)


class Intcode(object):

  def __init__(self, trace=False, registers=None,
               input=None, get_input=None):
    self.mem = []
    self.pc = 0
    self.acc = 0
    self.trace = trace or _DEFAULT_TRACE
    self.halted = False

    self.input = input or []
    self.get_input = get_input
    self.extra_output = None
    self.out_buf = []

    if registers:
      self.register_names = registers
      self.registers = {}
      for r in self.register_names:
        self.registers[r] = 0
    else:
      self.register_names = []
    """
    self.rel_base = 0
    """

  def mem_append(self, any_value):
    """Load another value into the end of memory."""
    self.mem.append(any_value)

  def poke(self, address, any_value):
    self.mem[address] = any_value

  def reg(self, r):
    return self.registers[r]

  def reg_set(self, r, value):
    assert r in self.register_names
    self.registers[r] = value

  @property
  def is_halted(self):
    return self.halted

  def reset(self):
    self.halted = False
    self.pc = 0
    self.acc = 0
    for r in self.register_names:
      self.registers[r] = 0
    self.input = []
    if self.trace:
      print('RESET')
      self.one_line_trace()

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

  def push_input(self, more_input):
    if isinstance(more_input, list):
      self.input.extend(more_input)
    else:
      self.input.append(more_input)

  def run(self, loop_detect=False):
    self.pc = 0
    self.acc = 0
    n_cycles = 0
    if loop_detect:
      seen = set()
    while self.pc < len(self.mem):
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
        before = 'pc:%d,' % self.pc + self.reg_str() + ' [' +str(op) + ']'
      self.step(op)
      if self.trace:
        print(before, '->', self.reg_str())
    return

  def reg_str(self):
    if self.registers:
      return ' '.join(['%c:%d' % (r, self.registers[r]) for r in self.register_names])
    return 'acc:%d' % self.acc

  def one_line_trace(self, op=None):
    print('pc', self.pc, self.reg_str(), op or '')


"""
From 2019

OpCode = collections.namedtuple('OpCode', 'mnemonic op n_args n_store')

class IntCode(object):

  opcodes = {op.op: op for op in [
    OpCode('+', 1, 2, 1),
    OpCode('INPUT', 3, 0, 1),
    OpCode('RELBASE', 9, 1, 0),
  ]}

  modifiers = ['', '#', 'rel+']

  def __init__(self, mem, input=None, get_input=None):
    self.pc = 0
    self.mem = mem
    ...

  def extend_mem(self, max_addr):
    if len(self.mem) < max_addr + 1:
      # print("EXTEND: from %d to %d" % (len(self.mem), max_addr))
      self.mem += [0] * (max_addr + 1 - len(self.mem))
      # print("EXTEND: New len", len(self.mem))

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

    elif op == 4:
      if self.trace:
        print('output: ', arg1)
      output(arg1)
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

"""


class Op(object):

  def __init__(self, opcode, reg, v):
    self.opcode = opcode
    self.reg = reg
    if v in ('w', 'x', 'y', 'z'):
        self.vreg = v
        self.value = 0
    else:
      self.vreg = None
      self.value = 0
      if v is not None:
        self.value = int(v)

  def __repr__(self):
    ret = '%s %s' % (self.opcode, self.reg)
    if self.opcode != 'inp':
      if self.vreg:
        ret += ' ' + self.vreg
      else:
        ret += ' ' + str(self.value)
    return ret

  @staticmethod
  def parse(s):
    parts = s.split(' ')
    if len(parts) > 2:
      v = parts[2]
    else:
      v = None
    op = Op(opcode=parts[0], reg=parts[1], v=v)
    return op
 

class ALU(Intcode):

  def __init__(self, **kwargs):
    super(ALU, self).__init__(
        registers=('w', 'x', 'y', 'z'),
        **kwargs)

    self.w = 0
    self.x = 0
    self.y = 0
    self.z = 0

  def step(self, op):
    save_pc = self.pc
    r = op.reg
    a = self.reg(r)
    if op.vreg:
      v = self.reg(op.vreg)
    else:
      v = op.value

    if op.opcode == 'inp':
      # inp a - Read an input value and write it to variable a.
      if not self.input:
        assert self.get_input
        self.push_input(self.get_input())
      v = self.input[0]
      if v > 9:
        print('  bad input', v, 'in', self.input)
      self.reg_set(r, v)
      if self.trace:
        print('input', r, '<-', v)
      self.input = self.input[1:]
    elif op.opcode == 'add':
      # add a b - Add the value of a to the value of b,
      # then store the result in variable a.
      self.reg_set(r, a + v)
    elif op.opcode == 'mul':
      # mul a b - Multiply the value of a by the value of b,
      # then store the result in variable a.
      self.reg_set(r, a * v)
    elif op.opcode == 'div':
      # div a b - Divide the value of a by the value of b,
      # truncate the result to an integer,
      # then store the result in variable a.
      # (Here, "truncate" means to round the value toward zero.)
      assert v != 0
      self.reg_set(r, int(a / v))
    elif op.opcode == 'mod':
      # mod a b - Divide the value of a by the value of b, then store the
      # remainder in variable a. (This is also called the modulo operation.)
      assert a >= 0
      assert v > 0
      self.reg_set(r, a - v * int(a / v))
    elif op.opcode == 'eql':
      # eql a b - If the value of a and b are equal, then store the value
      # 1 in variable a. Otherwise, store the value 0 in variable a.
      self.reg_set(r, 1 if a == v else 0)
    else:
      print('bad opcode', op)
      raise Exception('illegal op:%s at %d' % (op, saved_pc))
    self.pc += 1

  @staticmethod
  def from_string(s):
    alu = ALU()
    for line in s.split('\n'):
      line = line.strip()
      if line:
        alu.mem_append(Op.parse(line))
    return alu


def check():
  alu = ALU.from_string("""
      inp w
      add z w
      mod z 2
      div w 2
      add y w
      mod y 2
      div w 2
      add x w
      mod x 2
      div w 2
      mod w 2""")
  for i in range(10):
    alu.reset()
    alu.push_input(int(i))
    alu.run()
    w = alu.reg('w')
    x = alu.reg('x')
    y = alu.reg('y')
    z = alu.reg('z')
    res = (((((w << 1) | x) << 1) | y) << 1) | z
    if res != i:
      print('alu_check: FAIL: Expected %x, got, %x' % (i, res))
      sys.exit(1)
  print('alu_check: PASS: binary convert')


if __name__ == '__main__':
  check()
