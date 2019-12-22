#!/usr/bin/env python3


class Deck(object):

  def __init__(self, size=10007):
    self.size = size
    self.deck = [d for d in range(size)]

  def deal_new_stack(self):
    d = [0] * self.size
    for i in range(self.size):
      d[self.size-1-i] = self.deck[i]
    self.deck = d

  def deal_with_inc(self, inc):
    d = [0] * self.size
    ptr = 0
    loop = 0
    for i in range(self.size):
      d[ptr] = self.deck[i]
      if ptr == 2020:
        print('Filling 2020 at loop', loop)
      if ptr + inc > self.size:
        loop += 1
      ptr = (ptr + inc) % self.size
    self.deck = d

  def cut(self, cut):
    if cut < 0:
      cut = self.size + cut
    self.deck = self.deck[cut:] + self.deck[0:cut]

  def do(self, cmd):
    if cmd == 'deal into new stack':
      self.deal_new_stack()
    elif cmd.startswith('deal with increment'):
      inc = int(cmd[19:])
      self.deal_with_inc(inc)
    elif cmd.startswith('cut '):
      cut = int(cmd[4:])
      self.cut(cut)
    else:
      raise ValueError('Bad command "%s"' % cmd)
    if self.size > 10:
      print('%-30.30s: d[2020]=%d' % (cmd, self.deck[2020]))


 
def test1():
  deck = Deck(10)
  deck.do('deal with increment 7')
  deck.do('deal into new stack')
  deck.do('deal into new stack')
  # print(deck.deck)
  assert [0, 3, 6, 9, 2, 5, 8, 1, 4, 7] == deck.deck

  deck = Deck(10)
  deck.do('cut 6')
  deck.do('deal with increment 7')
  deck.do('deal into new stack')
  # print(deck.deck)
  assert [3, 0, 7, 4, 1, 8, 5, 2, 9, 6] == deck.deck

  deck = Deck(10)
  deck.do('deal with increment 7')
  deck.do('deal with increment 9')
  deck.do('cut -2')
  # print(deck.deck)
  assert [6, 3, 0, 7, 4, 1, 8, 5, 2, 9] == deck.deck
  #Result: 6 3 0 7 4 1 8 5 2 9

  deck = Deck(10)
  deck.do('deal into new stack')
  deck.do('cut -2')
  deck.do('deal with increment 7')
  deck.do('cut 8')
  deck.do('cut -4')
  deck.do('deal with increment 7')
  deck.do('cut 3')
  deck.do('deal with increment 9')
  deck.do('deal with increment 3')
  deck.do('cut -1')
  # print(deck.deck)
  # Result: 9 2 5 8 1 4 7 0 3 6
  assert [9, 2, 5, 8, 1, 4, 7, 0, 3, 6] == deck.deck


def part1():
  deck = Deck()
  with open('input_22.txt', 'r') as inp:
    for line in inp:
      deck.do(line.strip())
  for pos,v in enumerate(deck.deck):
    if v == 2019:
      print('part1: pos', pos)

test1()
part1()

