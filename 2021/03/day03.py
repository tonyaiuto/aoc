"AOC 2021: day 03"

from collections import defaultdict
import math

from tools import aoc


class Foo(object):

  def __init__(self):
    pass

  def __str__(self):
    return str(self)



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
    self.counts = defaultdict(int)
    self.samples = 0
    self.width = 0
    self.all = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.all.append(line)
    self.samples += 1
    if len(line) > self.width:
      self.width = len(line)
    for i in range(len(line)):
      bit = line[i]
      if bit == '1':
        self.counts[i] += 1

  def post_load(self):
    # called after all input is read
    print(self.samples, 'samples')
    print(self.counts)
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    gamma = 0
    epsilon = 0
    half = (self.samples + 1) // 2
    for i in range(self.width):
      gamma <<= 1
      epsilon <<= 1
      if self.counts[i] >= half:
        gamma |= 1
      else:
        epsilon |= 1
    # print(gamma)
    return gamma * epsilon


  def part2(self):
    print('===== Start part 2')
    self.reset()

    cleft = self.all

    oleft = self.all
    cleft = self.all
    for i in range(self.width):
      ones = 0
      onext = []
      znext = []
      for val in oleft:
        if val[i] == '1':
          ones += 1
          onext.append(val)
        else:
          znext.append(val)
      half = (len(oleft) + 1) // 2
      if ones >= half:
        oleft = onext
      else:
        oleft = znext
      # print(oleft)

      if len(cleft) > 1:
        ones = 0
        onext = []
        znext = []
        for val in cleft:
          if val[i] == '1':
            ones += 1
            onext.append(val)
          else:
            znext.append(val)
        half = (len(cleft) + 1) // 2
        if ones >= half:
          cleft = znext
        else:
          cleft = onext
        # print(cleft)

    ogv = int(oleft[0], 2)
    co2v = int(cleft[0], 2)
    print('og', ogv)
    print('co2', co2v)

    return ogv * co2v


day03.sample_test("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""", expect1=198, expect2=230)


if __name__ == '__main__':
  day03.run_and_check('input.txt', expect1=1307354, expect2=482500)
