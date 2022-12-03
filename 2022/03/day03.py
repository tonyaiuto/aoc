#!/usr/bin/env python3
"AOC 2021: day 03"

from collections import defaultdict

from tools import aoc

def priority(c):
  ascii = ord(c)
  if ord('a') <= ascii and ascii <= ord('z'):
    return ascii - ord('a') + 1
  if ord('A') <= ascii and ascii <= ord('Z'):
    return ascii - ord('A') + 27
  assert c == ascii


class day03(aoc.aoc):

  def __init__(self):
    super(day03, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.sum = 0
    self.dups = set()
    self.line = 0

  def do_line(self, line):
    # called for each line of input
    # line = line.strip()
    l = len(line) // 2
    left = line[0:l]
    right = line[l:]
    assert len(left) == len(right)
    left_c = set([c for c in line[0:l]])
    for c in right:
      if c in left_c:
        # I wasted too much time counting them only once.
        # I misinterpted the requirements and didn't step out of the box
        #if c in self.dups:
        #   # print('  skip', c)
        #   # return
        #   #continue
        #   pass

        p = priority(c)
        self.dprint('add dup', c, p)
        self.sum += p
        self.dups.add(c)
        return

  def part1(self):
    print('===== Start part 1')
    self.reset()
    return self.sum

  def part2(self):
    print('===== Start part 2')
    self.reset()
    sum = 0
    for lno in  range(0, len(self.all_input), 3):
      group = [self.all_input[lno], self.all_input[lno+1], self.all_input[lno+2]]
      c = do_group(group)
      sum += priority(c)
    return sum

def do_group(group):
  f = defaultdict(int)
  for sack in group:
    for i in set([i for i in sack]):
      f[i] += 1
  for c, count in f.items():
    if count == 3:
      # print('got', c)
      return c
  print('nothing is used 3 times', f)
  assert False


day03.sample_test("""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""", expect1=157, expect2=70)


if __name__ == '__main__':
  day03.run_and_check('input.txt', expect1=7746, expect2=2604)