class VDeck(object):

  def __init__(self, follow_pos=2019, size=10007, target_slot=0):
    self.size = size
    self.follow_pos = follow_pos
    self.target_slot = target_slot
    self.sum_cut = 0
    self.prod_shuffle = 1
    self.sum_shuffle = 0

  def deal_new_stack(self):
    self.prod_shuffle *= -1
    self.follow_pos = self.size - self.follow_pos - 1

  def deal_with_inc(self, inc):
    self.prod_shuffle *= inc
    self.sum_shuffle += inc
    # 0123456789  for 7
    # 0469368157
    """
    ptr = 0
    for i in range(self.follow_pos):
      # print('%d to %d' % (i, ptr))
      ptr = (ptr + inc) % self.size
    # print('X %d to %d' % (self.follow_pos, ptr))
    self.follow_pos = ptr
    """
    self.follow_pos = (inc * self.follow_pos) % self.size

  def cut(self, cut):
    if cut < 0:
      cut = self.size + cut
      self.sum_cut += cut
      if cut == self.follow_pos:
        self.follow_pos = 0
        return
    #   c  t 
    # 0123t45c79   679012345
    self.sum_cut += cut
    if cut < self.follow_pos:
      self.follow_pos -= cut
    else:
      # cut >= self.follow_pos:
      # 012t456c89 -> 789012t456
      self.follow_pos += (self.size - cut)

  def do(self, cmd):
    if cmd == 'deal into new stack':
      self.deal_new_stack()
    elif cmd.startswith('deal with increment'):
      inc = int(cmd[19:])
      self.deal_with_inc(inc)
    elif cmd.startswith('cut '):
      cut = int(cmd[4:])
      self.cut(cut)
    else:
      raise ValueError('Bad command "%s"' % cmd)


def test_part2():
  deck = VDeck(size=10, follow_pos=9, target_slot=6)
  deck.do('deal with increment 7')
  deck.do('deal into new stack')
  deck.do('deal into new stack')
  # print(deck.follow_pos)
  print('target_slot', deck.target_slot, 'expect 8')
  assert 3 == deck.follow_pos
  # assert [0, 3, 6, 9, 2, 5, 8, 1, 4, 7] == deck.deck

  deck = VDeck(size=10, follow_pos=9)
  deck.do('cut 6')  # 6789012345
  deck.do('deal with increment 7')  # 6.9.8..7..
  deck.do('deal into new stack')    # .......9.6 
  # print(deck.follow_pos)
  # print(deck.deck)
  assert 8 == deck.follow_pos
  # assert [3, 0, 7, 4, 1, 8, 5, 2, 9, 6] == deck.deck

  deck = VDeck(size=10, follow_pos=9)
  deck.do('deal with increment 7')
  deck.do('deal with increment 9')
  deck.do('cut -2')
  # print(deck.deck)
  # print(deck.follow_pos)
  assert 9 == deck.follow_pos
  # assert [6, 3, 0, 7, 4, 1, 8, 5, 2, 9] == deck.follow_pos
  #Result: 6 3 0 7 4 1 8 5 2 9

  deck = VDeck(size=10, follow_pos=9)
  deck.do('deal into new stack')
  deck.do('cut -2')
  deck.do('deal with increment 7')
  deck.do('cut 8')
  deck.do('cut -4')
  deck.do('deal with increment 7')
  deck.do('cut 3')
  deck.do('deal with increment 9')
  deck.do('deal with increment 3')
  deck.do('cut -1')
  # print(deck.follow_pos)
  # print(deck.deck)
  # Result: 9 2 5 8 1 4 7 0 3 6
  assert 0 == deck.follow_pos

  deck = VDeck(follow_pos=2019, size=10007)
  with open('input_22.txt', 'r') as inp:
    for line in inp:
      deck.do(line.strip())

  print('part1: pos', deck.follow_pos)
  assert 5472 == deck.follow_pos


def part2():
  deck = VDeck(size=119315717514047, follow_pos=2020)

  # and repeat this 101741582076661 times
  cmds = []
  with open('input_22.txt', 'r') as inp:
    for line in inp:
      cmds.append(line.strip())
      deck.do(line.strip())

  print('sumcut', deck.sum_cut)
  print('prod_shuffle', deck.prod_shuffle)
  print('sum_shuffle', deck.sum_shuffle)

  shift = deck.follow_pos - 2020
  print('part2x: shift', shift)
  pos = (2020 + shift * 101741582076661) % 119315717514047
  # too low: 56016606208231
  print('part2: pos', pos)
  assert 56016606210251 == pos

  for i in range(2, 101741582076661):
    for cmd in cmds:
      deck.do(cmd)
    if deck.follow_pos == 2020:
      print('loop at', i)
      break
   


test_part2()
part2()
