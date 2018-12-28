"""aoc 2018 day 19"""

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
    this.raw_ops = [
        Proc.addr, Proc.addi, Proc.mulr, Proc.muli,
        Proc.banr, Proc.bani, Proc.borr, Proc.bori,
        Proc.setr, Proc.seti,
        Proc.gtir, Proc.gtri, Proc.gtrr,
        Proc.eqir, Proc.eqri, Proc.eqrr,
    ]
    this.names = [
        'addr', 'addi', 'mulr', 'muli',
        'banr', 'bani', 'borr', 'bori',
        'setr', 'seti',
        'gtir', 'gtri', 'gtrr',
        'eqir', 'eqri', 'eqrr',
    ]
    # this.can_be = [range(16)] * 16
    this.ip_reg = 2  # HACK. From input
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
         this.ip, this.reg, this.names[opcode], a, b, c)
    v = this.raw_ops[opcode](this, a, b)
    this.reg[c] = v
    this.ip = this.reg[this.ip_reg]
    this.ip += 1
    if _VERBOSE > 0:
      msg += str(this.reg)
      print(msg)
    if this.ip >= len(this.mem):
      raise ValueError('Halt: ip=%d' % this.ip)

  def NameToOpcode(this, name):
    return this.names.index(name)

  def addr(this, a, b):
    return this.reg[a] + this.reg[b]

  def addi(this, a, b):
    return this.reg[a] + b

  def mulr(this, a, b):
    return this.reg[a] * this.reg[b]

  def muli(this, a, b):
    return this.reg[a] * b

  def banr(this, a, b):
    return this.reg[a] & this.reg[b]

  def bani(this, a, b):
    return this.reg[a] & b

  def borr(this, a, b):
    return this.reg[a] | this.reg[b]

  def bori(this, a, b):
    return this.reg[a] | b

  def setr(this, a, b):
    return this.reg[a]

  def seti(this, a, b):
    return a

  def gtir(this, a, b):
    return 1 if a > this.reg[b] else 0

  def gtri(this, a, b):
    return 1 if this.reg[a] > b else 0

  def gtrr(this, a, b):
    return 1 if this.reg[a] > this.reg[b] else 0

  def eqir(this, a, b):
    return 1 if a == this.reg[b] else 0

  def eqri(this, a, b):
    return 1 if this.reg[a] == b else 0

  def eqrr(this, a, b):
    return 1 if this.reg[a] == this.reg[b] else 0

  def LoadProg(this, inp):
    for line in inp:
      l = line.strip()
      if l.startswith('#ip '):
        this.ip_reg = int(l[4:])
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
  do_part2 = False
  while len(sys.argv) > 1 and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      _VERBOSE += 1
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      do_part2 = True
      iarg += 1

  proc = Proc()
  with open(sys.argv[iarg]) as inp:
    proc.LoadProg(inp)

  if do_part2:
    proc.reg[0] = 1
  part1(proc)
