"AOC 2020: day 18"

from collections import defaultdict
import math

from tools import reader


def sample_test(s, expect, expect2=None):
  puzz = day18()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day18()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day18()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day18()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Eval(object):

  HACKY = 1
  CLASSIC = 2

  ER    = 0xff
  END   = 0x01
  SHIFT = 0x02
  S     = SHIFT
  R     = 0x04
  RE    = R | END
  names = {
    ER: 'ERROR',
    R: 'reduce',
    RE: 'reduce+end',
    S: 'shift',
    SHIFT|END: 'SE',
  }

  trace = True
  mode = CLASSIC

  def __init__(self):
    pass


  def __str__(self):
    return str(self)


  @staticmethod
  def tokenize(s):
    o0 = ord('0')
    o9 = ord('9')
    for c in s:
      if c in (' ', '\n'):
        continue
      ci = ord(c)
      if o0 <= ci and ci <= o9:
        yield c
      elif c in ('+', '*'):
        yield c
      elif c in ('(', ')'):
        yield c
      else:
        print('fail on ', s)

  @staticmethod
  def eval1(s):
    # Try both ways and compare!
    Eval.mode = Eval.HACKY
    prec = {'(': 1, ')': 99, '+': 5, '*': 5}
    v_hacky = Eval.eval_shift_reduce(s, prec)

    Eval.mode = Eval.CLASSIC
    # The clever reader will note
    prec = {
        # top of stack: {incoming}
        '^': {'(':Eval.S, ')':Eval.ER, '+':Eval.S,  '*':Eval.S},
        '(': {'(':Eval.S, ')':Eval.RE, '+':Eval.S,  '*':Eval.S},
        ')': {'(':Eval.ER,')':Eval.R,  '+':Eval.S,  '*':Eval.S},
        '+': {'(':Eval.S, ')':Eval.R,  '+':Eval.R,  '*':Eval.R},
        '*': {'(':Eval.S, ')':Eval.R,  '+':Eval.R,  '*':Eval.R},
        }
    v_classic = Eval.eval_shift_reduce(s, prec)
    if v_hacky != v_classic:
      print('methods differ on:', s)
      assert v_hacky != v_classic
    return v_classic

  @staticmethod
  def eval2(s):
    if Eval.mode == Eval.HACKY:
      prec = {'(': 1, ')': 99, '+': 5, '*': 4}
    else:
      prec = {
          # top of stack: {incoming}
          '^': {'(':Eval.S, ')':Eval.ER, '+':Eval.S, '*':Eval.S},
          '(': {'(':Eval.S, ')':Eval.RE, '+':Eval.S, '*':Eval.S},
          ')': {'(':Eval.ER,')':Eval.R,  '+':Eval.S, '*':Eval.S},
          '+': {'(':Eval.S, ')':Eval.R,  '+':Eval.R, '*':Eval.R},
          '*': {'(':Eval.S, ')':Eval.R,  '+':Eval.S, '*':Eval.R},
          }
    return Eval.eval_shift_reduce(s, prec)

  @staticmethod
  def eval_shift_reduce(s, prec):
    stack = [None] * len(s)
    vstack = [None] * len(s)
    top = 0
    vtop = 0

    toks = [tok for tok in Eval.tokenize(s)]
    itok = 0

    def reduce():
      nonlocal stack, top, vtop
      #if top < 2:
      #  return
      if stack[top-1] == '^':
        top -= 1
      elif stack[top-1] == '+':
        vstack[vtop-2] += vstack[vtop-1]
        top -= 1
        vtop -= 1
        # print(' -> + top=', vstack[vtop-1])
      elif stack[top-1] == '*':
        vstack[vtop-2] *= vstack[vtop-1]
        vtop -= 1
        top -= 1
        # print(' -> * top=', vstack[vtop-1])
      elif stack[top-1] == '(':
        top -= 1
      else:
        print('reduce fail', vstack[0:vtop], 'stack', stack[0:top])
        assert False
      if Eval.trace:
        print('  reduce ->', vstack[0:vtop], stack[0:top])

    # 1 + 2 * 3 + 4 * 5 + 6

    at = 0
    if Eval.trace:
      print(toks)
    if Eval.mode == Eval.CLASSIC:
      stack[0] = '^'
      top = 1

    while at < len(toks):
      tok = toks[at]
      at += 1

      if tok.isdigit():
        vstack[vtop] = int(tok)
        vtop += 1
        print('n', tok, '>', vstack[0:vtop], '  ', stack[0:top])
        continue

      if Eval.mode == Eval.HACKY:
        if Eval.trace:
          print('tok', tok, vstack[0:vtop], '  ', stack[0:top])
        if tok == '(':
          stack[top] = '('
          top += 1
        elif tok == ')':
          while stack[top-1] != '(':
            reduce()
          top -= 1
        else:
          while top > 0 and prec[tok] <= prec[stack[top-1]]:
            reduce()
          stack[top] = tok
          top += 1

      elif Eval.mode == Eval.CLASSIC:
        while True:
          action = prec[stack[top-1]][tok]
          if Eval.trace:
            print('tok %s: %s %s,  prec<%s %s> => %s' % (
                tok, vstack[0:vtop], stack[0:top],
                stack[top-1], tok, Eval.names[action]))
          if action == Eval.ER:
            print('bad action: invalid expression')
            assert False
          if action & Eval.R:
            reduce()
          if action & Eval.S:
            stack[top] = tok
            top += 1
            # IF S were 0x03 this should not be needed, but it fails if I do. Huh?
            break
          if action & Eval.END:
            break
      else:
        assert Eval.mode in (Eval.HACKY, Eval.CLASSIC)

      if Eval.trace:
        print('  >>>', vstack[0:vtop], '  ', stack[0:top])
    while top > 0:
      if Eval.trace:
        print('  done', vstack[0:vtop], '  ', stack[0:top])
      reduce()

    return vstack[0]


class day18(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.values = []
    self.v2 = []

  def reset(self):
    pass

  def load_file(self, file):
    self.all = reader.FileReader(file).load()

  def load_str(self, s):
    self.all = reader.StringReader(s).load()

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.values = []
    # Compute both ways to check for diff
    for line in self.all:
      self.values.append(Eval.eval1(line))
    print(self.values)
    self.result1 = sum(self.values)

    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.v2 = []

    Eval.mode = Eval.CLASSIC
    for line in self.all:
      self.v2.append(Eval.eval2(line))
    self.result2 = sum(self.v2)

    print('part2', self.result2)
    return self.result2


sample_test('1 + 2 * 3 + 4 * 5 + 6', 71, 231)
sample_test('1 + (2 * 3) + (4 * (5 + 6))', 51, 51)
sample_test('2 * 3 + (4 * 5)', 26, 46)
sample_test('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445)
sample_test('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240, 669060)
sample_test('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340)
sample_test(
    '(7 + (6 * 3 + 6 * 4 * 9 + 3) * 4 + 6 + 8)'
    '+ ((5 + 6 + 5 * 3 * 3) * (6 * 8 * 8 * 5 + 4)) * 7 + 9 * 6'
    , 11783826, None)


if __name__ == '__main__':
  main('input.txt', 9535936849815, 472171581333710)
  pass
