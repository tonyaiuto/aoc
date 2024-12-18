#!/usr/bin/env python3
"""AOC 2024: day 17"""

import sys

def read_input(path):
  with open(path, 'r') as inp:
    regs = {}
    for line in inp:
      if line.startswith("Register"):
        reg = line[9]
        val = int(line[12:])
        regs[reg] = val
      if line.startswith("Program"):
        prog = [int(op) for op in line[9:].split(',')]
  return regs, prog



def do_gen(regs, prog, expect=None):
  print("""#!/usr/bin/env python3

import sys

HALT = 0
OUT_FAIL = 1

class ChronospatialSolver(object):

  def __init__(self):
    self.prog = %s
    self.reset()

  def reset(self):
    self.outbuf = []
""" % prog)
  for k, v in regs.items():
    print("    self.%s=%d" % (k, v))

  print("""

  def do_out(self, out):
    self.outbuf.append(out)
    if self.outbuf != self.prog[0:len(self.outbuf)]:
      return False
    return True

  def proc(self):
    pc = 0
    while True:
     if pc >= %d:
       return HALT
""" % len(prog))

  emit_code(prog)
 
  print("""
  def search(self):
    for i in range(1000000):
      self.reset()
      self.A = i
      self.try_a()

  def try_a(self):
    start = self.A
    if self.A % 10000 == 0:
      print("Trying at A=%d" % self.A)
    res = self.proc()
    if res == OUT_FAIL and len(self.outbuf) > 2:
      print('%10d %12o %8x' % (start, start, start), '=>', self.outbuf)
    if res == HALT:
      print(start, '=>', self.outbuf)
      if self.outbuf == self.prog:
        print("Win at %d" %  i)
        sys.exit(0)


if __name__ == '__main__':
  solver = ChronospatialSolver()
  solver.search()
""")


def emit_code(prog):
  # find all jump targets
  jump_targets = set()
  for pc in range(0, len(prog), 2):
     op = prog[pc]
     if op == 3:
       jump_targets.add(prog[pc+1])

  pc_incr = 2
  for pc in range(0, len(prog), 2):
     if pc in jump_targets:
       print(indent(1), "if pc == %d:" % pc)
     op = prog[pc]
     lit = prog[pc+1]

     if op == 0:
       print(indent(2), "self.A = self.A // (2 ** %s)" % decode_combo(lit))
     elif op == 1:
       print(indent(2), "self.B = self.B ^ %s" % lit)
     elif op == 2:
       print(indent(2), "self.B = %s %% 8" % decode_combo(lit))
     elif op == 3:
       print(indent(2), "if self.A != 0:")
       print(indent(2), "  pc = %s" % lit)
       print(indent(2), "  continue")

     elif op == 4:
       print(indent(2), "self.B = self.B ^ self.C")

     elif op == 5:
       print(indent(2), "if not self.do_out(%s %% 8):" % decode_combo(lit))
       print(indent(2), "  return OUT_FAIL")

     elif op == 6:
       print(indent(2), "self.B = self.A // (2 ** %s)" % decode_combo(lit))
     elif op == 7:
       print(indent(2), "self.C = self.A // (2 ** %s)" % decode_combo(lit))

     # program counter update
     if (pc + 2) not in jump_targets:
       pc_incr += 2
     else:
       print(indent(2), "pc += %d" % pc_incr)
       pc_incr = 0

  # and after the last block
  print(indent(2), "pc += %d" % (pc_incr-2))


def decode_combo(combo):
  if combo <= 3:
    return str(combo)
  if combo == 4:
    return 'self.A'
  if combo == 5:
    return 'self.B'
  if combo == 6:
    return 'self.C'
  if combo == 7:
    return -1


def indent(n):
  return '  ' * (n + 1)


if __name__ == '__main__':
  if len(sys.argv) > 1:
    prog = sys.argv[1]
  else:
    prog = 'input.txt'
  expect = None
  if len(sys.argv) > 2:
    expect = sys.argv[2]
  regs, prog = read_input(prog)
  do_gen(regs, prog, expect)

