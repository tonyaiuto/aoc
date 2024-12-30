#!/usr/bin/env python3
"AOC 2023: day 24"

from collections import defaultdict
import operator
import sys

from tools import aoc


class Gate(object):

  def __init__(self, parts):
    self.a = min(parts[0], parts[2])
    self.b = max(parts[0], parts[2])
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
    self.x = []
    self.y = []
    self.gates = []
    self.max_z = -1

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    if not line:
      return
    parts = line.split(' ')
    if parts[0][-1] == ':':
      name = parts[0][0:-1]
      value = int(parts[1])
      self.initial[name] = value
      n = int(name[1:])
      if parts[0][0] == 'x':
        assert len(self.x) == n
        self.x.append(value)
        self.max_x = n
      if parts[0][0] == 'y':
        assert len(self.y) == n
        self.y.append(value)
        self.max_y = n
      return
    gate = Gate(parts)
    if gate.out[0] == 'z':
      self.max_z = max(self.max_z, int(gate.out[1:]))
    self.gates.append(gate)

  def post_load(self):
    # called after all input is read
    self.wires = dict(self.initial)
    #if self.doing_sample:
    #  print(self.initial)
    #  print(self.gates)
    print(self.max_z)

  def gate_ready(self, gate):
    return gate.a in self.wires and gate.b in self.wires

  def gate_do(self, gate):
    return gate.do_op(self.wires[gate.a], self.wires[gate.b])

  def eval(self):
    unready = self.gates
    while len(unready) > 0:
      # print('len unready', len(unready))
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
    return self.get_z()

  def get_z(self):
    ret = 0
    for wire, value in self.wires.items():
      if wire[0] == 'z':
        bit = int(wire[1:]) 
        if value:
          ret |= 1 << bit
    return ret

  def to_wires(self, prefix, n):
    for bit in range(self.max_x+1):
      self.wires['%s%02d' % (prefix, bit)] = n & 1
      n >>= 1

  def part2(self):
    if self.doing_sample:
      return None
    print('===== Start part 2')
    self.reset()
    # My input has 222 gates and 45 bit inputs
    # A half adder needs 1 XOR, 1 AND
    # A full adder needs 2 XOR, 2 AND, 1 OR
    # Coincidence? 44 * 5 + 2 == 222
    # Lets verify.
    n_gates = defaultdict(int)
    for g in self.gates:
      n_gates[g.opname] += 1
    print(n_gates)
    if len(self.gates) > 50:
      assert n_gates['and'] == 44 * 2 + 1
      assert n_gates['xor'] == 44 * 2 + 1
      assert n_gates['or'] == 44

    self.build_connections_to_gates()
    self.good_gates = set()
    self.bad_gates = set()
    self.check_sum_gates()
    assert len(self.sum_gates) == self.max_z + 1

    self.check_carry_inputs()
    # self.verify_half_adder(bit=0)
    #for bit in range(1, 4):
    #  self.verify_full_adder(bit=bit)
    return 42

  def check_carry_inputs(self):
    # Carry input 3 is the carry output of bit 2 full adder
    for bit, gate in self.carry_input.items():
      assert bit > 0
      if bit == 1:
        if gate.opname != 'and':
          print("Wrong gate type for carry out bit", bit, gate)
          self.bad_gates.add(gate)

        if self.check_inputs_for_xy(gate, bit=0, op_type='and', msg="carry-in"):
          self.good_gates.add(gate)
        continue

      if gate.opname != 'or':
        print("Wrong gate type for carry out bit", bit, gate)
        self.bad_gates.add(gate)
        continue
      in_a = self.output_to_gate[gate.a]
      in_b = self.output_to_gate[gate.b]
      if in_a.opname != 'and':
        print("Bad gate type for carryout input.", bit, in_a)
        self.bad_gates.add(in_a)
      if in_b.opname != 'and':
        print("Bad gate type for carryout input.", bit, in_b)
        self.bad_gates.add(in_b)

      # self.check_inputs_for_xy(gate, bit, op_type='or', msg="sum gate xor inputs1")

  def check_sum_gates(self):
    self.sum_gates = {}
    self.carry_input = {}
    for gate in self.gates:
      if gate.out[0] != 'z':
        continue
      bit = int(gate.out[1:])
      # print("sum gate", bit, gate)
      self.sum_gates[bit] = gate
   
      if gate.opname != 'xor':
        print("Wrong gate type for sum gate bit", bit, gate)
        self.bad_gates.add(gate)
        continue
      if bit == 0:
        if gate.a != 'x00' or gate.b != 'y00':
          print("Wrong inputs for sum gate bit 0", gate.a, gate.b)
          self.bad_gates.add(gate)
        else:
          self.good_gates.add(gate)
        continue

      # other bits are full adders: (a ^ b) ^ carry_in => sum
      in_a = self.output_to_gate[gate.a]
      in_b = self.output_to_gate[gate.b]
      if in_a.opname == 'xor':
        if self.check_inputs_for_xy(in_a, bit, op_type='xor', msg="sum gate xor inputs"):
          self.carry_input[bit] = in_b
      else:
        if self.check_inputs_for_xy(in_b, bit, op_type='xor', msg="sum gate xor inputs"):
          self.carry_input[bit] = in_a

  def check_inputs_for_xy(self, gate, bit, op_type, msg='gate'):  
    if gate.opname != op_type:
      print("Wrong gate type (got:%s, expect:%s)" % (gate.opname, op_type),
            "for", msg, 'bit', bit, gate)
      self.bad_gates.add(gate)
      return False
    xname = 'x%02d' % bit
    yname = 'y%02d' % bit
    if gate.a != xname or gate.b != yname:
      print("Wrong base inputs for", msg, 'bit', bit, gate)
      self.bad_gates.add(gate)
      return False
    self.good_gates.add(self)
    return True

  def build_connections_to_gates(self):
    self.input_to_gates = defaultdict(set)
    self.output_to_gate = {}
    for gate in self.gates:
      self.input_to_gates[gate.a].add(gate)
      self.input_to_gates[gate.b].add(gate)
      assert gate.out not in self.output_to_gate
      self.output_to_gate[gate.out] = gate

  def input_to_gate_type(self, name, type):
    ret = None
    for gate in self.input_to_gates[name]:
      if gate.opname == type:
        assert not ret
        ret = gate
    return ret
    
  def verify_half_adder(self, bit):
    x = 'x%02d' % bit
    y = 'y%02d' % bit
    gx = self.input_to_gate_type(x, 'xor')
    gy = self.input_to_gate_type(y, 'xor')
    if gx != gy:
      print("Inputs to adder %d xor are incorrect. Expect %s/%s got" % (x, y),
            gx.a, gx.b, gy.a, gy.b)
      return False
    if gx.out != 'z%02d' % bit:
      print("Output to adder %d xor are incorrect. Expect %s, got %s" % (bit, gx.out))
      return False
    gx = self.input_to_gate_type(x, 'and')
    gy = self.input_to_gate_type(y, 'and')
    if gx != gy:
      print("Inputs to adder %d and are incorrect. Expect %s/%s got" % (x, y),
            gx.a, gx.b, gy.a, gy.b)
      return False
    return True

  def verify_full_adder(self, bit):
    x = 'x%02d' % bit
    y = 'y%02d' % bit
    gx = self.input_to_gate_type(x, 'xor')
    gy = self.input_to_gate_type(y, 'xor')
    if gx != gy:
      print("Inputs to adder %d xor are incorrect. Expect %s/%s got" % (x, y),
            gx.a, gx.b, gy.a, gy.b)
      return False
    if gx.out != 'z%02d' % bit:
      print("Output to adder %d xor are incorrect. Expect %s, got %s" % (bit, gx.out))
      return False
      
    gx = self.input_to_gate_type(x, 'and')
    gy = self.input_to_gate_type(y, 'and')
    if gx != gy:
      print("Inputs to adder %d and are incorrect. Expect %s/%s got" % (x, y),
            gx.a, gx.b, gy.a, gy.b)
      return False
    return True


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
