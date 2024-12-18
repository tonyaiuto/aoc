"""AOC 2020: intcode interpreter."""

import sys

_DEFAULT_TRACE = False

class Ins(object):
  """A dummy instruction set.

  Used for testing Intcode.
  """

  def __init__(self, opcode, arg):
    self.opcode = opcode
    self.arg = int(arg)

  def __repr__(self):
    return '%s %d' % (self.opcode, self.arg)


class Intcode(object):

  def __init__(self, trace=False, registers=None,
               input=None, get_input=None,
               terminate_on_end_of_input=False,
               max_cycles = 1000):
    # These are considered public to subclasses
    self.mem = []
    self.pc = 0
    self.acc = 0
    self.trace = trace or _DEFAULT_TRACE
    self.halted = False
    self.cycle = 0
    self.max_cycles = max_cycles

    self.input = input or []
    self.terminate_on_end_of_input = terminate_on_end_of_input
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
    self.cycle = 0
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

  def next_input(self):
    if not self.input:
      if self.terminate_on_end_of_input:
        self.halted = True
        return 0
      if self.get_input:
        self.push_input(self.get_input())
      else:
        print('Ran out of input and no get_input() supplied')
        assert False
    value = self.input[0]
    if self.trace:
      print('input:', value)
    self.input = self.input[1:]
    return value

  def run(self, loop_detect=False):
    self.pc = 0
    self.acc = 0
    self.cycles = 0
    if loop_detect:
      seen = set()
    while self.pc < len(self.mem):
      if self.is_halted:
        break
      self.cycles += 1
      if self.cycles > self.max_cycles:
        print('Possible infinite loop. More than %d cycles. Use max_cycles= to change.' % self.max_cycles)
        return 'loop'
      if loop_detect:
        if self.pc in seen:
          print('Loop', self.acc)
          return
        seen.add(self.pc)
      op = self.mem[self.pc]
      if self.trace:
        before = 'pc:%3d, ' % self.pc + self.reg_str() + ' [' +str(op) + ']'
      self.step(op)
      if self.trace:
        print(before, '->', self.reg_str())
    return

  def mem_at(self, reg):
    """Returns memory pointed to by a register.

    Essentially, register indirect.
    """
    if reg == 'pc':
      return self.mem[self.pc]
    return self.mem[self.registers[reg]]

  def inc_pc(self):
    self.pc = (self.pc + 1) % len(self.mem)

  def reg_str(self):
    if self.registers:
      return ','.join(['%c:%3d' % (r, self.registers[r]) for r in self.register_names])
    return 'acc:%d' % self.acc

  def one_line_trace(self, op=None):
    print('pc', self.pc, self.reg_str(), op or '')


class TestIntcode(Intcode):
  def __init__(self, **kwargs):
    super(TestIntcode, self).__init__(**kwargs)

  def reset(self):
    super(TestIntcode, self).reset()
 
  def step(self, op):
    if op.opcode == 1:
      self.acc = op.arg
    elif op.opcode == 99:
      self.halted = True
    else:
      raise Exception('unknown opcode: <%s>', str(op))
    self.pc = self.pc + 1
 

def check():
  # Smoke test
  cpu = TestIntcode()
  cpu.mem_append(Ins(1, 42))
  cpu.mem_append(Ins(99, 0))
  cpu.mem_append(Ins(666, 777))
  cpu.run()
  assert cpu.acc == 42
  assert cpu.is_halted
  assert cpu.pc == 2


if __name__ == '__main__':
  check()
  print('PASS:', __file__)
