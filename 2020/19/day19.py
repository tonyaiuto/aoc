"AOC 2020: day 19"

from collections import defaultdict
import math

from tools import reader
from tools.memoized import memoized


def sample_test(s, expect, expect2=None):
  puzz = day19()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day19()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day19()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day19()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Rule(object):

  rules = {}
  trace1 = False
  trace2 = True

  def __init__(self, number=None, c=None, subrules=None):
    self.number = number
    self.c = c
    self.subrules = subrules
    self.all = None
    self.loops = False
    Rule.rules[number] = self
    self.depth = 0

  def __str__(self):
    if self.c:
      return '%d: %c' % (self.number, self.c)
    more = ' loops' if self.loops else ''
    return '%d: %s%s' % (self.number, self.subrules, more)


  @staticmethod
  def from_string(s):
     x = s.strip().split(':')
     number = int(x[0])
     rest = x[1].strip()
     if rest.startswith('"'):
       chr = rest[1]
       assert rest[2] == '"'
       return Rule(number=number, c=chr)
     else:
       subrules = []
       for sub in rest.split('|'):
          fs = [int(x) for x in sub.strip().split(' ')]
          subrules.append(fs)
       return Rule(number=number, subrules=subrules)

  def match1(self, msg):

    def submatch(rule, msg, lvl):
      if Rule.trace1:
        print(' '*lvl, 'submatch', rule, msg)
      if len(msg) == 0:
        return False, 0
      if rule.c:
        if msg[0] == rule.c:
          if Rule.trace1:
            print(' '*lvl, 'matched', rule, msg)
          return True, 1
        else:
          return False, 0

      for sub in rule.subrules:
        l = 0
        ok = True
        for s in sub:
          ok, lm = submatch(Rule.rules[s], msg[l:], lvl+1)
          if not ok:
            break
          l += lm
        if ok:
          if Rule.trace1:
            print(' '*lvl, 'matched', sub, l, msg)
          return True, l
      return False, 0

    ok, l = submatch(self, msg, 0)
    print('FINAL', ok, l, len(msg))
    return l == len(msg)

  @staticmethod
  def precomp():
    Rule.rules[0].subgen()

  def match2(self, msg):

    all_len = len(msg)
    all_matched = False
    max_depth = len(msg)
    print(self)

    def submatch(rule, msg, lvl):
      nonlocal all_len, max_depth
      print(' '*lvl, 'submatch', rule.number, msg)
      did_lens = set()

      if not rule.loops:
        #XX ret = []
        for s in rule.all:
          print(' '*lvl, 'check', s, msg)
          if msg.startswith(s):
            if Rule.trace2:
              print(' '*lvl, 'matched', rule, s, msg)
            ls = len(s)
            if ls not in did_lens:
              did_lens.add(ls)
              yield ls
	    #XX ret.append(s)
	    #XX return True, len(s)
        return

      for subset in rule.subrules:
        l = match_set(subset, msg, lvl+1)
        if l > 0:
          yield l
      return

    def match_set(rule_set, msg, lvl):
      if len(rule_set) == 0:
        yield 0

      if Rule.trace2:
          print(' '*lvl, 'match_subset', rule_set)
      for len_sm in submatch(Rule.rules[rule_set[0]], msg, lvl+1):
        if len(rule_set) > 1:
          l = match_set(rule_set[1:], msg[len_sm:], lvl+1)
          if l > 0:
            return len_sm + l
      return -1

    for _ in submatch(self, msg, 0):
      if all_matched:
        print('FINAL2', all_matched)
        return True
    print('FINAL2 fail')
    return False


  @staticmethod
  def precomp():
    Rule.rules[0].subgen()


  # memoized
  def subgen(self):
    if self.all:
      return self.all
    if self.c:
      self.loops = False
      self.all = [self.c]
      self.min_len = 1
      return self.all
    
    all = []
    for subset in self.subrules:
      tails = ['']
      for ri in range(len(subset)):
        rul = subset[len(subset)-1-ri]
        sr = Rule.rules[rul]
        foo = []
        for head in sr.subgen():
          print(rul, '=>', [head+tail for tail in tails])
          foo.extend([head+tail for tail in tails])
        tails = foo
        if rul in (8, 11):
          print('===========================')
          self.loops = True
        else:
          self.loops = self.loops or sr.loops
      all.extend(tails)

      print(self, ' => ', all[0:5])

    self.all = set(all)
    self.min_len = min([len(x) for x in all])
    return all


class day19(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True

  def reset(self):
    pass

  def load_file(self, file):
    self.all = reader.FileReader(file, by_group=True).load()
    self.post_load()

  def load_str(self, s):
    self.all = reader.StringReader(s, by_group=True).load()
    self.post_load()

  def do_line(self, line):
    pass

  def post_load(self):
    for line in self.all[0]:
      r = Rule.from_string(line)
      print(r)
    self.start = Rule.rules[0]
    self.messages = self.all[1]
    self.max_msg_len = max([len(m) for m in self.messages])


  def part1(self):
    print('===== Start part 1')
    self.reset()

    matches = 0
    for msg in self.messages:
      if self.start.match1(msg):
        matches += 1
    self.result1 = matches

    print('part1', self.result1)
    return self.result1

  def part2(self):
    print('===== Start part 2')
    self.reset()

    Rule.precomp()
    print('max_msg_len', self.max_msg_len)
    print('min 42 len', Rule.rules[42].min_len)

    # r = Rule.from_string('8: 42 | 42 8')
    ranges = []
    for i in range(1, 1+(self.max_msg_len // Rule.rules[42].min_len)):
      ranges.append([42 for _ in range(i)])
    print('ranges', ranges)
    r8 = Rule.rules[8]
    r8.subrules = ranges
    r8.loops = True
    print('rule8=', r8)

    # r = Rule.from_string('11: 42 31 | 42 11 31')
    r11 = Rule.rules[11]
    ranges = []
    for i in range(1, 1+(
        self.max_msg_len // (Rule.rules[42].min_len+Rule.rules[31].min_len))):
      ranges.append([42 for _ in range(i)] + [31 for _ in range(i)])
    print('ranges', ranges)
    r11.subrules = ranges
    r11 = Rule.rules[11]
    r11.loops = True

    for i in range(0,50):
      r = Rule.rules.get(i)
      if r:
        print(r)

    matches = 0
    for msg in self.messages:
      if self.start.match1(msg):
        matches += 1
    self.result2 = matches

    print('part2', self.result2)
    return self.result2



sample_test("""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""", 2, None)

sample_test("""
0: 8 11
1: "a"
2: 1 24 | 14 4
3: 5 14 | 16 1
4: 1 1
5: 1 14 | 15 1
6: 14 14 | 1 14
7: 14 5 | 1 21
8: 42
9: 14 27 | 1 26
10: 23 14 | 28 1
11: 42 31
12: 24 14 | 19 1
13: 14 3 | 1 12
14: "b"
15: 1 | 14
16: 15 1 | 14 14
17: 14 2 | 1 7
18: 15 15
19: 14 1 | 14 14
20: 14 14 | 1 15
21: 14 1 | 1 14
22: 14 14
23: 25 1 | 22 14
24: 14 1
25: 1 1 | 1 14
26: 14 22 | 1 20
27: 1 6 | 14 18
28: 16 1
31: 14 17 | 1 13
42: 9 14 | 10 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""", 3, 12)


if __name__ == '__main__':
  # main('input.txt', None, None)
  pass
