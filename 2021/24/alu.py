"""AOC 2021: day 24 ALU intcode interpreter."""

import sys

from tools import intcode

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
 

class ALU(intcode.Intcode):

  class ZCheck(Exception):
    def __init__(self, message):
      self.message = message

  def __init__(self, **kwargs):
    super(ALU, self).__init__(
        registers=('w', 'x', 'y', 'z'),
        **kwargs)
    self.expectz = []
    
  def reset(self):
    super(ALU, self).reset()
    self.n_input = 0

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
      curz = self.reg('z')
      if self.expectz and self.n_input < len(self.expectz):
        e = self.expectz[self.n_input]
        if curz != e:
          raise ALU.ZCheck('Ask for input %d: expect %d, got %d' % (
              self.n_input, e, curz))
      self.n_input += 1
      v = self.next_input()
      if v > 9:
        print('  bad input', v, 'in', self.input)
      self.reg_set(r, v)
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
      self.reg_set(r, a // v)
    elif op.opcode == 'mod':
      # mod a b - Divide the value of a by the value of b, then store the
      # remainder in variable a. (This is also called the modulo operation.)
      assert a >= 0
      assert v > 0
      # MAYBE? self.reg_set(r, a - v * int(a / v))
      self.reg_set(r, a % v)
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
