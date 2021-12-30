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

pow27 = [27 ** n for n in range(25)]
what_pow_27 = {27 ** n:n for n in range(25)}
what_pow_7 = {7 ** n:n for n in range(25)}
# print(pow27)

class Player(object):

  def __init__(self, player, start):
    self.player = player
    self.odd = (player % 2) == 1
    self.pos = start
    self.score = 0
    # for part2
    self.won = 0
    self.wins = 0
    self.h = {0: (self.pos, 0)}

  def __str__(self):
    return 'player %d: space %d, score %d' % (self.player, self.pos, self.score)

  def move(self, n):
    self.pos = (self.pos - 1 + n) % 10 + 1
    self.score += self.pos

  def would_win(self, rolls, hist):
    prev = hist // 10
    cur_roll = hist - prev * 10
    # print('odd, prev', self.odd, prev)
    pos, score = self.h[prev]
    pos = (pos - 1 + cur_roll) % 10 + 1
    score += pos
    if score >= 21:
      return True
    # print("h", hist, '=', pos, score)
    self.h[hist] = (pos, score)
    return False


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

    # roll history to # universes
    self.rolls2u = {}

    self.rolls2u[0] = (1, 0, 0)
    for i in range(25):
      self.playerturn(self.p1)
      # self.pr2u()
      self.pstate(i, self.p1)
      if len(self.rolls2u) == 0:
        break
      self.playerturn(self.p2)
      self.pstate(i, self.p2)
      if len(self.rolls2u) == 0:
        break

    if self.p1.won > self.p2.won:
      return self.p1.won
    return self.p2.won

  def pstate(self, round, player):
      n_u = len(self.rolls2u)
      tot_win = self.p1.wins + self.p2.wins
      p7 = what_pow_7.get(n_u + tot_win) or '?'
      print(', '.join([
        '= after round %d' % round,
        'player %d' % player.player,
        'n_rolls:%d' % n_u,
        'rolls+wins:%d = 7^%s' % (n_u+tot_win, p7)]))

  def playerturn(self, player):
    nxt = {}
    n_wins = 0
    for roll in range(3, 10):
      roll_times = roll_probs[roll]
      for rolls, parts in self.rolls2u.items():
        n_univ, p1, p2  = parts
        new_n_univ = n_univ * roll_times
        n_rolls = rolls * 10 + roll 
        # print('nrolls', n_rolls)
        if player.odd:
          p1 = p1*10+roll
          hist = p1
        else:
          p2 = p2*10+roll
          hist = p2
        # print('   -> hist', n_rolls, p1, p2)
        if player.would_win(n_rolls, hist):
          player.won += new_n_univ
          n_wins += 1
        else:
          nxt[n_rolls] = (new_n_univ, p1, p2)
    self.rolls2u = nxt
    player.wins += n_wins
    if n_wins:
      print(' -> player', player.player, 'won:', n_wins, 'tot:', player.won)


  def pr2u(self):
    tot = 0
    for rolls in sorted(self.rolls2u):
      print(rolls, self.rolls2u[rolls])
      tot += self.rolls2u[rolls]
    p = what_pow_27.get(tot) or '???'
    print('  tot:', tot, ', 27^%s' % p)


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
  day21.run_and_check('input.txt', expect1=802452, expect2=270005289024391)
