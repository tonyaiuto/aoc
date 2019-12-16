#!/usr/bin/env python3

import sys



INP='59790677903322930697358770979456996712973859451709720515074487141246507419590039598329735611909754526681279087091321241889537569965210074382210124927546962637736867742660227796566466871680580005288100192670887174084077574258206307557682549836795598410624042549261801689113559881008629752048213862796556156681802163843211546443228186862314896620419832148583664829023116082772951046466358463667825025457939806789469683866009241229487708732435909544650428069263180522263909211986231581228330456441451927777125388590197170653962842083186914721611560451459928418815254443773460832555717155899456905676980728095392900218760297612453568324542692109397431554'


BASE_PATTERN = [0, 1, 0, -1]

def str_to_list(s):
  return [int(c) for c in s]

def do_mul(input, pattern):
  sum = 0
  # msg = []
  for i,d in enumerate(input):
    # msg.append('%d * %d' % (d, pattern[(i+1)%len(pattern)]))
    sum += d * pattern[(i+1)%len(pattern)]
  # print('%s = %d' % (' + '.join(msg), sum))
  return abs(sum) % 10


def expand_base(pos):
  ret = []
  for d in BASE_PATTERN:
    ret.extend([d] * pos)
  return ret


def do_fft(input, passes=1):
  for _ in range(passes):
    out = []
    for i in range(len(input)):
      out.append(do_mul(input, expand_base(i+1)))
    input = out
  return out


def check_100(input_s, first8):
  input = str_to_list(input_s)
  expect = str_to_list(first8)
  got = do_fft(input, passes=100)
  # print('expect', expect, ', got', got)
  assert expect == got[0:8]


def test_fft():
  input = [int(c) for c in '12345678']
  assert [0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1] == expand_base(3)
  assert 4 == do_mul(input, expand_base(1))
  assert 8 == do_mul(input, expand_base(2))
  assert 2 == do_mul(input, expand_base(3))
  assert 2 == do_mul(input, expand_base(4))
  assert 6 == do_mul(input, expand_base(5))
  assert 8 == do_mul(input, expand_base(8))
  p1 = do_fft(input)
  assert [4, 8, 2, 2, 6, 1, 5, 8] == p1

  check_100('80871224585914546619083218645595', '24176176')
  check_100('19617804207202209144916044189917', '73745418')
  check_100('69317163492948606335995924319873', '52432133')


def part1():
  input = str_to_list(INP)
  got = do_fft(input, passes=100)
  print('pass1', ''.join([str(d) for d in got[0:8]]))


if __name__ == '__main__':
  test_fft()
  part1()
  # part2()

