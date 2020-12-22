"AOC 2020: day 22"

from collections import defaultdict

from tools import reader


def sample_test(s, expect, expect2=None):
  puzz = day22()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day22()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day22()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day22()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Player(object):

  def __init__(self, deck=None, clone=None, ncards=0):
    if deck:
      assert deck[0].startswith('Player ')
      self.n = int(deck[0][7])
      self.cards = [int(s.strip()) for s in deck[1:]]
    else:
      self.n = 10 * clone.n
      self.cards = clone.cards[0:ncards]

  def get_sig(self):
    ret = 0
    for c in self.cards:
      ret = ret * 100 + c
    return ret
    
  def __str__(self):
    return 'player %d: %s' % (self.n, self.cards)

  def print(self):
    print('player %d: %s' % (self.n, self.cards))

  def draw(self):
    ret = self.cards[0]
    self.cards = self.cards[1:]
    return ret

  def add(self, *cards):
    for c in cards:
      self.cards.append(c)
    # self.print()

  def has_lost(self):
    return len(self.cards) == 0

  def score(self):
    rev = self.cards[::-1]
    res = 0
    for i in range(0, len(rev)):
      res += (i+1) * rev[i]
    return res


class day22(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.players = []
    self.player2 = None
    self.player1 = None

  def reset(self):
    pass

  def load_file(self, file):
    all = reader.FileReader(file, by_group=True).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    all = reader.StringReader(s, by_group=True).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    p = Player(line)
    self.players.append(p)
    p.print()
    if self.player1:
      self.player2 = p
    else:
      self.player1 = p

  def post_load(self):
    pass

  def play1(self):

    while True:
      d1 = self.player1.draw()
      d2 = self.player2.draw()
      if d1 > d2:
        self.player1.add(d1, d2)
      elif d2 > d1:
        self.player2.add(d2, d1)
      else:
        pass

      if self.player1.has_lost():
        self.result1 = self.player2.score()
        break
      elif self.player2.has_lost():
        self.result1 = self.player1.score()
        break



  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.result1 = None

    self.play1()

    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = None

    done = False
    totgame = 0

    def trace(*valist):
      if False:
        print(*valist)

    def do_game(p1, p2):
      nonlocal totgame
      sigs = set()
      totgame = totgame +1
      game = totgame
      round = 0
      while True:
        p1s = p1.get_sig()
        p2s = p2.get_sig()
        if (p1s, p2s) in sigs:
          done = True
          trace('-------- sig match', p1, p2s)
          return 1
        sigs.add((p1s, p2s))

        if p1.has_lost():
          trace('=> winner of game', game, 'is player 2')
          return 2
        elif p2.has_lost():
          trace('=> winner of game', game, 'is player 1')
          return 1

        round += 1
        trace('\n-- round', round, 'game', game)
        trace(p1)
        trace(p2)


        d1 = p1.draw()
        d2 = p2.draw()

        if d1 <= len(p1.cards) and d2 <= len(p2.cards):
          subgame = totgame + 1
          trace('  play subgame...')
          winner = rcombat(p1, d1, p2, d2)
          if winner == 1:
             trace('=> winner game', subgame, 'is player 1')
             p1.add(d1, d2)
          else:
             trace('=> winner game', subgame, 'is player 2')
             p2.add(d2, d1)
        else:
          if d1 > d2:
            p1.add(d1, d2)
            trace('player 1 wins')
          elif d2 > d1:
            p2.add(d2, d1)
            trace('player 2 wins')


    def rcombat(p1, d1, p2, d2):
      x1 = Player(clone=p1, ncards=d1)
      x2 = Player(clone=p2, ncards=d2)
      return do_game(x1, x2)

    while not done:
      if self.player1.has_lost():
        self.player2.print() 
        self.result2 = self.player2.score()
        break
      elif self.player2.has_lost():
        self.result2 = self.player1.score()
        break
      do_game(self.player1, self.player2)


    print('part2', self.result2)
    return self.result2




sample_test("""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""", 306, 291)



if __name__ == '__main__':
  main('input.txt', 33694, 31835)
