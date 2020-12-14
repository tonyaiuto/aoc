"AOC 2020: day 14"

from collections import defaultdict
import functools
import math

from tools import reader


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

def run2(s):
  puzz = day14()
  puzz.mode = 2
  puzz.load_str(s)
  res = puzz.part2()


def main(input, e1=None, e2=None):
  puzz = day14()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day14()
  puzz.mode = 2
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


def mask_val(word, mask0, mask1):
   return (word & ~mask0) | mask1


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
    self.mem = {}
    self.mode = 1

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
    if line.startswith('mask = '):
      mask = line[7:]
      self.raw_mask = mask
      self.mask0, self.mask1, self.maskx = proc_mask(mask)
      print('mask %s -> %09x, %09x, %09x' % (mask, self.mask0, self.mask1, self.maskx))
    elif line.startswith('mem['):
      addr = 0
      x = line[4:].replace('] = ', ',').split(',')
      addr = int(x[0])
      val = int(x[1])
      print('  mem[%3d] <- %3d %6x %09x' % (addr, val, val, mask_val(val, self.mask0, self.mask1)))
      if self.mode == 1:
        self.mem[addr] = mask_val(val, self.mask0, self.mask1)
      else:
        self.write_many(addr, val)
    else:
      print('bad input', line)
      assert False

  def post_load(self):
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.mode = 1
    sum = 0
    for loc, val in self.mem.items():
      sum += val
    self.result1 = sum

    print('part1', self.result1)
    return self.result1


  def write_many(self, addr, val):

    # Find the X's and positions in the mask
    n_floating_bits = 0          # # of floating bits
    bits = []       # set of bit values of the floating bits
    keep_mask = 0   # mask to keep the non-floating address bits on
    force_on_mask = 0
    bit = 1 << 35
    for c in self.raw_mask:
      keep_mask <<= 1
      force_on_mask <<= 1
      if c == 'X':
        n_floating_bits += 1
        bits.append(bit)
      else:
        keep_mask |= 1
        if c == '1':
          force_on_mask |= 1
      bit >>= 1

    print('n_floating_bits', n_floating_bits, bits, range, 1 << n_floating_bits)
    print('   force_on_mask:%9x, keep_mask: %9x' % (force_on_mask, keep_mask))

    fixed_bits = (addr | force_on_mask) & keep_mask
    print('   fixed_bits      %9x' % fixed_bits)
    for faddr in range(1 << n_floating_bits):
     eaddr = fixed_bits
     f = faddr
     for bit in bits:
       if f & 1 != 0:
         eaddr |= bit
       f >>= 1
     # print('    %d -> set @ %9x %d' % (faddr, eaddr, eaddr))
     self.mem[eaddr] = val


  def part2(self):
    print('===== Start part 2')
    #self.reset()
    #self.mode = 2
    sum = 0
    for loc, val in self.mem.items():
      sum += val
    self.result2 = sum

    print('part2', self.result2)
    return self.result2


sample_test("""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""", 165)

run2("""
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""")


if __name__ == '__main__':
  main('input.txt', 6317049172545, 3434009980379)
  pass 
