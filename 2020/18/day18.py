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

  def __init__(self):
    pass


  def __str__(self):
    return str(self)


  @staticmethod
  def tokenize(s):
    o0 = ord('0')
    o9 = ord('9')
    for c in s:
      if c == ' ':
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
  def eval(s):
    stack = [None] * len(s)
    top = 0

    toks = [tok for tok in Eval.tokenize(s)]
    itok = 0

    def do_op(lhs, rhs):
      nonlocal stack, top
      if stack[top-1] == '+':
        top -= 1
        return lhs + rhs
      elif stack[top-1] == '*':
        top -= 1
        return lhs * rhs
      else:
        print("WFT")

    def seval(strt, lvl):
      nonlocal stack, top
      at = strt
      acc = 0
      while at < len(toks):
        tok = toks[at]
        at += 1
        # print(' ' * lvl, 'tok', tok, 'acc', acc, 'stack', stack[0:top])

        if tok == ')':
          return acc, at

        if tok == '(':
          # acc=6, stack=+
          v, nxt = seval(at, lvl+1)
          if at == strt+1:
            acc = v
          else:
            acc = do_op(acc, v)
          at = nxt
        elif tok in ('+', '*'):
          stack[top] = tok
          top += 1
        elif tok.isdigit():
          d = int(tok)
          if at == strt+1:
            acc = d
          else:
            acc = do_op(acc, d)
        # print(' ' * lvl, '  >>> acc', acc, 'stack', stack[0:top])
      return acc, at

    v,_ = seval(0, 0)
    return v

  @staticmethod
  def eval2(s):
    stack = [None] * len(s)
    vstack = [None] * len(s)
    top = 0
    vtop = 0

    toks = [tok for tok in Eval.tokenize(s)]
    itok = 0

    prec = {'(': 1, '+': 5, '*': 4}

    def reduce():
      nonlocal stack, top, vtop
      print('reduce')
      #if top < 2:
      #  return
      if stack[top-1] == '+':
        vstack[vtop-2] += vstack[vtop-1]
        top -= 1
        vtop -= 1
        # print(' -> + top=', vstack[vtop-1])
      elif stack[top-1] == '*':
        vstack[vtop-2] *= vstack[vtop-1]
        vtop -= 1
        top -= 1
        # print(' -> * top=', vstack[vtop-1])
      else:
        print("WTF", )
        assert fail


    # 1 + 2 * 3 + 4 * 5 + 6

    at = 0
    while at < len(toks):
      tok = toks[at]
      at += 1
      print('tok', tok, vstack[0:vtop], 'stack', stack[0:top])
      if tok == ')':
        while stack[top-1] != '(':
          reduce()
        top -= 1
      elif tok == '(':
        stack[top] = '('
        top += 1
      elif tok in ('(', '+', '*'):
        while top >= 1 and prec[tok] < prec[stack[top-1]]:
          reduce()
        stack[top] = tok
        top += 1
      elif tok.isdigit():
        vstack[vtop] = int(tok)
        vtop += 1
      print('  >>>', vstack[0:vtop], 'stack', stack[0:top])
    while top > 0:
      print('  done', vstack[0:vtop], 'stack', stack[0:top])
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
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    all = reader.StringReader(s).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    self.values.append(Eval.eval(line))
    self.v2.append(Eval.eval2(line))


  def post_load(self):
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    print(self.values)
    self.result1 = sum(self.values)

    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = sum(self.v2)

    print('part2', self.result2)
    return self.result2


sample_test('1 + 2 * 3 + 4 * 5 + 6', 71, 231)
sample_test(' 1 + (2 * 3) + (4 * (5 + 6))', 51, 51)
sample_test('2 * 3 + (4 * 5)', 26, 46)
sample_test('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445)
sample_test('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240, 669060)
sample_test('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340)


if __name__ == '__main__':
  main('input.txt', 9535936849815, 472171581333710)
