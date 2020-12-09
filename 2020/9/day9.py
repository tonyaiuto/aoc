"AOC 2020: day 9"

from collections import defaultdict

import reader


def sample_test1(s, window, expect):
  puzz = day9(window=window)
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

def sample_test2(s, window, expect):
  puzz = day9(window=window)
  puzz.load_str(s)
  res = puzz.part1()
  res2 = puzz.part2(res)
  if expect != res2:
    print('FAIL: expect', expect, 'got', res2)
    assert expect == res2


def main(input):
  puzz = day9()
  puzz.load_file(input)
  res = puzz.part1()
  assert res == 25918798
  print('part1', res)
  res2 = puzz.part2(res)
  print('part2', res2)
  assert res2 == 3340942


class day9(object):

  def __init__(self, window=25):
    self.window = window
    self.pos = window - 1
    self.buf = [0]*window
    self.all = []
    self.sums = []
    self.in_sums = {}
    self.n = 0
    self.in_window = defaultdict(int)
    self.first = -1

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for line in all:
      if line:
        self.do_line(line)


  def load_str(self, s):
    all = reader.StringReader(s).load()
    for line in all:
      if line:
        self.do_line(line)


  def do_line(self, line):
    v = int(line)
    self.all.append(v)
    if self.n > 0:
      self.sums.append(self.sums[-1]+v)
    else:
      self.sums.append(v)
    self.in_sums[self.sums[-1]] = self.n
    self.n += 1
    next = (self.pos + 1) % self.window

    # print('next', next)
    valid = False
    if self.n > self.window:
      for i in range(self.window):
        n = self.buf[i]
        # print('check for', n, v - n)
        maybe = self.in_window.get(v - n)
        if maybe and maybe > 0:
          # print('valid', v, n, '+', v-n)
          valid = True
          break
      self.in_window[self.buf[next]] -= 1
    self.pos = next
    self.buf[next] = v
    self.in_window[v] += 1
    # print(self.pos, '@', self.buf)
    # print(','.join('%d:%d' % (k, v) for k, v in self.in_window.items()))
    if self.n > self.window and not valid:
      print('invalid', v)
      if self.first < 0:
        self.first = v
      return False
    return True

  def part1(self):
    print('part1', self.first)
    return self.first

  def part2(self, want):
    print(self.all)
    print(self.sums)
    for i in range(self.n):
      print('at', i, self.sums[i], 'want', self.sums[i] + want)
      sp = self.in_sums.get(self.sums[i] + want)
      if sp and sp - i > 1:
        j = i + 1
        print('got it at', j, 'to', sp, self.all[j:sp+1])
        mn = mx = self.all[j]
        for x in self.all[j:sp+1]:
          mn = min(mn, x)
          mx = max(mx, x)
        print(mn, mx, '=>', mn+mx)
        return mn+mx
        


SAMP="""
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""
sample_test1(SAMP, 5, 127)

sample_test2(SAMP, 5, 62)


if __name__ == '__main__':
  main('input.txt')
