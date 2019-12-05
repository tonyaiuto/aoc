#!/usr/bin/env python3



def to_digits(i):
  ret = [0] * 6
  t = i
  for di in range(6):
    ret[5-di] = t % 10
    t = t // 10
  return ret


assert to_digits(206938) == [2, 0, 6, 9, 3, 8]

def is_ok1(i):
  last = 0
  double = False
  for d in to_digits(i):
    if d < last:
      return False
    if d == last:
      double = True
    last = d
  return double
   

assert is_ok1(111111) == True
assert is_ok1(223450) == False
assert is_ok1(123789) == False


def part1(low, high):
  i = low
  found = 0
  while i <= high:
    if is_ok1(i):
      print(i)
      found += 1
    i += 1
  print('part1:', found)


def is_ok2(i):
  last = 0
  freq = [0]*10
  in_row = 0
  for d in to_digits(i):
    if d < last:
      return False
    if d == last:
      freq[d] += 1
    else:
      freq[d] = 1
    last = d
  dlist = [True for d in freq if d == 2]
  print(i, freq, dlist)
  return len(dlist) > 0
 

assert is_ok2(222222) == False
assert is_ok2(112233) == True
assert is_ok2(123444) == False
assert is_ok2(111122) == True


def part2(low, high):
  i = low
  found = 0
  while i <= high:
    if is_ok2(i):
      print(i)
      found += 1
    i += 1
  print('part2:', found)


# part1(206938, 679128)
part2(206938, 679128)
