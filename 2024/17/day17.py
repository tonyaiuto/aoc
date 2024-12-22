#!/usr/bin/env python3
"AOC 2023: day 17"

from collections import defaultdict
import copy

from tools import aoc
from tools import gridutils
from tools import intcode

class Op(object):
  def __init__(self, name, do):
    self.name = name
    self.do = do


def do_jnz(comp, literal, combo):
  if comp.reg('A') == 0:
    return
  comp.pc = literal


def do_output(comp, literal, combo):
  comp.save_output(combo % 8)
  if comp.in_part2:
    if comp.out_buf != comp.mem[0:len(comp.out_buf)]:
      comp.out_fail = True


class Chronospatial(intcode.Intcode):

  def __init__(self, **kwargs):
    super(Chronospatial, self).__init__(
      registers=('A', 'B', 'C'),
      **kwargs
    )
    self.ops = [
      Op('adv',
         lambda comp, literal, combo: comp.reg_set('A', comp.reg('A') // (2 ** combo))
      ),
      Op('bxl',
         lambda comp, literal, combo: comp.reg_set('B', comp.reg('B') ^ literal)
      ),
      Op('bst',
         lambda comp, literal, combo: comp.reg_set('B', combo % 8)
      ),
      Op('jnz', do_jnz),
      Op('bxc',
         lambda comp, literal, combo: comp.reg_set('B', comp.reg('B') ^ comp.reg('C'))
      ),
      Op('out', do_output),
      Op('bdv',
         lambda comp, literal, combo: comp.reg_set('B', comp.reg('A') // (2 ** combo))
      ),
      Op('cdv',
         lambda comp, literal, combo: comp.reg_set('C', comp.reg('A') // (2 ** combo))
      ),
    ]

  def __repr__(self):
    return str(self)

  def __str__(self):
    return str(self.__dict__)

  def step(self, op, verbose=False):
    self.pc += 1
    literal_arg = self.mem_at("pc")
    self.pc += 1
    combo_arg = self.decode_combo(literal_arg)
    opcode = self.ops[op]
    opcode.do(self, literal_arg, combo_arg)
    if verbose:
      print(
          '%s(%d)' % (opcode.name, op), 'lit:%d, combo:%d' % (literal_arg, combo_arg),
          'regs', self.reg('A'), self.reg('B'), self.reg('C')
      )

  def decode_combo(self, combo):
    if combo <= 3:
      return combo
    if combo == 4:
      return self.reg('A')
    if combo == 5:
      return self.reg('B')
    if combo == 6:
      return self.reg('C')
    if combo == 7:
      """
      print("Got combo 7")
      print("mem", self.mem)
      print("registers", self.registers)
      print("pc", self.pc)
      print("output", self.read_output())
      sys.exit(1)
      """
      return None

  def print(self):
    print(self.__dict__)


class day17(aoc.aoc):

  def __init__(self):
    super(day17, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.comp = Chronospatial()
    self.comp.in_part2 = False

  def reset(self):
    # for future use
    self.comp.registers = copy.copy(self.save_registers)
    self.comp.pc = 0
    self.comp.out_fail = False

  def do_line(self, line):
    # called for each line of input
    if line.startswith("Register"):
      reg = line[9]
      val = int(line[12:])
      self.comp.reg_set(reg, val)

    if line.startswith("Program"):
      for op in line[9:].split(','):
        self.comp.mem_append(int(op))

  def post_load(self):
    # called after all input is read
    self.comp.print()
    self.save_registers = copy.copy(self.comp.registers)


  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.comp.in_part2 = False

    while self.comp.pc < len(self.comp.mem):
      self.comp.step(self.comp.mem[self.comp.pc], verbose=self.doing_sample)
      if self.comp.reg('B') > 7:
        print("B went nuts", self.comp.reg('B'))
        return -1

    output = self.comp.read_output()
    print('OUTPUT', output)
    return ','.join([str(x) for x in output])

  def part2(self):
    print('===== Start part 2')
    self.comp.in_part2 = True

    start_a = 0
    while start_a < 200000:
      if start_a % 10000 == 0:
        print("== Part 2: A=%d" % start_a)
      self.reset()
      self.comp.reg_set('A', start_a)
      # self.comp.print()
      while self.comp.pc < len(self.comp.mem):
        self.comp.step(self.comp.mem[self.comp.pc])
        if self.comp.reg('B') > 7:
          print("B went nuts", self.comp.reg('B'))
          return -1
        if self.comp.out_fail:
          break
      output = self.comp.read_output()
      if len(output) == len(self.comp.mem):
        if output == self.comp.mem:
          return start_a
      start_a += 1
   
    return -1


day17.sample_test("""
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""", expect1='4,6,3,5,6,3,5,2,1,0')

day17.sample_test("""
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""", expect2=117440)


if __name__ == '__main__':
  day17.run_and_check('input.txt', expect1='3,1,5,3,7,4,2,7,5', expect2=None)
  pass
