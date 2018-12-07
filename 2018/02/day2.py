"""
For example, if you see the following box IDs:

abcdef contains no letters that appear exactly two or three times.
bababc contains two a and three b, so it counts for both.
abbcde contains two b, but no letter appears exactly three times.
abcccd contains three c, but no letter appears exactly two times.
aabcdd contains two a and two d, but it only counts once.
abcdee contains two e.
ababab contains three a and three b, but it only counts once.

Of these box IDs, four of them contain a letter which appears exactly twice, and three of them contain a letter which appears exactly three times. Multiplying these together produces a checksum of 4 * 3 = 12.

What is the checksum for your list of box IDs?
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import sys

def freqs(id):
  freqs = collections.defaultdict(int)
  for c in id:
    freqs[c] += 1
  res = {}
  for char, count in freqs.iteritems():
    res[count] = char
  return res

def part1(inp):
  n_2 = 0
  n_3 = 0
  for id in inp:
    f = freqs(id.strip())
    # print('%s => %s' % (id, f))
    if 2 in f:
      n_2 += 1
    if 3 in f:
      n_3 += 1
  print('checksum = %d\n' % (n_2 * n_3))


"""
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
"""
def part2(inp):
  ids = []
  for id in inp:
    ids.append(id.strip())
  ids = sorted(ids)
  last = '                                          '
  for id in ids:
    diff = 0
    for i in range(len(id)):
      if last[i] != id[i]:
        if diff == 1:
          diff = 2
          break
        diff = 1
    if diff == 1:
      comm = ''
      for i in range(len(id)):
        if last[i] == id[i]:
          comm += id[i]
      print('%s\n%s\n%s\n' % (last, id, comm))
      return
    last = id

if __name__ == '__main__':
  with open(sys.argv[1]) as inp:
    part2(inp)
