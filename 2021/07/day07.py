"AOC 2021: day 07"

from tools import aoc


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

  def post_load(self):
    # called after all input is read
    self.positions = [int(s) for s in self.all_input[0].split(',')]
    # print(self.positions)
    self.pf = sorted(self.positions)

  def part1(self):
    print('===== Start part 1')

    l = len(self.positions)
    if self.trace_sample:
      print(self.pf)
      print(self.pf[0:l//2])
    move_to = self.pf[l//2]
    print('move to', move_to)
    # print([abs(move_to - spos) for spos in self.pf])
    return sum([abs(move_to - spos) for spos in self.pf])

  def part2(self):
    print('===== Start part 2')

    l = len(self.positions)
    move_to = self.pf[l//2]
    print('move to', move_to)
    mean = sum(self.pf) // len(self.pf)
    print('mean', mean)

    low_cost = 99999999999999999
    min_target = 0
    for target in range(self.pf[0], self.pf[-1]):
       cost = sum([move_cost(target - spos) for spos in self.pf])
       if self.trace_sample:
         print('to', target, 'costs', cost)
       low_cost = min(low_cost, cost)
       if cost == low_cost:
         min_target = target
    print('target:', min_target)
    return low_cost


def move_cost(n):
  n = abs(n)
  return (n * (n + 1)) // 2


day07.sample_test("""
16,1,2,0,4,2,7,1,2,14
""", expect1=37, expect2=168)


if __name__ == '__main__':
  day07.run_and_check('input.txt', expect1=359648, expect2=100727924)
