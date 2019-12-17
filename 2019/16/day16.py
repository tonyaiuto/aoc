#!/usr/bin/env python3

import sys

INP='59790677903322930697358770979456996712973859451709720515074487141246507419590039598329735611909754526681279087091321241889537569965210074382210124927546962637736867742660227796566466871680580005288100192670887174084077574258206307557682549836795598410624042549261801689113559881008629752048213862796556156681802163843211546443228186862314896620419832148583664829023116082772951046466358463667825025457939806789469683866009241229487708732435909544650428069263180522263909211986231581228330456441451927777125388590197170653962842083186914721611560451459928418815254443773460832555717155899456905676980728095392900218760297612453568324542692109397431554'


BASE_PATTERN = [0, 1, 0, -1]

def str_to_list(s):
  return [int(c) for c in s]


def base(digit_pos, pos):
  # digit_pos: 3
  # assert [0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0, 0, 0]
  return BASE_PATTERN[pos // digit_pos % 4]


def do_mul(input, digit):
  # digit is 1 based
  tot = 0
  # For thinking about it
  #for i, d in enumerate(input):
  #  tot += d * BASE_PATTERN[((i+1) // digit) % 4]
  #  But note the diagonal of the 0
  if digit > len(input) // 2:
    return sum(input[digit-1:]) % 10
  for i in range(digit-1, len(input)):
    b = BASE_PATTERN[((i+1) // digit) % 4]
    if b == 1:
       tot += input[i]
    elif b == -1:
       tot -= input[i]
  return abs(tot) % 10

def do_mul(input, digit):


def do_fft(input, passes=1):
  # not property of mask, that after computing digit i, it is not needed
  # any more
  for _ in range(passes):
    for i in range(len(input)):
      input[i] = do_mul(input, i+1)
  return input


def do_fft_2(input, passes=1):
  end = len(input)
  out = list(input)
  rsum = input[end-1]
  for pos in range(end - 2, -1, -1):
    out[pos] = (input[pos] + rsum * passes) % 10
    rsum += input[pos]
  return out

"""
12345678
01029498

7 + 8 * 4 = 39
6 + 7 * 4 = 34
5 + 6 * 4 = 29

"""


def check_100(input_s, first8):
  input = str_to_list(input_s)
  expect = str_to_list(first8)
  got = do_fft(input, passes=100)
  print('expect', expect, ', got', got)
  # assert expect == got[0:8]


def test_fft():
  assert  0 ==  base(1, 0)
  assert  1 ==  base(1, 1)
  assert  0 ==  base(1, 2)
  assert -1 ==  base(1, 3)
  assert  0 ==  base(1, 4)
  assert  0 ==  base(3, 0)
  assert  0 ==  base(3, 1)
  assert  0 ==  base(3, 2)
  assert  1 ==  base(3, 3)
  assert  0 ==  base(3, 12)

  input = [int(c) for c in '12345678']
  p1 = do_fft(input)
  print('expect [4, 8, 2, 2, 6, 1, 5, 8], got', p1)
  # assert [4, 8, 2, 2, 6, 1, 5, 8] == p1

  check_100('80871224585914546619083218645595', '24176176')
  check_100('19617804207202209144916044189917', '73745418')
  check_100('69317163492948606335995924319873', '52432133')


def part1():
  input = str_to_list(INP)
  assert len(input) % 2 == 0
  got = do_fft(input, passes=100)
  first8 = ''.join([str(d) for d in got[0:8]])
  print('pass1', first8)
  assert '19239468' == first8


def part2():
  message_offset = int(INP[0:7])
  print('message offset', message_offset)
  inp1 = str_to_list(INP)
  input = inp1 * 10000
  # got = do_fft(input, passes=100)
  got = do_fft(input, passes=1)
  message = got[message_offset:message_offset+8]
  print('part2:', message)



if __name__ == '__main__':
  test_fft()
  part1()
  # part2()

