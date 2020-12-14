"AOC 2020: day 13"

from collections import defaultdict
import math
from functools import reduce

from tools import reader


def lcm(periods):
  lcm = periods[0]
  for i in periods[1:]:
    lcm = lcm * i // math.gcd(lcm, i)
  return lcm

def is_prime(n):
  if (n & 1) == 0:
    return False
  i = 1
  while i * i < n:
    i += 2
    if (n // i) * i == n:
     return False
  return True


def sample_test(s, expect, expect2=None):
  puzz = day13()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res
  if expect2:
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day13()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Foo(object):

  def __init__(self):
    pass


  def __str__(self):
    return str(self)



class day13(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.lines = 0

  def reset(self):
    pass

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    all = reader.StringReader(s).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    self.lines += 1
    if self.lines == 1:
      self.etime = int(line)
    elif self.lines == 2:
      self.all_times = line.split(',')

  def post_load(self):
    print(self.all_times)
    self.live = [int(x) for x in self.all_times if x != 'x']
    print(self.live)
    pass



  def part1(self):
    self.reset()
    self.result1 = None
    min_wait = self.etime
    mmt = -1
    d = max([x for x in self.live])
    for x in self.live:
      dst = x * int(self.etime / x)
      if dst == self.etime:
        print('exact, match on', x)
        self.result1 = 0
        return
      wait = (dst + x) - self.etime
      print('======', x, dst, wait)
      if wait < min_wait:
        min_wait = wait
        mmt = x
    self.result1 = mmt * min_wait
    print('bus @ ', mmt, 'is good') 

    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('------- part 2')
    self.reset()
    self.result2 = None

    # Build list of dispatch cycles and their indicies
    foo = []
    for t in range(len(self.all_times)):
      if self.all_times[t] == 'x':
        continue
      foo.append((t, int(self.all_times[t])))
      print(t, int(self.all_times[t]))
    foo.sort(reverse=True, key = lambda x: x[1])
    # [(0, 7), (1, 13), (7, 19), (6, 31), (4, 59)]
    print(foo)

    d = foo[0][1]
    t = d

    # Find the # iterations of first dispatch cycle needed to align with each of
    # the others. 
    cyc = [1] * len(foo)
    d_cycle = foo[0][1]
    t = d_cycle
    delta = foo[0][0]
    for fi in range(1, len(foo)):
      x = foo[fi]
      t = d_cycle
      while True:
        t += d_cycle
        if (t - delta + x[0]) % x[1] == 0:
          cyc[fi] = int(t / d_cycle)
          break
    # expect something like [1, 288, 32, 8, 29, 23, 19, 4, 13]
    print('cycles:', cyc)

    """
    # Build up the iteration jump accross all routes
    cyc = [1] * len(foo)
    d_cycle = foo[0][1]
    t = d_cycle
    delta = foo[0][0]
    for fi in range(1, len(foo)):
      # compute how many loops of previous cycles it takes to aling with me.
      x = foo[fi]
      t = d_cycle
      while True:
        t += d_cycle
        if (t - delta + x[0]) % x[1] == 0:
          cyc[fi] = int(t / d_cycle)
          d_cycle = t
          break
    # expect something like [1, 288, 32, 8, 29, 23, 19, 4, 13]
    print('cycles:', cyc)
    print('d_cycle:', d_cycle)
    print('== is the answer', foo[-1][1] * d_cycle)
    """

    primes = set()
    for i in range(1, len(cyc)):
      for j in range(i+1, len(cyc)):
        gcd = math.gcd(cyc[i], cyc[j])
        print('gcd %d %d => %d' % (cyc[i], cyc[j], gcd))
        if gcd == 1:
          primes.add(cyc[i])
          primes.add(cyc[j])
    print('primes', primes)

    primes = set()
    for c in cyc:
      if is_prime(c):
        primes.add(c)
    print('primes2', primes)
    lcm_cyc = lcm(cyc)
    print('lcm', lcm_cyc)

    # This always works, but it is slow. It is just the first period.
    d = cyc[0] * foo[0][1]

    # d = lcm_cyc
    # d = d_cycle
    # d = cyc[1] * foo[0][1]

    print('skip (cyc * dcyc0)', d)

    if foo[0][1] == 787:
      # [1, 288, 32, 8, 29, 23, 19, 4, 13]
      d = foo[0][1] * 29 * 23 * 19 * 13
      d = foo[0][1] * reduce((lambda x, y: x*y), primes)
      # return

    t = 0
    n_loop = 0
    n_hits = 0
    while True:
      n_loop += 1
      t += d
      is_t = True
      for x in foo[1:]:
        if (t - delta + x[0]) % x[1] == 0:
          # print('maybe at', t, 'on', x)
          n_hits += 1
        else:
          is_t = False
          break
      if is_t:
        self.result2 = t - delta
        break

    print('# loops', n_loop, 'hits', n_hits)
    print('part2', self.result2)
    #for f in [(0, d)] + foo:
    #  print(f[1], self.result2 % f[1], 'expect', f[0])

 
    if foo[0][1] == 787:
      print('  big input: too low ', 100000000000000)
      print('  big input: too high', 265889040662602637)
      print('  big input: too high', 6227853516434245)
    print('part2   ', self.result2)
    return self.result2



sample_test("""939
7,13,x,x,59,x,31,19""", 295, expect2=1068781)


def try2(s, expect):
  puzz = day13()
  puzz.load_str(s)
  res = puzz.part2()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

try2("""939\n17,x,13,19""", 3417)
try2("""1\n67,7,59,61""", 754018)
try2("""1\n67,x,7,59,61""", 779210)
try2("""1\n67,7,x,59,61""", 1261476)
try2("""1\n1789,37,47,1889""", 1202161486)



if __name__ == '__main__':
  main('input.txt', 3997, 500033211739354)
  pass
