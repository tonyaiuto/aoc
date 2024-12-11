#!/usr/bin/env python3
"AOC 2023: day 11"

from tools import aoc


class day11(aoc.aoc):

  def __init__(self):
    super(day11, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def post_load(self):
    # called after all input is read
    self.stones = [int(x) for x in self.all_input[0].split(' ')]


  def part1_slow(self):
    print('===== Start part 1')
    self.reset()
    print(self.stones)

    stones = list(self.stones)
    for blink in range(25):
      if self.doing_sample and blink < 10:
        print(stones)
      ns = []
      for stone in stones:
        ns.extend(self.do_stone(stone))
      stones = ns
    return len(stones)


  def part1(self):
    print('===== Start part 1')
    self.reset()
    print(self.stones)

    ret = 0
    for stone in self.stones:
      x = self.blink_stone(stone, blinks=25)
      # print('stone', stone, '->', x)
      ret += x
    return ret

  def do_stone(self, stone):
    if stone == 0:
      return [1]
    ps = str(stone)
    lps = len(ps)
    if lps % 2 == 0:
      return [int(ps[0:lps//2]), int(ps[lps//2:])]
    return [stone * 2024]


  def blink_stone(self, stone, blinks, verbose=False):
    stones = [stone] 
    for blink in range(blinks):
      ns = []
      for stone in stones:
        ns.extend(self.do_stone(stone))
      stones = ns
      if verbose:
        print(stones)
    return len(stones)


  def part2(self):
    print('===== Start part 2')
    # 3279 998884 1832781 517 8 18864 28 0
    self.reset()

    ret = 0
    for stone in self.stones:
      if self.doing_sample:
        print("START Stone", stone)
      n = how_many(stone, 75)
      if self.doing_sample:
        print("  END Stone", stone, '=', n)
      ret += n
    return ret


blink_map = {}

def how_many(stone, blinks, verbose=False):
  # How many stones are left from stone after n blinks

  key = (stone, blinks)
  if blinks == 0:
    return 1
  memo = blink_map.get(key, -1)
  if memo > 0:
    return memo

  blinks -= 1
  ret = -1
  if stone == 0:
    ret = how_many(1, blinks)
  else:
    ps = str(stone)
    lps = len(ps)
    if lps % 2 == 0:
      ret = how_many(int(ps[0:lps//2]), blinks) + how_many(int(ps[lps//2:]), blinks)
    else:
      ret = how_many(stone * 2024, blinks)
  assert ret > 0
  blink_map[key] = ret
  return ret

n125 = how_many(125, 6)
n17 = how_many(17, 6)
print("125 x 6 =>", n125, "17 x 6 =>", n17)
assert n125 + n17 == 22


day11.sample_test("""
125 17
""", expect1=55312, expect2=65601038650482)


if __name__ == '__main__':
  day11.run_and_check('input.txt', expect1=218956, expect2=259593838049805)
