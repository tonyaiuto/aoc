"""aoc 2018 day 16"""

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
    this.reg = [0] * 4
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
    this.can_be = [range(16)] * 16

  def instruction(this, opcode, a, b, c):
    # Every instruction consists of four values: an opcode, two inputs
    # (named A and B), and an output (named C), in that order. The opcode
    # specifies the behavior of the instruction and how the inputs are
    # interpreted. The output, C, is always treated as a register.

    v = this.raw_ops[opcode](this, a, b)
    if _VERBOSE > 1:
      print('   %s: r%d <- %d <- r%d:%d, r%d:%d' % (
          this.names[opcode], c, v, a, this.reg[a], b, this.reg[b]))
    this.reg[c] = v

  #[2, 3, 3, 2] ([11, 0, 3, 0]) -> [1, 3, 3, 2]
  # an be raw ops []

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

  def TrySample(this, sample):
    print(sample)
    try_op = sample.op[0]
    could_be = []
    for op in this.can_be[try_op]:
      this.reg = list(sample.before)
      this.instruction(op, sample.op[1], sample.op[2], sample.op[3])
      # this.raw_ops[op](this, sample.op[1], sample.op[2], sample.op[3])
      if this.reg == sample.after:
        if _VERBOSE > 2:
          print('  could be %d' % op)
        could_be.append(op)
    print('  can be raw ops %s' % could_be)
    if _PART2:
      this.can_be[try_op] = could_be
      assert len(could_be) > 0
      if len(could_be) == 1:
        taken = could_be[0]
        for op in range(16):
          if op != try_op:
            this.can_be[op] = [o for o in this.can_be[op] if o != taken]
    return len(could_be)

class Sample(object):

  def __init__(this, before, after, op):
    this.before = before
    this.after = after
    this.op = op

  def __str__(this):
    return '%s (%s) -> %s' % (this.before, this.op, this.after)

  @staticmethod
  def Read(inp):
    for line in inp:
      l = line.strip()
      if l == '':
        continue
      if l.startswith('='):
        return None
      if l.startswith('Before:'):
        # Before: [3, 2, 1, 1]
        before = [int(s) for s in l[7:].replace('[', '').replace(']', '').split(',')]
      if l[0].isdigit():
        # 9 2 1 2
        op = [int(s) for s in l.split(' ')]
      if l.startswith('After:'):
        # After:  [3, 2, 2, 1]
        after = [int(s) for s in l[6:].replace('[', '').replace(']', '').split(',')]
        return Sample(before, after, op)


"""

This sample shows the effect of the instruction 9 2 1 2 on the
registers. Before the instruction is executed, register 0 has value
3, register 1 has value 2, and registers 2 and 3 have value 1. After
the instruction is executed, register 2's value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed
with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes
listed above, but only three of them behave in a way that would
cause the result shown in the sample:

Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.
None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle
input). The manual also includes a small test program (the second
section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input
behave like three or more opcodes?
"""

if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while len(sys.argv) > 1 and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      do_part2 = True
      iarg += 1

  proc = Proc()
  np1 = 0
  n_samples = 0
  with open(sys.argv[iarg]) as inp:
    while True:
      sample = Sample.Read(inp)
      if not sample:
        break
      n_samples += 1
      npossible = proc.TrySample(sample)
      if npossible >= 3:
        np1 += 1

    print('%d of %d samples' % (np1, n_samples))
    print(proc.can_be)
    if do_part2:
      for can in proc.can_be:
        assert len(can) == 1

      proc.reg = [0] * 4
      for line in inp:
        l = line.strip()
        if l == '':
          continue
        if l[0].isdigit():
          op = [int(s) for s in l.split(' ')]
          real_op = proc.can_be[op[0]][0]
          proc.instruction(real_op, op[1], op[2], op[3])
      print('r0 == %d' % proc.reg[0])
