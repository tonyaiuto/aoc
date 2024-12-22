
import sys

A=41644071
B=0
C=0

# Program: 2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0

program = [2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0]

expect=[3,1,5,3,7,4,2,7,5]


for i in range(20):
       B = A % 8
       B = B ^ 2
       assert B == (A % 8) ^ 2
       C = A // (2 ** B)
       assert C == A // (2 ** ((A % 8) ^ 2))
       B = B ^ 7
       assert B == (A % 8) ^ 5
       B = B ^ C
       assert B == ((A % 8) ^ 5) ^ (A // (2 ** ((A % 8) ^ 2)))
       A = A // (2 ** 3)
       # print(B % 8)
       if B % 8 != expect[i]:
         print("OFF THE RAILS AT", i, A, B, C, expect)
         sys.exit(1)
       if A == 0:
         break
print("smoke test OK")




# Condensed
def run_quick(A, expect):
  A_save = A
  B=0
  C=0
  for i in range(len(expect)):
    # B = (A % 8) ^ 2
    # C = A // (2 ** ((A % 8) ^ 2))
    # B = ((A % 8) ^ 2 ^ 7) ^ (A // (2 ** ((A % 8) ^ 2)))

    B = ((A % 8) ^ 5) ^ (A // (2 ** ((A % 8) ^ 2)))
    # print(B % 8)
    if B % 8 != expect[i]:
      # print("OFF THE RAILS AT", i, A, B, C, expect)
      return False
    A = A // 8
    #if A == 0:
    #  break

  print(A_save, "=>", expect)
  return True

assert run_quick(A=41644071, expect=[3,1,5,3,7,4,2,7,5])


program = [2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0]
rp = list(reversed(program))


ALL_GOOD = set()

def try_from(a):
  possible_a = set([a])
  for digit in rp:
    # B = ((A % 8) ^ 5) ^ (A // (2 ** ((A % 8) ^ 2)))
    # print(B % 8)
    # A = A // 8
   
    # what must the low digit b
    b_mod_8 = digit
    print("=Looking for digit", b_mod_8, len(possible_a), "possible starts")
    npa = set()
    for a in possible_a:
      for last_digit_of_a in range(8):
        new_a = a << 3 | last_digit_of_a
        if run_quick(A=new_a, expect=program):
          print("GOT IT AT", new_a)
          ALL_GOOD.add(new_a)
          # return new_a

        if b_mod_8 == ((last_digit_of_a ^ 5) ^ (new_a // (2 ** (last_digit_of_a ^ 2)))) % 8:
          # print("got new at %o" % new_a, "%o" % a, last_digit_of_a, digit)
          npa.add(new_a)
    possible_a = npa
  return 0


for a in range(0,8):
  got = try_from(a)
  if got > 0:
    if run_quick(A=got, expect=program):
      break

# print(ALL_GOOD)
answer = min(ALL_GOOD)
size_check = len("%o" % answer) - len(program)
if size_check > 0:
  print('part2', answer, "%o" % answer, "whomp. Too large by %d digits", size_check)
  sys.exit(1)
else:
  print('part2', answer, "(octal: %o)" % answer)

# 1597968194550799 is too high,
#  472068288494607 is too high
#  472068287708175
#   190593310997519
# part2 190593310997519 (octal: 5325376646236017)
# print(min(possible_a))
  

#  am = [2412751744035530]
inca = 0o1000000000000000

a = inca

"""
  possible_a = set([a])
  for digit in rp:
    # B = ((A % 8) ^ 5) ^ (A // (2 ** ((A % 8) ^ 2)))
    # print(B % 8)

    if run_quick(A=got, expect=program):
"""

"""
b = 0
c = 0
#for big_a in range(0o100000, 0o1000000, 0o100000):
for big_a in range(0, 0o1000, 0o100):
  for a in range(big_a, big_a+8):
    b1 = a % 8
    b2 = b1 ^ 2
    c = a // (2 ** b2)
    b3 = b2 ^ 7
    b4 = b ^ c
    out = b4 % 8
    na = a // 8
    print("%8o  %o %o %8o %o %8o %8o" % (a, b1, b2, c, b3, b4, na), '=>', out)


x ^ 2

0 2 
1 3
2 0
3 1
4 6
5 7
6 4
7 5

  41644071    236670047  27b7027 => [3, 1, 5, 3, 7, 4, 2, 7, 5]
41644071 => [3, 1, 5, 3, 7, 4, 2, 7, 5]
  41644072    236670050  27b7028 => [7, 4, 5, 3, 7, 4, 2, 7, 5]

    146447       436017    23c0f => [2, 4, 1, 2, 7, 1]
    166833       505661    28bb1 => [2, 4, 1, 2, 7, 0]
    211983       636017    33c0f => [2, 4, 1, 2, 7, 3]
    277519      1036017    43c0f => [2, 4, 1, 2, 7, 7]
    343055      1236017    53c0f => [2, 4, 1, 2, 7, 5, 4]
    408591      1436017    63c0f => [2, 4, 1, 2, 7, 1]
    474127      1636017    73c0f => [2, 4, 1, 2, 7, 3]
    539663      2036017    83c0f => [2, 4, 1, 2, 7, 1]
    605199      2236017    93c0f => [2, 4, 1, 2, 7, 5, 5]
    670735      2436017    a3c0f => [2, 4, 1, 2, 7, 1]
    691121      2505661    a8bb1 => [2, 4, 1, 2, 7, 0]
    736271      2636017    b3c0f => [2, 4, 1, 2, 7, 2]
    801807      3036017    c3c0f => [2, 4, 1, 2, 7, 3]
    867343      3236017    d3c0f => [2, 4, 1, 2, 7, 5, 7]
    932879      3436017    e3c0f => [2, 4, 1, 2, 7, 1]
    998415      3636017    f3c0f => [2, 4, 1, 2, 7, 2]


Octal first digit -> last digit
0        0 => [5]
1        1 => [4]
2        2 => [5]
3        3 => [7]
4        4 => [1]
5        5 => [0]
6        6 => [3]
7        7 => [2]

Second digit

0	7
1	5
2	5
3	3
4	1
5	0
6	3
7	2


56


2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0
"""
