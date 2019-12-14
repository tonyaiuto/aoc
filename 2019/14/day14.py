#!/usr/bin/env python3

import re
import sys
import textwrap

QUANT_CHEM_RE = re.compile(r'(\d+) *([A-Za-z]+)')


class Node(object):

  def __init__(self):
    self.chems = []
    self.quants = []
    self.out_chem = None
    self.out_quant = 0

  def __str__(self):
    input = ', '.join(['%d %s' % (x[0], x[1])
                      for x in zip(self.quants, self.chems)])
    return '%s => %d %s' % (input, self.out_quant, self.out_chem)

  @staticmethod
  def fromText(text):
    node = Node()
    state_inputs = True
    for tok in Node.tokenize(text):
      # print(str(tok))
      if tok == '=>':
        state_inputs = False
      elif state_inputs:
        node.quants.append(tok[0])
        node.chems.append(tok[1])
      else:
        node.out_quant = tok[0]
        node.out_chem = tok[1]
    return node

  @staticmethod
  def tokenize(line):
    while line:
      c = line[0]
      if c == ' ' or c == ',':
        line = line[1:]
        continue
      elif line[0:2] == '=>':
        line = line[2:]
        yield '=>'
        continue
  
      m = QUANT_CHEM_RE.match(line)
      if m:
        quantity = int(m.group(1))
        chem = m.group(2)
        line = line[len(m.group(0)):]
        yield (quantity, chem)
        continue
      else:
        line = line[1:]
        yield 'WTF'



class NanoFactory(object):

  def __init__(self, reactions=None, path=None):
    if path:
      with open(path, 'r') as inp:
        reactions = inp.read()
    self._parse(textwrap.dedent(reactions))

  def _parse(self, s):
    for line in s.strip().split('\n'):
      n = Node.fromText(line)
      print(n)



def test_part1():
  nf = NanoFactory("""\
      10 ORE => 10 A
      1 ORE => 1 B
      7 A, 1 B => 1 C
      7 A, 1 C => 1 D
      7 A, 1 D => 1 E
      7 A, 1 E => 1 FUEL
      """)


if __name__ == '__main__':
  test_part1()

