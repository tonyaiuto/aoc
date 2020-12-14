"AOC 2020: day 14"

from collections import defaultdict
import math

from tools import reader
import intcode


def sample_test(s, expect, expect2=None):
  puzz = day14()
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
  puzz = day14()
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


def mask_val(word, mask0, mask1):
   return (word & ~mask0) | mask1


def reverse(s):
  ret = [''] * len(s)
  j = len(ret) - 1
  for c in s:
    ret[j] = c
    j -= 1
  return ''.join(ret)

def proc_mask(mask):
  m0 = 0
  m1 = 0
  mx = 0
  for c in mask:
    m0 <<= 1
    m1 <<= 1
    mx <<= 1
    if c == '0':
      m0 |= 1
    elif c == '1':
      m1 |= 1
    elif c == 'X':
      mx |= 1
    else:
      print('bad mask', mask)
      assert fail
  assert (m0 | m1 | mx) & 0xfffffffff == 0xfffffffff
  assert (m0 & m1) == 0
  assert (m0 & mx) == 0
  assert (m1 & mx) == 0
  return m0, m1, mx


class day14(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.mask = 0
    self.proc = intcode.Intcode()
    self.mem = {}

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
    # mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    # mem[8] = 11
    # mem[7] = 101
    # mem[8] = 0
    if not line:
      return
    if line.startswith('mask = '):
      mask = line[7:]
      self.mask0, self.mask1, self.maskx = proc_mask(mask)
      print('mask %s -> %012o, %012o, %012o' % (mask, self.mask0, self.mask1, self.maskx))
    elif line.startswith('mem['):
      addr = 0
      x = line[4:].replace('] = ', ',').split(',')
      addr = int(x[0])
      val = int(x[1])
      print('  mem[%3d] <- %3d %6o %012o' % (addr, val, val, mask_val(val, self.mask0, self.mask1)))
      self.mem[addr] = mask_val(val, self.mask0, self.mask1)
      pass
    else:
      print('bad input', line)
      assert False

  def post_load(self):
    pass



  def part1(self):
    print('===== Start part 1')
    self.reset()
    sum = 0
    for loc, val in self.mem.items():
      sum += val
    self.result1 = sum



    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = None


    print('part2', self.result2)
    return self.result2



sample_test("""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""", 165)



if __name__ == '__main__':
  main('input.txt', None, None)
