#!/usr/bin/env python3
"AOC 2021: day 16"

from tools import aoc

def to_bits(hex_s):
  for b in ['{0:04b}'.format(int(c, 16)) for c in hex_s]:
    for c in b:
      yield int(c)


def stream(bits):
  for b in bits:
    yield b


def to_n(bits, nbits):
  ret = 0
  for b in bits:
    ret = (ret << 1) | b
    nbits -= 1
    if nbits <= 0:
      break
  return ret


class Packet(object):

  verbose = True

  def __init__(self):
    pass

  @staticmethod
  def munch(hex_s):
    if Packet.verbose:
      print('munch:', hex_s)
    bits = [b for b in to_bits(hex_s)]
    bitstream = to_bits(hex_s)
    used = 0
    ret = []
    while used < len(bits) - 7:
      p = Packet()
      ret.append(p)
      # u = p.load(bitstream)
      u = p.load(bits[used:])
      # print('used', u, p)
      used += u
    return ret

  def load(self, bits, level=0):
    #  0     1    2   3    4    5
    # 1101.0010.1111.1110.0010.1000
    # VVVT.TTAA.AAAB.BBBB.CCCC.C
    self.len = 0
    self.sub_packets = []
    self.n = 0

    self.version = to_n(bits, 3)
    self.id = to_n(bits[3:6], 3)
    self.ver_sum = self.version
    # print('  ' * level, 'v/id/sum', self)
    used = 6
    if self.id == 4:
      self.len_type = 4
    else:
      self.len_type = to_n(bits[used:used+1], 1)
      used += 1

    if self.id == 1:
      self.n = 1

    if self.len_type == 4:
      more = 1
      while more:
        tmp = to_n(bits[used:], 5)
        used += 5
        self.n = self.n << 4 | tmp & 0x0f
        more = tmp & 0x10
    elif self.len_type == 0:
      self.len = to_n(bits[used:], 15)
      used += 15
      if Packet.verbose:
        print('  ' * level, 'LEN TYPE 0: used:', used)
      done = used + self.len
      while used < done:
        p = Packet()
        self.sub_packets.append(p)
        used += p.load(bits[used:], level+1)
        self.process(p)
        if Packet.verbose:
          print('  ' * level, '  0sub  packet', p)
    else:
      self.np = to_n(bits[7:], 11)
      used += 11
      if Packet.verbose:
        print('  ' * level, 'LEN TYPE 1', self.np, 'subpackets')
      for i in range(self.np):
        p = Packet()
        self.sub_packets.append(p)
        used += p.load(bits[used:], level+1)
        self.process(p)
        if Packet.verbose:
          print('  ' * level, '  1sub packet', p)

    return used


  def process(self, p):
    self.ver_sum += p.ver_sum
    if self.id == 0:
      self.n += p.n
    elif self.id == 1:
      # print('==== product', self.n, p.n)
      self.n *= p.n
    elif self.id == 2:
      if len(self.sub_packets) == 1:
        self.n = p.n
      else:
        self.n = min(self.n, p.n)
    elif self.id == 3:
      if len(self.sub_packets) == 1:
        self.n = p.n
      else:
        self.n = max(self.n, p.n)
    elif self.id == 5:
      if len(self.sub_packets) == 2:
        self.n = int(self.sub_packets[0].n > self.sub_packets[1].n)
    elif self.id == 6:
      if len(self.sub_packets) == 2:
        self.n = int(self.sub_packets[0].n < self.sub_packets[1].n)
    elif self.id == 7:
      if len(self.sub_packets) == 2:
        self.n = int(self.sub_packets[0].n == self.sub_packets[1].n)


  def __str__(self):
    return 'v:%x, id:%x, sum:%d, n:%d, len:%d' % (self.version, self.id, self.ver_sum, self.n, self.len)


class day16(aoc.aoc):

  def __init__(self):
    super(day16, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True


  def part1(self):
    if self.trace_sample:
      print('===== Start part 1: ', self.all_input[0])
    else:
      print('===== Start part 1')

    packets = Packet.munch(self.all_input[0])
    # print(packets[0])
    return sum([p.ver_sum for p in packets])


  def part2(self):
    print('===== Start part 2')

    packets = Packet.munch(self.all_input[0])
    return packets[0].n

_ = Packet.munch('D2FE28')
_ = Packet.munch('EE00D40C823060')
_ = Packet.munch('38006F45291200')

Packet.verbose = False
day16.sample_test('D2FE28', expect1=6, expect2=None)
day16.sample_test('8A004A801A8002F478', expect1=16)
day16.sample_test('620080001611562C8802118E34', expect1=12)
day16.sample_test('C0015000016115A2E0802F182340', expect1=23)
day16.sample_test('A0016C880162017C3686B18A3D4780', expect1=31)

day16.sample_test('C200B40A82', expect1=14, expect2=3)
day16.sample_test('04005AC33890', expect1=8, expect2=54)
day16.sample_test('880086C3E88112', expect1=15, expect2=7)
day16.sample_test('CE00C43D881120', expect1=11, expect2=9)
day16.sample_test('D8005AC2A8F0', expect2=1)
day16.sample_test('F600BC2D8F', expect2=0)
day16.sample_test('9C005AC2F8F0 ', expect2=0)
day16.sample_test('9C0141080250320F1802104A08', expect1=20, expect2=1)


if __name__ == '__main__':
  day16.run_and_check('input.txt', expect1=929, expect2=911945136934)
