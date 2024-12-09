#!/usr/bin/env python3
"AOC 2023: day 07"

from tools import aoc

class day07(aoc.aoc):

  def __init__(self):
    super(day07, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.res = []
    self.vals = []

  def do_line(self, line):
    # called for each line of input
    parts = line.split(':')
    self.res.append(int(parts[0]))
    self.vals.append([int(x) for x in parts[1].strip().split(' ')])

  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for i in range(len(self.res)):
      if got_match(vals=self.vals[i], target=self.res[i]):
        ret +=  self.res[i]
        # print('GOT', self.res[i])
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for i in range(len(self.res)):
      if got_match(vals=self.vals[i], target=self.res[i]):
        ret +=  self.res[i]
        # print('GOT', self.res[i])
      else:
        if got_match2(vals=self.vals[i], target=self.res[i]):
          # print('GOT 2', self.res[i])
          ret +=  self.res[i]
    return ret


def got_match(vals, target=None):
  cur = [vals[0]]
  more = vals[1:]
  while more:
    n_cur = []
    for v in cur:
      if v * more[0] <= target:
        n_cur.append(v * more[0])
      if v + more[0] <= target:
        n_cur.append(v + more[0])
    cur = n_cur
    more = more[1:]
    print
  # print('cur', cur)
  if target in cur:
    # print('GOT', target)
    return True
  return False

got_match([81, 40, 27], target=3267)
got_match([6, 8, 6, 15], target=7290)


def got_match2(vals, target=None):
  cur = [vals[0]]
  more = vals[1:]
  while more:
    n_cur = []
    for v in cur:
      next = more[0]
      if v * next <= target:
        n_cur.append(v * next)
      if v + next <= target:
        n_cur.append(v + next)
      vv = int('%d%d' % (v, next))
      if vv <= target:
        n_cur.append(vv)
    cur = n_cur
    more = more[1:]
    print
  # print('cur', cur)
  if target in cur:
    # print('GOT', target)
    return True
  return False


day07.sample_test("""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""", expect1=3749, expect2=11387)


if __name__ == '__main__':
  day07.run_and_check('input.txt', expect1=14711933466277, expect2=286580387663654)
