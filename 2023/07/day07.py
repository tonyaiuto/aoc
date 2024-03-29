#!/usr/bin/env python3
"AOC 2023: day 07"

from collections import defaultdict
from operator import attrgetter

from tools import aoc

FIVE = 50
FOUR = 40
FULL = 32
THREE = 30
TWO_PAIRS = 20
PAIR = 11
CARD = 10

CARDS  = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_VAL = {CARDS[ic]: len(CARDS) - ic for ic in range(len(CARDS))}
JCARDS = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
JCARD_VAL = {JCARDS[ic]: len(JCARDS) - ic for ic in range(len(JCARDS))}


class Hand(object):

  def __init__(self, cards, bid):
    self.cards = cards.strip()
    self.bid = int(bid)
    self.type = CARD
    self.type2 = CARD
    self._set_type()
    self.score = self.type
    self.jscore = self.type2
    for c in self.cards:
      self.score = self.score * 100 + CARD_VAL[c]
      self.jscore = self.jscore * 100 + JCARD_VAL[c]


  def _set_typex(self):
    tmp = defaultdict(int)
    for c in self.cards:
      tmp[c] += 1
      if tmp[c] == 3:
        self.type = THREE
      elif tmp[c] == 4:
        self.type = FOUR
      elif tmp[c] == 5:
        self.type = FIVE

    n_pairs = 0
    n_j = tmp.get('J') or 0
    for c in tmp:
      if tmp[c] == 2:
        n_pairs += 1
    self.n_pairs = n_pairs
    self.n_j = n_j

  def _set_type(self):
    tmp = defaultdict(int)
    for c in self.cards:
      tmp[c] += 1
      if tmp[c] == 3:
        self.type = THREE
      elif tmp[c] == 4:
        self.type = FOUR
      elif tmp[c] == 5:
        self.type = FIVE

    n_pairs = 0
    self.n_j = tmp.get('J') or 0
    for c in tmp:
      if tmp[c] == 2:
        n_pairs += 1
    self.n_pairs = n_pairs

    self.type2 = self.type
    if self.type == FIVE:
      return

    if self.type == FOUR:
      if self.n_j > 0:
        assert self.n_j == 1 or self.n_j == 4
        self.type2 = FIVE
      return

    assert self.n_j <= 3

    if self.type == THREE:
      if n_pairs == 1:
        self.type = FULL
        self.type2 = FULL
        assert self.n_j != 1

      if self.n_j == 1:
        self.type2 = FOUR
      if self.n_j == 2:
        self.type2 = FIVE
      if self.n_j == 3:
        self.type2 = FOUR
      if self.n_j == 3 and n_pairs == 1:
        self.type2 = FIVE

      #if self.type != self.type2:
      #  print('jboost', self.cards, self.type, self.type2, n_pairs, n_j)
      return

    if n_pairs == 2:
      self.type = TWO_PAIRS
      self.type2 = TWO_PAIRS
      if self.n_j == 1:
        self.type2 = FULL
      if self.n_j == 2:
        self.type2 = FOUR
      return

    if n_pairs == 1:
      self.type = PAIR
      self.type2 = PAIR
      if self.n_j == 1 or self.n_j == 2:
        self.type2 = THREE
      return

    if self.n_j == 1:
      self.type2 = PAIR


  def __str__(self):
    return '%s %2d' % (self.cards, self.type)
    # , '%10d' % self.score, self.bid)

  def __eq__(self, other):
    return self.cards == other.cards

  def __lt__(self, other):
    if self.type < other.type:
      return True
    if self.type > other.type:
      return False
    return self.score < other.score

  @staticmethod
  def key2(a):
    return a.type2 * 100000000000 + a.jscore


class day07(aoc.aoc):

  def __init__(self):
    super(day07, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.hands = []

  def do_line(self, line):
    # called for each line of input
    ls = line.strip().split(' ')
    hand = Hand(ls[0], ls[1])
    # print(hand.cards, "%2d" % hand.type, '%10d' % hand.score, hand.bid)
    self.hands.append(hand)

  def part1(self):
    print('===== Start part 1')
    self.ranked = sorted(self.hands)
    rank = 0
    ret = 0
    for hand in self.ranked:
      rank += 1
      ret += rank * hand.bid
    print('part1:', ret)
    return ret

  def part2(self):
    print('===== Start part 2')
    ranked = sorted(self.hands, key=Hand.key2)
    # ranked = sorted(self.hands, key=attrgetter('type2', 'jscore'))
    otype = 0
    rprev = None
    for r in ranked:
      wrong = False
      if r.n_j > 0 and r.type2 == CARD:
        wrong = False
      if r.n_j > 1 and r.type2 < THREE:
        wrong = False
      if r.n_j > 2 and r.type2 < FOUR:
        wrong = False
      if r.n_j == 4 and r.type2 != FIVE:
        wrong = False
      if r.n_j > 0 and r.type2 == FULL:
        wrong = False
      if wrong:
        print('wrong', r.cards, r.type2, r.n_pairs, r.n_j, '%012d' % r.jscore)
      """
      if otype != r.type2 or (rprev and rprev.n_j != r.n_j):
        if rprev:
          print('  ', rprev.cards, rprev.type2, rprev.n_pairs, rprev.n_j, '%012d' % rprev.jscore)
        print('>>', r.cards, r.type2, r.n_pairs, r.n_j, '%012d' % r.jscore)
      """
      otype = r.type2
      rprev = r
    nc = len(ranked)
    for i in range(nc):
      if nc < 10 or i % 50 == 0:
        r = ranked[i]
        print(r.cards, r.type2, r.n_pairs, r.n_j, '%012d' % r.jscore)

    rank = 0
    ret = 0
    for hand in ranked:
      rank += 1
      ret += rank * hand.bid
    print('part2:', ret)
    if ret >= 244873831:
      print('TOO HIGH')
    return ret


day07.sample_test("""
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""", expect1=6440, expect2=5905)


"""
244848487
244873831 too high
244878375 too high
244879828
244891298
244879828
245230961
245280802
"""

if __name__ == '__main__':
  day07.run_and_check('input.txt', expect1=246409899, expect2=244848487)
