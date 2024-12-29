#!/usr/bin/env python3
"AOC 2023: day 24"

from collections import defaultdict
import operator
import sys

from tools import aoc


class Gate(object):

  def __init__(self, parts):
    self.a = parts[0]
    self.b = parts[2]
    self.out = parts[4]
    if parts[1] == 'AND':
      self.op = operator.and_
      self.opname = 'and'
    elif parts[1] == 'OR':
      self.op = operator.or_
      self.opname = 'or'
    elif parts[1] == 'XOR':
      self.op = operator.xor
      self.opname = 'xor'
    else:
      print('bad op', parts[1])
      sys.exit(1)

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str('%s %s %s -> %s' % (self.a, self.b, self.opname, self.out))

  def do_op(self, a, b):
    return self.op(a, b)


class day24(aoc.aoc):

  def __init__(self):
    super(day24, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.initial = {}
    self.gates = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    if not line:
      return
    parts = line.split(' ')
    if parts[0][-1] == ':':
      self.initial[parts[0][0:-1]] = int(parts[1])
      return
    gate = Gate(parts)
    self.gates.append(gate)

  def post_load(self):
    # called after all input is read
    print(self.initial)
    self.wires = dict(self.initial)
    print(self.gates)

  def gate_ready(self, gate):
    return gate.a in self.wires and gate.b in self.wires

  def gate_do(self, gate):
    return gate.do_op(self.wires[gate.a], self.wires[gate.b])

  def eval(self):
    unready = self.gates
    while len(unready) > 0:
      print('len unready', len(unready))
      unready = self.do_ready(unready)

  def do_ready(self, possibly_ready):
    unready = []
    for gate in possibly_ready:
      a = self.wires.get(gate.a, -1)
      if a >= 0:
        b = self.wires.get(gate.b, -1)
        if b >= 0:
          assert gate.out not in self.wires
          self.wires[gate.out] = gate.do_op(a, b)
          continue
      unready.append(gate)
    return unready

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.eval()
    ret = 0
    for wire, value in self.wires.items():
      if wire[0] == 'z':
        bit = int(wire[1:]) 
        if value:
          ret |= 1 << bit
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day24.sample_test("""
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""", expect1=2024, expect2=None)


if __name__ == '__main__':
  day24.run_and_check('input.txt', expect1=42049478636360, expect2=None)
