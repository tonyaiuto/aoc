#!/usr/bin/env python3
"AOC 2023: day 04"

import heapq

from tools import aoc


def s2l(s):
  for x in s.split(' '):
    if x.strip():
      yield int(x)


class Card(object):

  def __init__(self, line):
    x = line.strip().split(':')
    self.numb = int((x[0][5:].strip()))
    y = x[1].split('|')
    self.win = list(s2l(y[0]))
    self.have = list(s2l(y[1]))
    # print(self.numb, self.win, self.have)
    win = set(self.win)
    self.score = 0
    self.match = 0
    self.count = 1
    for h in self.have:
      if h in win:
        self.match += 1
        if self.score == 0:
          self.score = 1
        else:
          self.score = self.score * 2

  def __str__(self):
    return str(self)


class day04(aoc.aoc):

  def __init__(self):
    super(day04, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.cards = []
    self.cardi = []

  def do_line(self, line):
    # called for each line of input
    c = Card(line.strip())
    heapq.heappush(self.cardi, c.numb)
    self.cards.append(c)

  def part1(self):
    print('===== Start part 1')
    tot_score = 0
    for c in self.cards:
      tot_score += c.score
    print(tot_score)
    return tot_score


  def part2_slow(self):
    print('===== Start part 2')
    tot_cards = 0
    while True:
      try:
        ic = heapq.heappop(self.cardi)
      except IndexError:
        break
      tot_cards += 1
      c = self.cards[ic-1]
      # print('card', c.numb, 'match', c.match)
      for wc in range(c.match):
        # print('push', c.numb + 1 + wc)
        heapq.heappush(self.cardi, c.numb + 1 + wc)
    return tot_cards

  def part2(self):
    print('===== Start part 2')
    tot_cards = 0
    for card in self.cards:
      tot_cards += card.count
      # print('do card', card.numb, 'match', card.match, 'count', card.count, 'tot', tot_cards)
      for wc in range(card.match):
        oc = card.numb + 1 + wc
        self.cards[oc-1].count += card.count
        # print('     card', oc, self.cards[oc-1].count)
    #for card in self.cards:
    #  print('final card', card.numb, card.match, card.count)
    return tot_cards


day04.sample_test("""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""", expect1=13, expect2=30)


if __name__ == '__main__':
  day04.run_and_check('input.txt', expect1=19855, expect2=10378710)
