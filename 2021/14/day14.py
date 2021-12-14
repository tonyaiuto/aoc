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

  def post_load(self):
    self.template = self.all_input[0]
    self.rules = {}
    for line in self.all_input[1:]:
      if not line:
        continue
      f, _, t = line.split(' ')
      self.rules[f] = t

  def part1(self):
    print('===== Start part 1')
    self.reset()

    x = self.template
    for i in range(10):
      if self.trace_sample and i < 5:
        print('Doing', x)
      x = self.do_gen(x)

    counts = defaultdict(int)
    for c in x:
      counts[c] += 1
    tmp = []
    foo = sorted(counts.values())
    print('Counts', foo)
    return foo[-1] - foo[0]

  def do_gen(self, polymer):
    prev = polymer[0]
    out = []
    for c in polymer[1:]:
      pair = prev + c
      out.append(prev)
      prev = c
      rep = self.rules.get(pair)
      if rep:
        out.append(rep)
    out.append(prev)
    return ''.join(out)


  def part2(self):
    print('===== Start part 2')

    self.letters = defaultdict(int)
    for c in self.template:
      self.letters[c] += 1

    pair_counts = defaultdict(int)
    for pair in pairwise(self.template):
      pair_counts[pair] += 1
    if self.trace_sample:
      print(pair_counts)
    for i in range(40):
      pair_counts = self.do_gen2(pair_counts)
      if self.trace_sample and i < 5:
        print(pair_counts)
        print(', '.join(['%s:%d' % (k, self.letters[k]) for k in sorted(self.letters)]))

    foo = sorted(self.letters.values())
    print('Counts', foo)
    return foo[-1] - foo[0]

  def do_gen2(self, pair_counts):

    ret = defaultdict(int)
    for pair, count in pair_counts.items():
      rep = self.rules[pair]
      self.letters[rep] += count
      ret[pair[0] + rep] += count
      ret[rep + pair[1]] += count
    return ret


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
""", expect1=1588, expect2=2188189693529)


if __name__ == '__main__':
  day14.run_and_check('input.txt', expect1=3697, expect2=4371307836157)
