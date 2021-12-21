#!/usr/bin/env python3
"AOC 2021: day 21"

from collections import defaultdict
import copy
import sys

from tools import aoc

roll_probs = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


class Player(object):

  def __init__(self, player, start):
    self.player = player
    self.pos = start
    self.score = 0
    self.pos_to_universes = {start: 1}
    self.pos_to_scores = {}
    for i in range(1, 11):
      # self.pos_to_scores[i] = [0] * 30
      self.pos_to_scores[i] = defaultdict(int)
    self.pos_to_scores[start][0] = 1

  def __str__(self):
    return 'player %d: space %d, score %d' % (self.player, self.pos, self.score)

  def move(self, n):
    self.pos = (self.pos - 1 + n) % 10 + 1
    self.score += self.pos


class day21(aoc.aoc):

  def __init__(self):
    super(day21, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    x = self.all_input[0].split(',')
    self.p1 = Player(1, int(x[0]))
    self.p2 = Player(2, int(x[1]))

  def part1(self):
    print('===== Start part 1')
    self.reset()

    dice = 0
    nrolls = 0
    while True:
      r, dice = roll(dice)
      nrolls += 1
      self.p1.move(r)
      if self.trace_sample and nrolls < 6:
        print('player 1 rolls', r, 'moves to', self.p1.pos, 'score', self.p1.score)

      if self.p1.score >= 1000:
        break
      r, dice = roll(dice)
      nrolls += 1
      self.p2.move(r)
      if self.trace_sample and nrolls < 6:
        print('player 2 rolls', r, 'moves to', self.p2.pos, 'score', self.p2.score)
      if self.p2.score >= 1000:
        break

    print('done')
    print(self.p1)
    print(self.p2)
    if self.p1.score < self.p2.score:
      return nrolls * 3 * self.p1.score
    return nrolls * 3 * self.p2.score


  def part2(self):
    print('===== Start part 2')
    self.reset()

    p1_wins = 0
    for i in range(3):
      self.turn2(self.p1)
      p_p2u(self.p1.pos_to_universes)
      p_p2s(self.p1.pos_to_scores)

      for s,n in self.p1.pos_to_scores.items():
        if s >= 21:
          print("p1 wins")
          p1_wins = n
          break
      self.turn2(self.p2)

      for s,n in self.p2.pos_to_scores.items():
        if s >= 21:
          print("p2 wins")
          p2_wins = n
          break

    if p1_wins:
      return p1_wins
    return p2_wins


  def turn2(self, player):

    p_to_u = copy.deepcopy(player.pos_to_universes)
    p_to_s = {}
    for i in range(1, 11):
      p_to_s[i] = defaultdict(int)

    for o_pos in player.pos_to_universes:
      for r, times in roll_probs.items():
        n_pos = (o_pos - 1 + r) % 10 + 1
        n_univ = times * player.pos_to_universes[o_pos]

        if n_pos in p_to_u:
          p_to_u[n_pos] *= n_univ
        else:
          p_to_u[n_pos] = n_univ

        # for each old position, how many different scores got us there
        for pos, scores in player.pos_to_scores.items():
          for score, count in scores.items():
            n_score = score + n_pos
            p_to_s[n_pos][n_score] = score * n_univ

    player.pos_to_universes = p_to_u
    player.pos_to_scores = p_to_s


def p_p2u(p_to_u):
  print('positions', ',   '.join(['%2d: %d' % (p, p_to_u[p]) for p in sorted(p_to_u)]))
  tot = sum(p_to_u.values())
  n = 27
  for i in range(6):
    if n == tot:
      print('   n_univ = 27 ^', i)
      break
    if n > tot:
      print('FAIL:   n_univ >= 27 ^', i)
      break
    n *= 27
 

def p_p2s(p_to_s):
  for p in sorted(p_to_s):
    print('  scores@', p, ', '.join(['%2d:%d' % (s, p_to_s[p][s]) for s in sorted(p_to_s[p])]))


def roll(dice):
  # internal is 0-99, return +1 of each
  roll = dice % 100 + (dice + 1) % 100 + (dice + 2) % 100 + 3
  return roll, (dice + 3) % 100


def check_roll(start, expect_roll, expect_new):
  r, n = roll(start)
  fail = False
  if expect_roll != r:
    print('FAIL: on', start, 'expected roll', expect_roll, 'got', r)
    fail = True
  if expect_new != n:
    print('FAIL: on', start, 'expected roll', expect_new, 'got', n)
    fail = True
  if fail:
    sys.exit(1)

check_roll(0, 6, 3)
check_roll(3, 15, 6)
check_roll(98, 200, 1)
check_roll(99, 103, 2)


day21.sample_test("""
4,8
""", expect1=739785, expect2=444356092776315)


if __name__ == '__main__':
  day21.run_and_check('input.txt', expect1=None, expect2=None)
