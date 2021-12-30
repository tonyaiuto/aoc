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
    self.pos_to_scores = {}
    for i in range(1, 11):
      self.pos_to_scores[i] = defaultdict(int)
    self.pos_to_scores[start][0] = 1
    self.won = 0
    self.h = {0: (self.pos, 0)}
    self.wins = 0

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
    self.h[prev*10+cur_roll] = (pos, score)
    # print("h", prev*10+cur_roll, '=', pos, score)
    if score >= 21:
      return True
    return False

  def would_winO(self, rolls, odd):
    return False
    roll_i = [int(c) for c in str(rolls)]
    prev = 0
    for r in roll_i[0 if odd else 1:-1:2]:
      prev = prev * 10 + r
    cur_roll = roll_i[-1]
    # print("would_win", roll_i, prev, cur_roll)
    pos, score = self.h[prev]

    pos = (pos - 1 + cur_roll) % 10 + 1
    score += pos
    self.h[prev*10+cur_roll] = (pos, score)
    # print("h", prev*10+cur_roll, '=', pos, score)
    if score >= 21:
       return True
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

    # roll history to # universes
    self.rolls2u = {}
    self.forp = {}

    # First turn initializes things
    if len(self.rolls2u) == 0:
      for roll in range(3, 10):
        self.rolls2u[roll] = roll_probs[roll]
        # print('init forp', roll)
        self.forp[roll] = (roll, 0)
        _ = self.p1.would_win(roll, roll)
    print('= after setup', 'player 1, n_rolls:', len(self.rolls2u))

    for i in range(5):
      self.playerturn(self.p2)
      self.pstate(i, self.p2)
      if len(self.rolls2u) == 0:
        break
      self.playerturn(self.p1)
      self.pstate(i, self.p1)
      # self.pr2u()
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
      for rolls, n_univ in self.rolls2u.items():
        new_n_univ = n_univ * roll_times
        (p1, p2) = self.forp[rolls]
        n_rolls = rolls * 10 + roll 
        # print('nrolls', n_rolls)
        if player.odd:
          self.forp[n_rolls] = (p1*10+roll, p2)
          hist = p1*10+roll
        else:
          self.forp[n_rolls] = (p1, p2*10+roll)
          hist = p2*10+roll
        # print('   -> forp', n_rolls, self.forp[n_rolls])
        if player.would_win(n_rolls, hist):
          player.won += new_n_univ
          n_wins += 1
        else:
          nxt[n_rolls] = new_n_univ
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


  def Xpart2(self):
    print('===== Start part 2')
    self.reset()

    p1_wins = 0
    p2_wins = 0
    p_p2s(self.p1.pos_to_scores)
    for i in range(9):
      print('== player 1 turn')
      # p_p2s(self.p1.pos_to_scores)
      # print('==== begin 2')
      self.turn2(self.p1, self.p2)
      p_p2s(self.p1.pos_to_scores)

      if self.p1.won > 444356092776315:
        print('  Gone to far at', self.p1.won)
        break
      print('== player 2 turn')
      self.turn2(self.p2, self.p1)
      p_p2s(self.p1.pos_to_scores)

    # assert i < 6

    if self.p1.won > self.p2.won:
      return self.p1.won
    return self.p2.won

    if p1_wins > p2_wins:
      return p1_wins
    return p2_wins

  def split(self, player, times=27):
    for pos, scores in player.pos_to_scores.items():
      for score in scores:
        scores[score] *= times

  def turn2(self, player, other):
    # position to # of universes at each score
    p_to_s = {}
    for i in range(1, 11):
      p_to_s[i] = defaultdict(int)

    still_playing = set()
    won_at = defaultdict(int)
    winnings = 0
    for roll in range(3, 10):
      roll_times = roll_probs[roll]
      nw = 0
      for o_pos in range(1, 11):
        n_pos = (o_pos - 1 + roll) % 10 + 1

        # from o_pos I will be at n_pos roll_times (out of 27)

        """
	If I was on pos N with and old score of S in U universes,
        and I am moving to position n_pos, roll_times times
        with a new score of score + n_pos
        then p2s[n_pos][new score] increases by U * roll_times
        # for each old position, how many different scores got us there
        """
        for score, n_univ in player.pos_to_scores[o_pos].items():
          # new score for the people at pos o_pos with prev_score score
          n_score = score + n_pos
          new_n_univ = n_univ * roll_times
          if n_score >= 21:
            player.won += new_n_univ
            won_at[n_score] += new_n_univ
            winnings += new_n_univ
            nw += 1
          else:
            p_to_s[n_pos][n_score] += new_n_univ
      if nw == 0:
        still_playing.add(roll)
      if nw > 0:
        print('   => won, roll:', roll,  '%2d' % nw, ','.join(['%d: %-6d' % (k, v) for k,v in won_at.items()]))

    player.pos_to_scores = p_to_s

    t = 0
    for p in p_to_s:
      scores = p_to_s[p]
      for score, n in scores.items():
        t += n
    # assert (t + player.won) in what_pow_27

    sp = sum([roll_probs[roll] for roll in still_playing])
    print('sp', sp)
    assert sp <= 27
    if winnings > 0:
      assert sp < 27

    # self.split(player, times=sp)
    if sp > 0:
      self.split(other, times=sp)


def p_p2s(p_to_s):
  tot = 0
  for p in sorted(p_to_s):
    scores = p_to_s[p]
    print('  scores@%-2d:' % p, ', '.join(['%2d:%6d' % (s, scores[s]) for s in sorted(scores)]))
    tot += sum(scores.values())
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
#                            44999274953475450
#                            50207674102141821327
#                            708329200200264
#                            822385675458


if __name__ == '__main__':
  day21.run_and_check('input.txt', expect1=None, expect2=None)
