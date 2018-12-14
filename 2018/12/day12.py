"""aoc 2018 day 12"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import sys
import time

_WSIZE = 5

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
    #pattern = [False] * _WSIZE
    #for i in range(_WSIZE):
    #  if text[i] == '#':
    #    pattern[i] = True

    this.patterns.append(text[0:_WSIZE])
    this.results.append(text[9])
 

class Game(object):

  def __init__(this, rules, state):
    this.rules = rules
    this.state = state
    this.gen = 0
    this.zero = 0
    this.start_time = time.time()

  def PrintState(this, out):
    out.write('=gen:%d, time: %d\n' % (this.gen, int(time.time() - this.start_time)))
    out.write('%3d: %3d ' % (this.gen, this.zero))
    out.write(this.state)
    out.write('\n')


  def Gen(this):
    this.gen += 1
    w = ['.'] * _WSIZE  # window
    w[3:_WSIZE] = this.state[0:2]
    used = 2  # two chars from state are in window
    n_state = ''
    pos = 0

    # does window match pattern
    def _match(p, pos):
      for i in range(_WSIZE):
        if p[i] != w[(pos + i) % _WSIZE]:
          return False
      return True

    emitted = 0
    while used < len(this.state) + 4:
      # find matching rule and emit result
      matched = False
      for ri in range(len(this.rules.patterns)):
        if _match(this.rules.patterns[ri], pos):
          # print('match at %d %s => %s' % (pos, this.rules.patterns[ri], n_state))
          n_state += this.rules.results[ri]
          matched = True
          break
      if not matched:
        n_state += '.'
      emitted += 1

      # slide window and input
      try:
        w[pos % _WSIZE] = this.state[used]
      except:
        # print('used = %d, emitted=%d' % (used, emitted))
        w[pos % _WSIZE] = '.'
      used += 1
      pos += 1
      assert emitted == pos

    #print('window = %s' % ''.join(
    #    [w[(pos + p) % _WSIZE] for p in range(_WSIZE)]))
    #print('out:%d, in:%d' % (len(n_state), len(this.state)))
    assert len(n_state) == emitted
    assert emitted == len(this.state) + 2
    # assert 
    left = 1
    if n_state[0] == '#':
      left = 0
      this.zero += 1
    right = len(n_state)
    if n_state[right-1] == '.':
      right -= 1
    # print('new=%s' % n_state)
    this.state = n_state[left:right]

  def SumPotted(this):
    vs = []
    sum = 0
    for i in range(len(this.state)):
      v = i - this.zero
      if this.state[i] == '#':
        vs.append(str(v))
        sum += v
      else:
        vs.append('-')
    print(vs)
    print('Sum Potted: %d' % sum)


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


def part1(game):
  game.PrintState(sys.stdout)
  for i in range(20):
    game.Gen()
    game.PrintState(sys.stdout)
  game.SumPotted()


def part2(game, target_gen):
  game.PrintState(sys.stdout)
  for i in range(3000):
    glide_right = '.' + game.state
    game.Gen()
    if glide_right == game.state:
      print('Glider!')
      game.PrintState(sys.stdout)
      break
  game.SumPotted()

  vs = []
  sum = 0
  more_gens = target_gen - game.gen
  for i in range(len(game.state)):
    v = more_gens + i - game.zero
    if game.state[i] == '#':
      vs.append(str(v))
      sum += v
    else:
      vs.append('-')
  print(vs)
  print('Sum Potted: %d' % sum)


if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-2':
      do_part2 = True
      iarg += 1
    elif sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    else:
      break
  with open(sys.argv[iarg]) as inp:
    rules, state = LoadAll(inp)
  if verbose:
    print(rules)
    print(state)
  game = Game(rules, state)
  part1(game)
  if do_part2:
    part2(game, 50000000000)
