#!/usr/bin/env python3
"AOC 2023: day 13"

from collections import defaultdict

from tools import aoc
from tools import qparser


class Button(object):

  button_parser = qparser.QParser([
          qparser.Literal('Button'),
          qparser.Text(name='button', eat_leading_ws=True),
          qparser.Literal(': X+'),
          qparser.Number(name='x'),
          qparser.Literal(', Y+'),
          qparser.Number(name='y'),
        ])

  def __init__(self, line):
    self.button = ''
    self.x = 0
    self.y = 0
    Button.button_parser.parse(self, line)

  def __repr__(self):
    return str(self.__dict__)

  def __str__(self):
    return '%s %d %d' % (self.button, self.x, self.y)


class Prize(object):

  prize_parser = qparser.QParser([
          qparser.Literal('Prize: X='),
          qparser.Number(name='x'),
          qparser.Literal(', Y='),
          qparser.Number(name='y'),
        ])

  def __init__(self, line, a, b):
    Prize.prize_parser.parse(self, line)
    self.a = a
    self.b = b
    self.least_cost = -1
    # subract the two linear equations.
    if self.x > self.y:
      self.target = self.x - self.y
      self.n_a = self.a.x - self.a.y
      self.n_b = self.b.x - self.b.y
    else:
      self.target = self.y - self.x
      self.n_a = self.a.y - self.a.x
      self.n_b = self.b.y - self.b.x

  def __repr__(self):
    return 'prize: %5d %5d' % (self.x, self.y)

  def __str__(self):
    return '%s %s %s' % (self.__repr__(), self.a, self.b)

  def least_cost1(self, verbose=False):
    if verbose:
      print(self)
    a_max = min(100, self.x // self.a.x, self.y // self.a.y)
    b_max = min(100, self.x // self.b.x, self.y // self.b.y)
    self.least_cost = -1
    for a_press in range(a_max):
      cost = self.press2cost(a_press, b_max=b_max, verbose=verbose)
      # cost_alt = self.press2cost_alt(a_press, b_max=b_max, verbose=verbose)
      # if cost != cost_alt:
      #   print("cost diff", cost, cost_alt)
      if cost <= 0:
        continue
      if self.least_cost > 0:
        self.least_cost = min(cost, self.least_cost)
      else:
        self.least_cost = cost
    return self.least_cost

  def least_cost2(self, verbose=False):
    if verbose:
      print(self)
    offset = 10000000000000
    #self.x += offset
    #self.y += offset

    # Find the recurance relationship
    # compute base # of A & B presses for cycle to start and 
    # how many more of each to hit it again.
    n_solved = 0
    a_press = 0
    while n_solved < 3:
      a_press += 1
      left = self.target - self.n_a * a_press
      b_press = left // self.n_b
      if (b_press > 0) and (b_press * self.n_b == left):
        # we have a solution
        cost = 3 * a_press + b_press
        if n_solved == 0:
          base_a = a_press
          base_b = b_press
          base_cost = cost
        elif n_solved == 1:
          delta_a = a_press - base_a
          delta_b = b_press - base_b
          delta1_cost = cost
        elif n_solved == 2:
          assert a_press == base_a + 2 * delta_a
          assert b_press == base_b + 2 * delta_b
          delta2_cost = cost
        n_solved += 1
        if verbose:
          print(' solution at %d %d => cost: %d' % (a_press, b_press, cost))

    # Ax = base_a + delta_a * N
    # Bx = base_b + delta_b * N
    # COST = 3 * (base_a + delta_a * N) + (base_b + delta_b * N)
    # COST = 3 * base_a + 3 * delta_a * N + base_b + delta_b * N
    # COST = 3 * base_a + base+b + N * (3 * delta_a + delta_b)

    def n_to_cost(n):
      return 3 * base_a + base_b + n * (3 * delta_a + delta_b)

    if verbose:
      print("costs 0..2:", n_to_cost(0), n_to_cost(1), n_to_cost(2))
    assert n_to_cost(0) == base_cost
    assert n_to_cost(1) == delta1_cost
    assert n_to_cost(2) == delta2_cost

    # solve for 
    # self.x = A * self.a.x + B * self.b.x
    # self.x = (base_a + delta_a * N) * self.a.x + (base_b + delta_b * N) * self.b.x
    # self.x = (base_a + delta_a * N) * self.a.x + (base_b + delta_b * N) * self.b.x
    # self.x = base_a * self.a.x + base_b * self.b.x  + delta_a * N * self.a.x + (base_b + delta_b * N) * self.b.x


    # limits of N range
    lower = 1
    max_a = max((self.x + offset) // self.a.x, (self.y + offset) // self.a.y)
    max_b = max((self.x + offset) // self.b.x, (self.y + offset) // self.b.y)
    max_an = (max_a - base_a) // delta_a
    max_bn = (max_b - base_b) // delta_b
    upper = max(max_an, max_bn)

    print("N from", lower, "to", upper)
    target = self.x + offset
    while upper > lower + 2:
      midpoint = (upper - lower) // 2 + lower
      x = base_a + delta_a * midpoint + base_b + delta_b * midpoint
      if x > target:
        break
      # 113636363729
      # 10000000007870
      lower = midpoint
    print("rebound N from", lower, "to", upper)
  
    for n in range(lower-10000, upper+1):
      a_press = base_a + delta_a * n
      b_press = base_b + delta_b * n
      if self.is_solution(a_press, b_press):
        cost = n_to_cost(n)
        print("===== solution @", n, "cost", cost)
        self.least_cost = min(self.least_cost, cost)

    """
    while upper > lower:
      midpoint = (upper - lower) // 2 + lower
      cost = n_to_cost(midpoint)
      cost_plus_1 = n_to_cost(midpoint+1)
      cost_plus_2 = n_to_cost(midpoint+2)
      cost_minus_1 = n_to_cost(midpoint-1)
      cost_minus_2 = n_to_cost(midpoint-2)

      if cost < cost_plus_1:
        # 5 points of trend.
        assert cost_plus_1 < cost_plus_2
        assert cost_minus_1 < cost
        assert cost_minus_2 < cost_minus_1
        lower = midpoint
      else:
        upper 

    """
    return self.least_cost

  def is_solution(self, a_press, b_press):
    return (self.x == (self.a.x * a_press + self.b.x * b_press)
            and self.y == (self.a.y * a_press + self.b.y * b_press))


  def press2cost(self, a_press, b_max=0, verbose=False):
    left = self.x - self.a.x * a_press
    b_press = left // self.b.x
    if b_press * self.b.x == left:
      if self.y == a_press * self.a.y + b_press * self.b.y:
        # we have a solution
        if b_max > 0 and b_press > b_max:
          return -1
        cost = 3 * a_press + b_press
        if verbose:
          print(' prize at %d %d => cost: %d' % (a_press, b_press, cost))
        return cost
    return -1

  def press2cost_alt(self, a_press, b_max=0, verbose=False):
    left = self.target - self.n_a * a_press
    b_press = left // self.n_b
    if b_press * self.n_b == left:
      # we have a solution
      if b_press < 0 or (b_max > 0 and b_press > b_max):
        return -1
      cost = 3 * a_press + b_press
      if verbose:
        print(' prize at %d %d => cost: %d (alt)' % (a_press, b_press, cost))
      return cost
    return -1


class day13(aoc.aoc):

  def __init__(self):
    super(day13, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.prizes = []
    
  def do_line(self, line):
    # called for each line of input
    a = Button(line[0])
    b = Button(line[1])
    prize = Prize(line[2], a, b)
    if self.doing_sample:
      print(prize)
    self.prizes.append(prize)


  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for prize in self.prizes:
      cost = prize.least_cost1(verbose=self.doing_sample)
      if cost > 0:
        ret += cost
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for prize in self.prizes:
      cost = prize.least_cost2(verbose=self.doing_sample)
      if cost > 0:
        ret += cost
      if not self.doing_sample:
        break
    return ret


day13.sample_test("""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

""", expect1=480, expect2=17)


if __name__ == '__main__':
  # 26923 low part1
  day13.run_and_check('input.txt', expect1=27105, expect2=None)
