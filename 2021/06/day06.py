"AOC 2021: day 06"

from collections import defaultdict
import math

from tools import aoc


class day06(aoc.aoc):

  def __init__(self):
    super(day06, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    self.state = [int(v) for v in self.all_input[0].split(',')]
    if self.trace_sample:
      print(self.state)
    self.nfish = len(self.state)
    self.ages = defaultdict(int)
    for x in self.state:
      self.ages[x] += 1

  def gen1(self):
    nxt = []
    for fi in range(len(self.state)):
      left = self.state[fi]
      if left > 0:
        self.state[fi] = left - 1
      else:
        self.state[fi] = 6
        nxt.append(8)
    self.state.extend(nxt)

  def part1(self):
    # print('===== Start part 1')
    for i in range(80):
      self.gen1()
      if self.trace_sample and i < 19:
        print(self.state)
    return len(self.state)

  def part1_fast(self):
    for i in range(80):
      self.gen2()
    return self.nfish

  def gen2(self):
    cur = self.ages
    self.ages = defaultdict(int)
    for age in cur.keys():
      count = cur[age]
      if age == 0:
        self.ages[8] = count
        self.ages[6] += count
        self.nfish += count
      else:
        self.ages[age-1] += count

  def part2(self):
    # print('===== Start part 2')
    for i in range(256):
      self.gen2()
    return self.nfish


day06.sample_test("""
3,4,3,1,2
""", expect1=5934, expect2=26984457539)


if __name__ == '__main__':
  day06.run_and_check('input.txt', expect1=389726, expect2=1743335992042)
  day06.do(day06.part1_fast, 'input.txt', expect=389726)
