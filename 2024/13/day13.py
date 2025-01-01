#!/usr/bin/env python3
"AOC 2023: day 13"

from collections import defaultdict
import math

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
    target_x = self.x + offset
    target_y = self.y + offset
   
    # target_x = self.a.x * A + self.b.x * B
    x_base_a, x_delta_a, x_base_b, x_delta_b = self.find_recurrance(
       target_x, self.a.x, self.b.x, verbose=verbose)
    if verbose:
      print("x Base/delta a,b:", x_base_a, x_delta_a, x_base_b, x_delta_b)
    assert target_x == x_base_a * self.a.x + x_base_b * self.b.x
    y_base_a, y_delta_a, y_base_b, y_delta_b = self.find_recurrance(
       target_y, self.a.y, self.b.y, verbose=verbose)
    if verbose:
      print("y Base/delta a,b:", y_base_a, y_delta_a, y_base_b, y_delta_b)
    assert target_y == y_base_a * self.a.y + y_base_b * self.b.y
   
    lcm_x = math.lcm(self.a.x, self.b.x)
    gcd_x = math.gcd(self.a.x, self.b.x)
    a_cycle_x = lcm_x // self.a.x
    b_cycle_x = lcm_x // self.b.x
    print("x via lcm", a_cycle_x, b_cycle_x, 'gcd', gcd_x)
    lcm_y = math.lcm(self.a.y, self.b.y)
    gcd_y = math.gcd(self.a.y, self.b.y)
    a_cycle_y = lcm_y // self.a.y
    b_cycle_y = lcm_y // self.b.y
    print("y via lcm", a_cycle_y, b_cycle_y, 'gcd', gcd_y)

    lcm_a = math.lcm(a_cycle_x, a_cycle_y)
    lcm_b = math.lcm(b_cycle_x, b_cycle_y)
    print("lcm_ab", lcm_a, lcm_b)
    lcm_xy = math.lcm(a_cycle_x * a_cycle_y, b_cycle_x * b_cycle_y)
    print("lcm_xy", lcm_xy, a_cycle_x * a_cycle_y, b_cycle_x * b_cycle_y)

    xf_a = self.b.x // gcd_x
    xf_b = - self.a.x // gcd_x
    yf_a = self.b.y // gcd_y
    yf_b = - self.a.y // gcd_y
    last = 0
    for m in range(1000):
      a = x_base_a + m * xf_a
      b = x_base_b + m * xf_b
      # print(m, a, b, self.a.x * a + self.b.x * b)
      a = y_base_a + m * yf_a
      b = y_base_b + m * yf_b
      # print(m, a, b, self.a.y * a + self.b.y * b)

      n = (x_base_a - y_base_a + m * xf_a) // yf_a
      if n * yf_a == (x_base_a - y_base_a + m * xf_a):
        a = y_base_a + n * yf_a
        b = y_base_b + n * yf_b
        delta = m - last
        print(m, delta, a, b, self.a.x * a + self.b.x * b, self.a.y * a + self.b.y * b)
        last = m
      
   

    """
    for n in range(100):
      a_press = x_base_a + n * lcm_a
      b_press = (target_x - a_press * self.a.x) // self.b.x
      x = a_press * self.a.x + b_press * self.b.x
      y = a_press * self.a.y + b_press * self.b.y

      a_press_y = y_base_a + n * lcm_a
      b_press_y = (target_y - a_press_y * self.a.y) // self.b.y
      x_y = a_press_y * self.a.x + b_press_y * self.b.x
      y_y = a_press_y * self.a.y + b_press_y * self.b.y

      if (abs(y - target_y) < 10000) or n % 10 == 0:
        print(n, '%9d' % a_press, '%9d' % b_press, x, y, y_y)

    # learning
    for n in range(3):
      a_press = (x_base_a + n*x_delta_a)
      b_press = (x_base_b + n*x_delta_b)
      x = a_press * self.a.x + b_press * self.b.x
      a_press2 = (y_base_a + n*y_delta_a)
      b_press2 = (y_base_b + n*y_delta_b)
      y = (y_base_a + n*y_delta_a)*self.a.y + (y_base_b + n*y_delta_b)*self.b.y
      print(n, x, y, a_press, b_press, a_press2, b_press2)
    """

    """
    last_sol = 0
    for na in range(200):
      for nb in range(500):
        a_press = (x_base_a + na*x_delta_a)
        b_press = (x_base_b + na*x_delta_b)
        a_press2 = (y_base_a + nb*y_delta_a)
        b_press2 = (y_base_b + nb*y_delta_b)
        if a_press == a_press2:
          x = a_press * self.a.x + b_press * self.b.x
          y = a_press * self.a.y + b_press * self.b.y
          a_delta = a_press - last_sol
          last_sol = a_press
          print("Solution at a ", a_press, a_delta, x, y)
          if b_press == b_press2:
            print("Solution at b ", b_press)

    if target_x < target_y:
      target = target_y - target_x
      n_a = self.a.y - self.a.x
      n_b = self.b.y - self.b.x
    else:
      target = target_x - target_y
      n_a = self.a.x - self.a.y
      n_b = self.b.x - self.b.y
    if verbose:
      print("X %d = %d * A + %d * B" % (target_x, self.a.x, self.b.x))
      print("Y %d = %d * A + %d * B" % (target_y, self.a.y, self.b.y))
      print("  %d = %d * A + %d * B" % (target, n_a, n_b))

    nn = 0
    for a in range(base_a, 2*target // n_a, delta_a):
      need = target - n_a * a
      b = need // n_b
      print(a * n_a + b * n_b, '=== %d * %d + %d * %d' % (a, n_a, b, n_b))
      nn += 1
      if nn > 3:
        break

    need_bx = target_x - base_a * self.a.x
    bpress = need_bx // self.b.x
    got = base_a * self.a.x + bpress * self.b.x
    print(target_x, ":", got, "<= %d * %d + %d * %d" % (self.a.x, base_a, self.b.x, bpress))
    # return 11
    """

    """
    maxa = target_x // self.a.x
    n_sol = 0
    for i in range(100):
      a = maxa - i
      need_bx = target_x - self.a.x * a
      b = need_bx // self.b.x
      got = self.a.x * a + self.b.x * b
      if target_x == got:
        print("Got x solution at a,b", a, b, got)
        got_y = self.a.y * a + self.b.y * b
        if target_y == got_y:
          n_sol += 1
          print("Got full solution at a,b", a, b, got, got_y)
          if n_sol > 0:
            break
    """

    
  def find_recurrance(self, target, n_a, n_b, verbose=False):
    # Find the recurance relationship
    # compute base # of A & B presses for cycle to start and 
    # how many more of each to hit it again.
    n_solved = 0
    a_press = 0
    while n_solved < 3:
      a_press += 1
      left = target - n_a * a_press
      b_press = left // n_b
      if (b_press > 0) and (b_press * n_b == left):
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
          print(' pattern at %d %d => cost: %d' % (a_press, b_press, cost))
    return base_a, delta_a, base_b, delta_b


  def least_cost2_a(self, verbose=False):
    if verbose:
      print(self)
    offset = 10000000000000
    #self.x += offset
    #self.y += offset
    base_a, delta_a, base_b, delta_b = self.find_recurrance(
       self.target, self.n_a, self.nb, verbose=verbose)

    # Ax = base_a + delta_a * N
    # Bx = base_b + delta_b * N
    # COST = 3 * (base_a + delta_a * N) + (base_b + delta_b * N)
    # COST = 3 * base_a + 3 * delta_a * N + base_b + delta_b * N
    # COST = 3 * base_a + base+b + N * (3 * delta_a + delta_b)

    def n_to_cost(n):
      return 3 * base_a + base_b + n * (3 * delta_a + delta_b)

    if verbose:
      print("base/delta, a/b", base_a, delta_a, base_b, delta_b)
      print("costs 0..2:", n_to_cost(0), n_to_cost(1), n_to_cost(2))
    assert n_to_cost(0) == base_cost
    assert n_to_cost(1) == delta1_cost
    assert n_to_cost(2) == delta2_cost

    # solve for 
    # self.x = A * self.a.x + B * self.b.x
    # self.x = (base_a + delta_a * N) * self.a.x + (base_b + delta_b * N) * self.b.x
    # self.x = (base_a + delta_a * N) * self.a.x + (base_b + delta_b * N) * self.b.x
    # self.x = base_a * self.a.x + base_b * self.b.x + (delta_a * self.a.x + delta_b * self.b.x) * N
    # self.x = base_a * self.a.x + base_b * self.b.x + (delta_a * self.a.x + delta_b * self.b.x) * N
    # self.x = base_a + delta_a * midpoint + base_b + delta_b * midpoint

    # self.x = (base_a + delta_a * N) * self.a.x + (base_b + delta_b * N) * self.b.x

    # limits of N range
    target_x = self.x + offset - base_a * self.a.x - base_b * self.b.x
    target_y = self.y + offset - base_a * self.a.y - base_b * self.b.y
    # assert N * delta_a * self.x == target_x


    lower = 1
    max_a = min(target_x // self.a.x, (self.y + offset) // self.a.y)
    max_b = min(target_x // self.b.x, (self.y + offset) // self.b.y)
    max_an = (max_a - base_a) // delta_a
    max_bn = (max_b - base_b) // delta_b
    upper = min(max_an, max_bn)

    print("N from", lower, "to", upper)
    while upper > lower + 2:
      midpoint = (upper - lower) // 2 + lower
      x = base_a + delta_a * midpoint + base_b + delta_b * midpoint
      if x > target_x:
        break
      # 113636363729
      # 10000000007870
      lower = midpoint
    print("rebound N from", lower, "to", upper)

    for n in range(lower, lower+5):
      a_press = base_a + delta_a * n
      b_press = base_b + delta_b * n
      got_x = self.a.x * a_press + self.b.x * b_press
      got_y = self.a.y * a_press + self.b.y * b_press
      off_x = self.x + offset - got_x
      off_y = self.y + offset - got_y
      print(n, '#a,b', a_press, b_press, '=>', got_x, got_y, 'offby', off_x, off_y)

  
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
    # called for each group of input
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
