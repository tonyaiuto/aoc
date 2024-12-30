#!/usr/bin/env python3
"AOC 2023: day 22"

from collections import defaultdict

from tools import aoc


class day22(aoc.aoc):

  def __init__(self):
    super(day22, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.initial = []

  def do_line(self, line):
    # called for each line of input
    initial = int(line)
    self.initial.append(initial)
    if initial >= 16777216:
      print("Large initial", initial)
    assert initial < 0x1000000

  def post_load(self):
    # called after all input is read
    if self.doing_sample:
      print(self.initial)

  def part1(self):
    print('===== Start part 1')

    ret = 0
    for secret in self.initial:
      for i in range(2000):
        secret = evolve(secret)
      ret += secret

    return ret


  def part2(self):
    print('===== Start part 2')

    signals = defaultdict(int)
    best_signal = ''
    best_price = 0
    for secret in self.initial:
      if self.doing_sample:
        print("SECRET", secret)
      changes, prices = calc_changes(secret, n=2000)
      per_monkey = set()
      for i in range(1996):
        price = prices[i+3]
        # signal = tuple(changes[i:i+4])
        signal = ','.join([str(x) for x in changes[i:i+4]])
        if signal in per_monkey:
          continue
        per_monkey.add(signal)
        if price > 0:
          signals[signal] += price
          #if signals[signal] > best_price:
          #  best_price = signals[signal]
          #  best_signal = signal
          #  print("New best at", signal, best_price)

        if self.doing_sample:
          if signal in ('-2,1,-1,3', '-9,7,-6,7'):
            print(i, signal, price, signals[signal])
        #if signal == (7, -6, 7, -4):
        #    print(i, signal, price, signals[signal])
    return max(signals.values())


def evolve(secret):
    secret = secret ^ (secret << 6)
    secret = secret & 0xffffff  # prune  secret % 16777216, secret % 0x1000000
    secret = secret ^ (secret >> 5)
    secret = secret & 0xffffff  # prune
    secret = secret ^ (secret << 11)
    secret = secret & 0xffffff  # prune
    return secret

assert evolve(123) == 15887950
assert evolve(15887950) == 16495136
assert evolve(16495136) == 527345
# 704524
# 1553684
# 12683156
# 11100544
# 12249484
# 7753432
# 5908254


def calc_changes(initial, n=2000):
  cur = initial
  cur_d = cur % 10
  changes = []
  prices = []
  for i in range(n):
    nxt = evolve(cur)
    nxt_d = nxt % 10
    changes.append(nxt_d - cur_d)
    prices.append(nxt_d)
    cur = nxt
    cur_d = nxt_d
  return changes, prices

chgs, prices = calc_changes(123, n=9)
assert chgs == [-3, 6, -1, -1, 0, 2, -2, 0, -2]
assert prices == [0, 6, 5, 4, 4, 6, 4, 4, 2]

day22.sample_test("""
1
10
100
2024
""", expect1=37327623, expect2=None)

day22.sample_test("""
1
2
3
2024
""", expect1=37990510, expect2=23)


if __name__ == '__main__':
  day22.run_and_check('input.txt', expect1=16619522798, expect2=1854)
