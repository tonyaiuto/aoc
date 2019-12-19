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

TRACE = False

def do_mul(input, digit):
  # digit is 1 based
  tot = 0
  # For thinking about it
  #for i, d in enumerate(input):
  #  tot += d * BASE_PATTERN[((i+1) // digit) % 4]
  #  But note the diagonal of the 0
  #if digit > len(input) // 2:
  #  return sum(input[digit-1:]) % 10
  msg = '   ' * (digit-1)
  for i in range(digit-1, len(input)):
    b = BASE_PATTERN[((i+1) // digit) % 4]
    if b == 1:
       msg += ' +%d' % input[i]
       tot += input[i]
    elif b == -1:
       msg += ' -%d' % input[i]
       tot -= input[i]
    else:
       msg += '   '
  d = abs(tot) % 10
  if TRACE:
    msg += ' = %d' % d
    print(msg)
  return d


def do_fft(input, passes=1):
  # not property of mask, that after computing digit i, it is not needed
  # any more
  for _ in range(passes):
    for i in range(len(input)):
      input[i] = do_mul(input, i+1)
  return input


def do_fft_2(input, passes=1):
  end = len(input)
  for _ in range(passes):
    rsum = 0
    for pos in range(end - 1, - 1, -1):
      rsum += input[pos]
      input[pos] = rsum % 10
  return input


def check_100(input_s, first8):
  input = str_to_list(input_s)
  expect = str_to_list(first8)
  got = do_fft(input, passes=100)
  print('expect', expect, ', got', got)
  assert expect == got[0:8]

  split_point = len(input) // 2
  for i in range(10):
    got = do_fft(list(input), passes=i)
    got2 = do_fft_2(list(input), passes=i)
    # print('fft ', got)
    # print('fft2', got2)
    assert got[split_point:] == got2[split_point:]


def test_fft():
  global TRACE

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

  TRACE = True
  input = [int(c) for c in '12345678']
  p1 = do_fft(input)
  print('expect [4, 8, 2, 2, 6, 1, 5, 8], got', p1)
  # assert [4, 8, 2, 2, 6, 1, 5, 8] == p1

  input = [int(c) for c in '12345678']
  do_fft(input, passes=4)

  TRACE = False

  check_100('80871224585914546619083218645595', '24176176')
  check_100('19617804207202209144916044189917', '73745418')
  check_100('69317163492948606335995924319873', '52432133')


def part1():
  input = str_to_list(INP)
  assert len(input) % 2 == 0
  got = do_fft(input, passes=100)
  first8 = ''.join([str(d) for d in got[0:8]])
  print('part1', first8)
  assert '19239468' == first8


def part2():
  input = str_to_list(INP)
  message_offset = int(INP[0:7])
  need = len(input) * 10000 - message_offset
  print('message offset:', message_offset, 'of', len(input) * 10000,
        ', need:', need)
  assert message_offset == 5979067
  len(input) * 100
  i_offset = message_offset % len(input)
  more_times = need // len(input)
  # print('len(input) * 10000', len(input) * 10000)
  # print('len(input) - i_offset + more_times * len(input)', len(input), i_offset, more_times, len(input))
  # print(len(input) - i_offset + more_times * len(input))
  assert need == len(input) - i_offset + more_times * len(input)
  new_input = input[i_offset:] + input * more_times
  assert need == len(new_input)

  got = do_fft_2(new_input, passes=1)
  first8 = ''.join([str(d) for d in got[0:8]])
  print('part2 1p', first8)

  new_input = input[i_offset:] + input * more_times
  got = do_fft_2(new_input, passes=10)
  first8 = ''.join([str(d) for d in got[0:8]])
  print('part2 10p', first8)

  new_input = input[i_offset:] + input * more_times
  got = do_fft_2(new_input, passes=100)
  first8 = ''.join([str(d) for d in got[0:8]])
  print('part2', first8)


if __name__ == '__main__':
  test_fft()
  part1()
  part2()

