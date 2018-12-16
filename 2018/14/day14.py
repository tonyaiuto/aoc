"""aoc 2018 day 13"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys

class Recipes(object):

  def __init__(this, start):
    this.scores = []
    for c in start:
      this.scores.append(ord(c) - ord('0'))
    this.elf1 = 0
    this.elf2 = 1

  def __str__(this):
    out = []
    for i in range(len(this.scores)):
      v = this.scores[i]
      if i == this.elf1:
        out.append('(%d)' % v)
      elif i == this.elf2:
        out.append('[%d]' % v)
      else:
        out.append(str(v))
    return(' '.join(out))

  def MoveElf(this, elf_pos):
    return (elf_pos + 1 + this.scores[elf_pos]) % len(this.scores)

  def Turn(this):
    combined = this.scores[this.elf1] + this.scores[this.elf2]
    if combined >= 10:
      this.scores.append(1)
      combined -= 10
    this.scores.append(combined)
    this.elf1 = this.MoveElf(this.elf1)
    this.elf2 = this.MoveElf(this.elf2)

  def Last10(this):
    l = len(this.scores) - 10
    return ''.join([str(d) for d in this.scores[l:]])
    

def part1(recipes, end):
  for i in range(end+11):
    if i < 30:
      print(recipes)
    n_recipes = len(recipes.scores) - 10
    if n_recipes == 5:
      print('5: %s' % recipes.Last10())
    if n_recipes == 18:
      print('18: %s' % recipes.Last10())
    if n_recipes == 2018:
      print('2018: %s' % recipes.Last10())
    if n_recipes == end:
      print('%d: %s' % (end, recipes.Last10()))
    recipes.Turn()


def part2(recipes, target_s):
  target = []
  for c in target_s:
    target.append(ord(c) - ord('0'))
  lt = len(target)
  while True:
    recipes.Turn()
    if recipes.scores[-(lt+1):-1] == target:
      print('%s appears after %d' % (target_s, len(recipes.scores) - lt - 1))
      break
    if recipes.scores[-lt:] == target:
      print('%s appears after %d' % (target_s, len(recipes.scores) - lt))
      break

if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      do_part2 = True
      iarg += 1
  start = sys.argv[iarg]
  end = sys.argv[iarg+1]
  r = Recipes(start)
  if do_part2:
    part2(r, end)
  else:
    part1(r, int(end))
