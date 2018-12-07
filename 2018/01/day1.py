from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

def sum(inp):
  sum = 0
  for x in inp:
    sum += int(x.strip())
  return sum

def calibrate(inp):
  sum = 0
  freqs = {}
  while True:
    inp.seek(0)
    for x in inp:
      sum += int(x.strip())
      if sum in freqs:
        print('%d appears twice' % sum)
        return
      freqs[sum] = True

if __name__ == '__main__':
  with open(sys.argv[1]) as inp:
    print('Sum: %d' % sum(inp))
    calibrate(inp)
