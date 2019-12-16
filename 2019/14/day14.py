#!/usr/bin/env python3

import re
import textwrap

QUANT_CHEM_RE = re.compile(r'(\d+) *([A-Za-z]+)')


class Node(object):

  def __init__(self):
    self.name = None
    self.out_quant = 0
    self.inputs = []
    self.made = 0  # total made
    self.used = 0  # total used

  def __str__(self):
    input = ', '.join(['%d %s' % (q, c) for (q,c) in self.inputs])
    return '%s => %d %s (made:%d, used:%d)' % (
        input, self.out_quant, self.name, self.made, self.used)

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
        node.name = tok[1]
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
    self.by_name = {}
    self.trace = False
    self._parse(textwrap.dedent(reactions))

    # ORE is never a right hand side, so manifest it from nothing
    self.ore = Node()
    self.ore.name = 'ORE'
    self.ore.out_quant = 1
    self.by_name['ORE'] = self.ore

  def reset(self):
    for node in self.by_name.values():
      node.made = 0
      node.used = 0

  def _parse(self, s):
    for line in s.strip().split('\n'):
      node = Node.fromText(line)
      # print(node)
      if node.name in self.by_name:
        raise Exception(
            '%s is yielded two ways. Violates premise' % node.name)
      self.by_name[node.name] = node

  def ensure(self, t_need, t_chem):
    target_node = self.by_name[t_chem]

    # reduce need by what we have on hand
    on_hand = target_node.made - target_node.used
    if on_hand > 0:
      use = min(t_need, on_hand)
      t_need -= use
    if self.trace:
      print('Have %d leftover %s on hand. Making %d' % (
          on_hand, t_chem, t_need))

    # How many times do we have to run the reaction.
    n_times = (t_need + target_node.out_quant - 1) // target_node.out_quant

    for (need, chem) in target_node.inputs:
      input_node = self.by_name[chem]
      need = need * n_times  # number needed for output required
      if self.trace:
        print('need %5d of %-8.8s: %s' % (need, chem, P(state)))
      self.ensure(need, chem)
      input_node.used += need
    t_need -= target_node.out_quant * n_times
    target_node.made += target_node.out_quant * n_times


  def min_ore(self, target=1):
    self.ensure(target, 'FUEL')
    # print('min ore NODE:', str(self.ore))
    return self.ore.used

  def max_fuel(self, limit=1000000000000):
    self.reset()
    min_ore = self.min_ore(target=1)
    target = limit // min_ore
    print('Start max for %d / 1 at %d' % (min_ore, target))
    last_good = 1
    increment = 1024 * 1024
    max_f = 0
    while True:
      self.reset()
      min_ore = self.min_ore(target=target)
      # print('Made %d with %13d ORE' % (target, min_ore))
      if min_ore < limit:
        last_good = target
        max_f = max(max_f, target)
        target += increment
      elif min_ore > limit:
        target = last_good
        if increment == 1:
          break
        increment = increment // 2
      elif min_ore == limit:
        max_f = max(max_f, target)
        break
    return max_f


def test_min_ore():
  nf = NanoFactory(reactions="""\
      10 ORE => 10 A
      1 ORE => 1 B
      7 A, 1 B => 1 C
      7 A, 1 C => 1 D
      7 A, 1 D => 1 E
      7 A, 1 E => 1 FUEL
      """)
  assert 7 == len(nf.by_name)
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
  assert 8 == len(nf.by_name)
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
  min_ore = nf.min_ore()
  assert 2210736 == min_ore


def test_max_fuel():
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
  max_fuel = nf.max_fuel()
  assert 5586022 == max_fuel


def part1():
  nf = NanoFactory(path='input_14.txt')
  min_ore = nf.min_ore()
  print('part1: Need %d ORE' % min_ore)
  #  445745 445745 is too low
  # need_ore: 445869 still wrong
  assert 445745 < min_ore
  assert 469536 == min_ore


def part2():
  nf = NanoFactory(path='input_14.txt')
  max_fuel = nf.max_fuel()
  print('part2: max_fuel:', max_fuel)
  assert 3343477 == max_fuel


if __name__ == '__main__':
  test_min_ore()
  # part1()
  test_max_fuel()
  part2()
