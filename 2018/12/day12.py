"""aoc 2018 day 12"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys

"""
What is the sum of all metadata entries?
"""

class Rule(object):

  def __init__(this, pattern, result):
    this.pattern = pattern
    this.result = result

  def __str__(this):
    return '%s => %s' % (['#' if x else '.' for x in this.pattern],
                         '#' if this.result else '.')

class Rules(object):

  def __init__(this):
    this.patterns = []
    this.results = []

  def __str__(this):
    r = []
    for i in range(len(this.patterns)):
      r.append('%s => %s' % (this.patterns[i], this.results[i]))
    return '\n'.join(sorted(r))

  def ParseAndAdd(this, text):
    # '#.#.# => .'
    #pattern = [False] * 5
    #for i in range(5):
    #  if text[i] == '#':
    #    pattern[i] = True

    this.patterns.append(text[0:5])
    this.results.append(text[9])
 

def LoadAll(inp):
  rules = Rules()

  state = None
  for line in inp:
    line = line.strip()
    if line.startswith('initial state:'):
      state = line[15:]
      continue
    if len(line) == 10:
      rules.ParseAndAdd(line)
  return rules, state

if __name__ == '__main__':
  verbose = False
  iarg = 1
  if sys.argv[iarg] == '-v':
    verbose = True
    iarg += 1
  with open(sys.argv[iarg]) as inp:
    rules, state = LoadAll(inp)
  print(rules)
  print(state)
