#!/usr/bin/env python3

from collections import defaultdict
import re
import sys
import textwrap

QUANT_CHEM_RE = re.compile(r'(\d+) *([A-Za-z]+)')



class Node(object):

  def __init__(self):
    self.inputs = []
    self.out_chem = None
    self.out_quant = 0

  def __str__(self):
    input = ', '.join(['%d %s' % (q, c) for (q,c) in self.inputs])
    return '%s => %d %s' % (input, self.out_quant, self.out_chem)

  @staticmethod
  def fromText(text):
    node = Node()
    state_inputs = True
    for tok in Node.tokenize(text):
      if tok == '=>':
        state_inputs = False
      elif state_inputs:
        node.inputs.append(tok)
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
        yield '<UNKNOWN TOKEN: %s>' % c


def P(dict):
  return ','.join(['%s:%d' % (chem, quant)for chem,quant in sorted(dict.items())])

class NanoFactory(object):

  def __init__(self, reactions=None, path=None):
    if path:
      with open(path, 'r') as inp:
        reactions = inp.read()
    self.to_get = {}
    self.nodes = []
    self.trace = False
    self._parse(textwrap.dedent(reactions))

  def _parse(self, s):
    for line in s.strip().split('\n'):
      node = Node.fromText(line)
      self.nodes.append(node)
      # print(node)
      if node.out_chem in self.to_get:
        raise Exception(
            '%s is yielded two ways. Violates premise' % node.out_chem)
      self.to_get[node.out_chem] = node

  def make(self, t_need, t_chem, state, g_need):
    target_node = self.to_get[t_chem]
    if state[t_chem] >= t_need:
      # state[t_chem] -= t_need
      return state

    # How many times do we have to run the reaction.
    # t_need -= state[t_chem]  # actual need
    n_times = (t_need + target_node.out_quant - 1) // target_node.out_quant

    for (need, chem) in target_node.inputs:
      need = need * n_times
      g_need[chem] += need
      if self.trace:
        print('need %5d of %-8.8s: %s' % (need, chem, P(state)))
      if chem == 'ORE':
        state['ORE'] += need
      else:
        self.make(need-state[chem], chem, state=state, g_need=g_need)
        if state[chem] < need:
          print('WTF?', chem, 'need:', need, str(target_node), P(state))
        state[chem] -= need
    state[t_chem] += target_node.out_quant * n_times

  def min_ore(self):
    state = defaultdict(int)
    need = defaultdict(int)
    self.make(1, 'FUEL', state, need)
    print('min_or: Need %d %d ORE' % (state['ORE'], need['ORE']))

    need_ore = 0
    for node in self.nodes:
      for (i_need, i_chem) in node.inputs:
        if i_chem == 'ORE':
          # How much do we need of this precursor
          t_need = need[node.out_chem]
          n_times = (t_need + node.out_quant - 1) // node.out_quant
          need_ore += i_need * n_times
    print('need_ore:', need_ore)
    return min(need_ore, state['ORE'])


def test_part1():
  nf = NanoFactory(reactions="""\
      10 ORE => 10 A
      1 ORE => 1 B
      7 A, 1 B => 1 C
      7 A, 1 C => 1 D
      7 A, 1 D => 1 E
      7 A, 1 E => 1 FUEL
      """)
  assert 6 == len(nf.to_get)
  min_ore = nf.min_ore()
  assert 31 == min_ore

  nf = NanoFactory(reactions="""\
      9 ORE => 2 A
      8 ORE => 3 B
      7 ORE => 5 C
      3 A, 4 B => 1 AB
      5 B, 7 C => 1 BC
      4 C, 1 A => 1 CA
      2 AB, 3 BC, 4 CA => 1 FUEL
      """)
  assert 7 == len(nf.to_get)
  min_ore = nf.min_ore()
  assert 165 == min_ore


  nf = NanoFactory(reactions="""\
      2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
      17 NVRVD, 3 JNWZP => 8 VPVL
      53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
      22 VJHF, 37 MNCFX => 5 FWMGM
      139 ORE => 4 NVRVD
      144 ORE => 7 JNWZP
      5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
      5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
      145 ORE => 6 MNCFX
      1 NVRVD => 8 CXFTF
      1 VJHF, 6 MNCFX => 4 RFSQX
      176 ORE => 6 VJHF
      """)
  min_ore = nf.min_ore()
  assert 180697 == min_ore

  nf = NanoFactory(reactions="""\
      171 ORE => 8 CNZTR
      114 ORE => 4 BHXH
      189 ORE => 9 KTJDG
      121 ORE => 7 VRPVC
      12 VRPVC, 27 CNZTR => 2 XDBXC
      15 KTJDG, 12 BHXH => 5 XCVML
      3 BHXH, 2 VRPVC => 7 MZWV
      5 BHXH, 4 VRPVC => 5 LTCX
      6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
      14 VRPVC => 6 BMBT
      15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
      1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
      7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
      7 XCVML => 6 RJRHP
      13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
      5 BMBT => 4 WPTQ
      6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
      """)
  # nf.trace = True
  min_ore = nf.min_ore()
  assert 2210736 == min_ore


def part1():
  nf = NanoFactory(path='input_14.txt')
  min_ore = nf.min_ore()
  print('part1: Need %d ORE' % min_ore)
  #  445745 445745 is too low
  # need_ore: 445869 still wrong
  assert 445745 < min_ore


if __name__ == '__main__':
  test_part1()
  # part1()

