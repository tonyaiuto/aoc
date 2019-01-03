"""aoc 2018 day 21"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import sys

_VERBOSE = 0
_PART2 = False


class Proc(object):

  def __init__(this):
    this.n_reg = 6
    this.reg = [0] * this.n_reg
    # this.can_be = [range(16)] * 16
    this.ip_reg = 0
    this.ip = 0
    this.mem = []

  def instruction(this, opcode, a, b, c):
    # Every instruction consists of four values: an opcode, two inputs
    # (named A and B), and an output (named C), in that order. The opcode
    # specifies the behavior of the instruction and how the inputs are
    # interpreted. The output, C, is always treated as a register.

    # When the instruction pointer is bound to a register, its value is
    # written to that register just before each instruction is executed,
    # and the value of that register is written back to the instruction
    # pointer immediately after each instruction finishes execution.
    # Afterward, move to the next instruction by adding one to the
    # instruction pointer, even if the value in the instruction pointer
    # was just updated by an instruction. (Because of this, instructions
    # must effectively set the instruction pointer to the instruction
    # before the one they want executed next.)

    this.reg[this.ip_reg] = this.ip
    if _VERBOSE > 0:
      msg = 'ip=%d %s %s %d %d %d ' % (
         this.ip, this.reg, proc._NAMES[opcode], a, b, c)
    v = Proc._RAW_OPS[opcode](this, a, b)
    this.reg[c] = v
    this.ip = this.reg[this.ip_reg]
    this.ip += 1
    if _VERBOSE > 0:
      msg += str(this.reg)
      print(msg)
    if this.ip >= len(this.mem):
      raise ValueError('Halt: ip=%d' % this.ip)

  def NameToOpcode(this, name):
    return Proc._NAMES.index(name)

  def addr(this, a, b):
    """returns: r$a + r$b"""
    return this.reg[a] + this.reg[b]

  def addi(this, a, b):
    """returns: r$a + $b"""
    return this.reg[a] + b

  def mulr(this, a, b):
    """returns: r$a * r$b"""
    return this.reg[a] * this.reg[b]

  def muli(this, a, b):
    """returns: r$a * $b"""
    return this.reg[a] * b

  def banr(this, a, b):
    """returns: r$a & $b"""
    return this.reg[a] & this.reg[b]

  def bani(this, a, b):
    """returns: r$a & $b"""
    return this.reg[a] & b

  def borr(this, a, b):
    """returns: r$a | r$b"""
    return this.reg[a] | this.reg[b]

  def bori(this, a, b):
    """returns: r$a | $b"""
    return this.reg[a] | b

  def setr(this, a, b):
    """returns: r$a"""
    return this.reg[a]

  def seti(this, a, b):
    """returns: $a"""
    return a

  def gtir(this, a, b):
    """returns: $a > r$b"""
    return 1 if a > this.reg[b] else 0

  def gtri(this, a, b):
    """returns: r$a > $b"""
    return 1 if this.reg[a] > b else 0

  def gtrr(this, a, b):
    """returns: r$a > r$b"""
    return 1 if this.reg[a] > this.reg[b] else 0

  def eqir(this, a, b):
    """returns: $a == r$b"""
    return 1 if a == this.reg[b] else 0

  def eqri(this, a, b):
    """returns: r$a == $b"""
    return 1 if this.reg[a] == b else 0

  def eqrr(this, a, b):
    """returns: r$a == r$b"""
    return 1 if this.reg[a] == this.reg[b] else 0

  def LoadProg(this, inp):
    for line in inp:
      l = line.strip()
      if l.startswith('#ip '):
        this.ip_reg = int(l[4:])
        if _VERBOSE > 0:
          print('#ip=r%d' % this.ip_reg)
        continue
      if l == '### END INPUT':
        break
      if l == '' or l[0] == '#':
        continue
      instr = l.split(' ')
      opcode = proc.NameToOpcode(instr[0])
      args = [int(s) for s in instr[1:]]
      this.mem.append([opcode] + args)

  def Clock(this):
    inst = this.mem[this.ip]
    proc.instruction(inst[0], inst[1], inst[2], inst[3])

  def Print(this):
    for ip in range(len(this.mem)):
      inst = this.mem[ip]
      opcode = Proc._NAMES[inst[0]]
      print('%2d: %s %d %d %d' % (ip, opcode, inst[1], inst[2], inst[3]))

  def ToCode(this):
    print('// int %s;' % ', '.join(
        ['r%d' % i for i in range(this.n_reg) if i != this.ip_reg]))
    print('void prog() {')
    ip_str = 'r%d' % this.ip_reg
    for ip in range(len(this.mem)):
      inst = this.mem[ip]
      op = Proc._RAW_OPS[inst[0]]
      opcode = Proc._NAMES[inst[0]]
      asm = '%s %d %d %d' % (opcode, inst[1], inst[2], inst[3])

      line = ''
      # Modify program counter
      if inst[3] == this.ip_reg:
        if inst[1] == this.ip_reg and opcode == 'addi':
          line = 'goto l%d' % (ip + inst[2] + 1)
        if opcode == 'addr':
          cond_r = inst[2] if inst[1] == this.ip_reg else inst[1]
          line = 'if (r%d) goto l%d' % (cond_r, ip + 2)
        elif opcode == 'seti':
          if inst[1] < ip:
            print('\tpreg(%d);' % ip)
          line = 'goto l%d' % (inst[1] + 1)
      if not line and op.__doc__:
        i = op.__doc__.index('returns:')
        if i >= 0:
          code = op.__doc__[i+8:].strip()
          code = code.replace('$a', '%d' % inst[1])
          code = code.replace('$b', '%d' % inst[2])
          code = code.replace(ip_str, '%d' % ip)
          line = ('r%d = %s' % (inst[3], code))
          line = line.replace(ip_str, 'pc')
      if line:
        line += ';'
        line += ' ' * 30
        print('l%d:\t%s // %s' % (ip, line[0:30], asm))
      else:
        print('l%d:\t%s' % (ip, asm))
    print('l%d:\treturn;' % len(this.mem))
    print('}')

  _RAW_OPS = [
      addr, addi, mulr, muli,
      banr, bani, borr, bori,
      setr, seti,
      gtir, gtri, gtrr,
      eqir, eqri, eqrr,
  ]
  _NAMES = [
      'addr', 'addi', 'mulr', 'muli',
      'banr', 'bani', 'borr', 'bori',
      'setr', 'seti',
      'gtir', 'gtri', 'gtrr',
      'eqir', 'eqri', 'eqrr',
  ]


def part1(proc):
  # What value is left in register 0 when the background process halts?
  while True:
    try:
      proc.Clock()
    except ValueError as e:
      print(str(e))
      break
  print('r0=%d' % proc.reg[0])


if __name__ == '__main__':
  iarg = 1
  dump = False
  while iarg < len(sys.argv) and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      _VERBOSE += 1
      iarg += 1
    if sys.argv[iarg] == '-d':
      dump = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      iarg += 1

  proc = Proc()
  with open(sys.argv[iarg]) as inp:
    proc.LoadProg(inp)
  if dump:
    proc.Print()

  proc.ToCode()

  if _PART2:
    proc.reg[0] = 1
  # part1(proc)
