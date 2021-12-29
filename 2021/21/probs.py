

from collections import defaultdict
import itertools

probs = defaultdict(int)
for x,y,z in itertools.product(range(1, 4), range(1,4), range(1,4)):
  print('sum', x+y+z, x, y, z)
  probs[x+y+z] += 1
  
for i in range(1,10):
  print('%d: %d' % (i, probs[i]))


print()
targ = 444356092776315 + 341960390180808

def dopow(m):
  i = 0
  x = 1
  s = 0
  p2i = {}
  for i in range(50):
    print('%d^%2d' % (m, i), '=', '%20d' % x, '%20d' % s, '%20d' % (targ - x))
    p2i[x] = i
    if x == targ:
      print("targ")
    if x > targ:
      break
    ii = p2i.get(targ - x)
    if ii:
      print(x, '+', p2i[ii], ii, '=', targ)
    x *= m
    s += x
  print('target:', targ)

dopow(3)
# dopow(4)

