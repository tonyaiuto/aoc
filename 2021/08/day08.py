"AOC 2021: day 08"

from collections import defaultdict
import math

from tools import aoc


len_to_digit = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}

class E(object):

  def __init__(self, signals, displayed):
    self.signals = [sorted(v) for v in signals.strip().split(' ')]
    self.displayed = [set(v) for v in displayed.strip().split(' ')]

  def __str__(self):
    return str(self)


class day08(aoc.aoc):

  def __init__(self):
    super(day08, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.e = []
    self.sigs = {}

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    signal, output = line.split('|')
    e = E(signal, output)
    self.e.append(e)
    for s in e.signals:
      key = ''.join(s)
      if key not in self.sigs:
        self.sigs[key] = s
  

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    ret = 0
    for f in self.e:
      for d in f.displayed:
        if len(d) in len_to_digit:
          ret = ret + 1
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()

    # print(self.sigs)
    ret = 0
    for f in self.e:
      m = [0] * 10
      for sig in f.signals:
        l = len(sig)
        if l == 2:
          if m[1] != set(sig):
            print('m1 might be', sig)
          m[1] = set(sig)
        elif l == 4:
          m[4] = set(sig)
        elif l == 3:
          m[7] = set(sig)
        elif l == 7:
          m[8] = set(sig)
      print('m1', m[1])
      print('m4', m[4])
      print('m7', m[7])
      print('m8', m[8])
      top = m[7] - m[1]
      print('top', top)

      left_l = m[4] - m[7]
      print('left_l', left_l)

      for sig in f.signals:
        l = len(sig)
        if l == 6:  # 0 or 6
          if contains_all_seg_of(sig, m[7]) and contains_all_seg_of(sig, left_l):
            m[9] = set(sig)
            print('m9 might be', sig)
          elif contains_all_seg_of(sig, m[1]):
            # must be 0
            m[0] = set(sig)
            print('m0 might be', sig)
          else:
            m[6] = set(sig)
            print('m6 might be', sig)
        elif l == 5:
          if contains_all_seg_of(sig, m[7]):
            m[3] = set(sig)
            print('m3 might be', sig)
          else:
            if contains_all_seg_of(sig, left_l):
              m[5] = set(sig)
              print('m5 might be', sig)
            else:
              m[2] = set(sig)
              print('m2 might be', sig)

      if self.trace_sample:
        for i in range(10):
          print(' ->', i, m[i])

      value = 0
      for d in f.displayed:
        # print('check', d)
        for i in range(10):
          if d == m[i]:
            value = value * 10 + i
      if self.trace_sample:
         print("got", value)
      ret += value
    return ret

def contains_all_seg_of(maybe, known):
  for seg in known:
    if seg not in maybe:
      return False
  return True

def contains_any_seg_of(maybe, known):
  for seg in known:
    if seg in maybe:
      return True
  return False

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

day08.sample_test("""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
""", expect1=None, expect2=5353)


day08.sample_test("""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""", expect1=26, expect2=61229)

if __name__ == '__main__':
  day08.run_and_check('input.txt', expect1=None, expect2=None)
  pass
