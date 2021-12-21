

from collections import defaultdict
import itertools

probs = defaultdict(int)
for x,y,z in itertools.product(range(1, 4), range(1,4), range(1,4)):
  print('sum', x+y+z, x, y, z)
  probs[x+y+z] += 1
  
for i in range(1,10):
  print('%d: %d' % (i, probs[i]))
