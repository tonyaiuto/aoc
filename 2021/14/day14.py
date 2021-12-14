#!/usr/bin/env python3
"AOC 2021: day 14"

from collections import defaultdict
import itertools

from tools import aoc

def pairwise(s):
  prev = None
  for c in s:
    if prev is not None:
      yield prev + c
    prev = c


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



class day14(aoc.aoc):

  def __init__(self):
    super(day14, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    pass

  def post_load(self):
    # called after all input is read

    self.template = self.all_input[0]
    self.rules = {}
    for line in self.all_input[1:]:
      if not line:
        continue
      f, _, t = line.split(' ')
      if self.trace_sample:
        print(f, '==>', t)
      self.rules[f] = t


  def part1(self):
    print('===== Start part 1')
    self.reset()

    x = self.template
    for i in range(10):
      x = self.do_gen(x)

    # print(x)
    print('expect 3073', len(x))
    counts = defaultdict(int)
    for c in x:
      counts[c] += 1
    tmp = []
    foo = sorted(counts.values())
    return foo[-1] - foo[0]

  def do_gen(self, polymer):
    print('Doing', polymer)
    prev = polymer[0]
    out = []
    for c in polymer[1:]:
      pair = prev + c
      out.append(prev)
      prev = c
      rep = self.rules.get(pair)
      if rep:
        if self.trace_sample:
          print('   ', pair, '->', rep)
        out.append(rep)
      else:
        if self.trace_sample:
          print('   ', pair, 'not found')
    out.append(prev)
    return ''.join(out)

  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.cycles = {}

    counts = defaultdict(int)
    for c in self.template:
      counts[c] += 1
    foo = sorted(counts.values())
   
    x = self.template
    for i in range(3):
      x = self.do_gen(x)

    for r in self.rules:
      self.find_cycle(r)

    return 42

  def find_cycle(self, r):
    orig = r
    tmp = r
    loop_c = r[1]
    print('Finding cycle in', r, '->', self.rules[r])
    limit = len(self.rules)
    for l in range(limit+1):
      rep = self.rules[r]
      r = r[0] + rep
      tmp = r + tmp[1:]
      if rep == loop_c:
        break
    if rep != loop_c:
      print(' => NO LOOP')
      return None
    print(' =>', tmp, l + 1)
    self.cycles[orig] = l + 1


day14.sample_test("""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""", expect1=1588, expect2=None)


if __name__ == '__main__':
  # day14.run_and_check('input.txt', expect1=None, expect2=None)
  pass
