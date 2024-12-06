#!/usr/bin/python3

import sys

f = open('m2', 'r')
inp = f.read()
f.close

ret = 0
for line in inp.split('\n'):
  if not line:
    continue
  if not line.startswith('mul('):
    print("FAIL", line)
    sys.exit(1)
  if line[-1] != ')':
    print("FAIL", line)
    sys.exit(1)

  # print(line)
  pairs = line[4:-1].split(',')
  try:
    ret += int(pairs[0]) * int(pairs[1])
  except ValueError:
    pass

print(ret)
