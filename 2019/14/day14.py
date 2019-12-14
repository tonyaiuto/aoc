#!/usr/bin/env python3

import re
import sys
import textwrap

QUANT_CHEM_RE = re.compile(r'(\d+) *([A-Za-z]+)')


class NanoFactory(object):

  def __init__(self, reactions=None, path=None):
    if path:
      with open(path, 'r') as inp:
        reactions = inp.read()
    self._parse(textwrap.dedent(reactions))

  def _parse(self, s):
    for line in s.strip().split('\n'):
      for tok in self.tokenize(line):
        print(str(tok))
 

  @staticmethod
  def tokenize(line):
    while line:
      if line[0] == ' ':
        line = line[1:]
        continue
      if line[0] == '\n':
        line = line[1:]
        yield '\n'
        continue
      elif line[0:2] == '=>':
        line = line[2:]
        yield '=>'
        continue
      elif line[0] == ',':
        line = line[1:]
        yield ','
        continue
  
      m = QUANT_CHEM_RE.match(line)
      if m:
        quantity = int(m.group(1))
        chem = m.group(2)
        line = line[len(m.group(0)):]
        yield (chem, quantity)
        continue
      else:
        line = line[1:]
        yield 'WTF'


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

