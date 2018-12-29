#!python

import time

#ip 2

r0 = 1
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0

#     0  addi 2 16 2
#     1	seti 1 4 1
#     2	seti 1 2 4
#     3	mulr 1 4 3
#     4	eqrr 3 5 3
#     5	addr 3 2 2
#     6	addi 2 1 2
#     7	addr 1 0 0
#     8	addi 4 1 4
#     9	gtrr 4 5 3
#     10	addr 2 3 2
#     11	seti 2 7 2
#     12	addi 1 1 1
#     13	gtrr 1 5 3
#     14	addr 3 2 2
#     15	seti 1 0 2
#     16	mulr 2 2 2

def sub17():
    global r0, r1, r2, r3, r4, r5
    # 17	addi 5 2 5
    # ip=17 [1, 0, 17, 0, 0, 0] addi 5 2 5 [1, 0, 17, 0, 0, 2]
    r5 += 2
    # 18	mulr 5 5 5
    # ip=18 [1, 0, 18, 0, 0, 2] mulr 5 5 5 [1, 0, 18, 0, 0, 4]
    r5 = r5 * r5
    # 19	mulr 2 5 5
    # ip=19 [1, 0, 19, 0, 0, 4] mulr 2 5 5 [1, 0, 19, 0, 0, 76]
    r5 = r5 * 19
    # 20	muli 5 11 5      
    # ip=20 [1, 0, 20, 0, 0, 76] muli 5 11 5 [1, 0, 20, 0, 0, 836]
    r5 = r5 * 11
    # 21	addi 3 4 3
    # ip=21 [1, 0, 21, 0, 0, 836] addi 3 4 3 [1, 0, 21, 4, 0, 836]
    r3 += 4
    # ip=22 [1, 0, 22, 4, 0, 836] mulr 3 2 3 [1, 0, 22, 88, 0, 836]
    # 22	mulr 3 2 3
    r3 = r3 * 22
    # 23	addi 3 7 3
    # ip=23 [1, 0, 23, 88, 0, 836] addi 3 7 3 [1, 0, 23, 95, 0, 836]
    r3 = r3 + 7
    # 24	addr 5 3 5
    # ip=24 [1, 0, 24, 95, 0, 836] addr 5 3 5 [1, 0, 24, 95, 0, 931]
    r5 = r5 + r3
    # ip=25 [1, 0, 25, 95, 0, 931] addr 2 0 2 [1, 0, 26, 95, 0, 931]

    # 25	addr 2 0 2
    # pc += 1
    # 26	seti 0 1 2
    # pc = 0

    # ip=27 [1, 0, 27, 95, 0, 931] setr 2 1 3 [1, 0, 27, 27, 0, 931]
    r3 = 27
    # ip=28 [1, 0, 28, 27, 0, 931] mulr 3 2 3 [1, 0, 28, 756, 0, 931]
    r3 = r3 * 28
    # ip=29 [1, 0, 29, 756, 0, 931] addr 2 3 3 [1, 0, 29, 785, 0, 931]
    r3 = r3 + 29
    # ip=30 [1, 0, 30, 785, 0, 931] mulr 2 3 3 [1, 0, 30, 23550, 0, 931]
    r3 = r3 * 30
    # ip=31 [1, 0, 31, 23550, 0, 931] muli 3 14 3 [1, 0, 31, 329700, 0, 931]
    r3 = r3 * 14
    # ip=32 [1, 0, 32, 329700, 0, 931] mulr 3 2 3 [1, 0, 32, 10550400, 0, 931]
    r3 = r3 * 32
    # ip=33 [1, 0, 33, 10550400, 0, 931] addr 5 3 5 [1, 0, 33, 10550400, 0, 10551331]
    r5 += r3
    # ip=34 [1, 0, 34, 10550400, 0, 10551331] seti 0 9 0 [0, 0, 34, 10550400, 0, 10551331]
    r0 = 0
    # ip=35 [0, 0, 35, 10550400, 0, 10551331] seti 0 8 2 [0, 0, 0, 10550400, 0, 10551331]
    r2 = 0
    return


# ip=0 [1, 0, 0, 0, 0, 0] addi 2 16 2 [1, 0, 16, 0, 0, 0]
sub17()
# expect 0 0 0 10550400 0 10551331
print r0, r1, r2, r3, r4, r5

# ip=1 [0, 0, 1, 10550400, 0, 10551331] seti 1 4 1 [0, 1, 1, 10550400, 0, 10551331]
r1 = 1
# ip=2 [0, 1, 2, 10550400, 0, 10551331] seti 1 2 4 [0, 1, 2, 10550400, 1, 10551331]
r4 = 1

def sub3():
  global r0, r1, r2, r3, r4, r5

  t = int(time.time())
  while True:
    # ip=3 [0, 1, 3, 10550400, 1, 10551331] mulr 1 4 3 [0, 1, 3, 1, 1, 10551331]
    r3 = r1 * r4
    # ip=4 [0, 1, 4, 1, 1, 10551331] eqrr 3 5 3 [0, 1, 4, 0, 1, 10551331]
    r3 = r3 == r5
    # ip=5 [0, 1, 5, 0, 1, 10551331] addr 3 2 2 [0, 1, 5, 0, 1, 10551331]
    # ip=6 [0, 1, 6, 0, 1, 10551331] addi 2 1 2 [0, 1, 7, 0, 1, 10551331]
    if r3:
      #     7	addr 1 0 0
      r0 = r1 + r0
      nt = int(time.time())
      print('loop: r0=%d, t=%d' % (r0, nt-t))
      t = nt
    # ip=8 [0, 1, 8, 0, 1, 10551331] addi 4 1 4 [0, 1, 8, 0, 2, 10551331]
    r4 = r4 + 1
    # ip=9 [0, 1, 9, 0, 2, 10551331] gtrr 4 5 3 [0, 1, 9, 0, 2, 10551331]
    r3 = r4 > r5
    # ip=10 [0, 1, 10, 0, 2, 10551331] addr 2 3 2 [0, 1, 10, 0, 2, 10551331]
    if r3:
      break
    # ip=11 [0, 1, 11, 0, 2, 10551331] seti 2 7 2 [0, 1, 2, 0, 2, 10551331]
    #print('ip=11 [%d, %d, %d, %d, %d, %d] seti 2 7 2 [%d, %d, %d, %d, %d, %d]' % (
    #    r0, r1, 11, r3, r4, r5, r0, r1, 2, r3, r4, r5))
    # continue

def sub3a():
  global r0, r1, r2, r3, r4, r5
  r3 = 0
  while True:
    # ip=3..11
    r0 += r1
    r4 = r5 + 1

    # ip=12 [8, 7, 12, 1, 932, 931] addi 1 1 1 [8, 8, 12, 1, 932, 931]
    r1 += 1
    # ip=13 [8, 8, 13, 1, 932, 931] gtrr 1 5 3 [8, 8, 13, 0, 932, 931]
    # ip=14 [8, 8, 14, 0, 932, 931] addr 3 2 2 [8, 8, 14, 0, 932, 931]
    # if r1 > r5, skip
    if r1 > r5:
      # 16	mulr 2 2 2
      return
    # ip=15 [8, 8, 15, 0, 932, 931] seti 1 0 2 [8, 8, 1, 0, 932, 931]
    r4 = 1
    print('ip=2+ [%d, %d, %d, %d, %d, %d] seti 2 7 2 [%d, %d, %d, %d, %d, %d]' % (
        r0, r1, 11, r3, r4, r5, r0, r1, 2, r3, r4, r5))


sub3a()

print('halt')
print r0, r1, r2, r3, r4, r5

