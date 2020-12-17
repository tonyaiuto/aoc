"AOC 2020: day 16"

from collections import defaultdict
import math

from tools import reader
from tools import qparser as qp


def sample_test(s, expect, expect2=None):
  if expect:
    puzz = day16()
    puzz.load_str(s)
    res = puzz.part1()
    if expect != res:
      print('FAIL: expect', expect, 'got', res)
      assert expect == res

  if expect2:
    puzz = day16()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day16()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day16()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Field(object):

  rule_parser = qp.QParser([
    qp.Text('name', allow_space=True),
    qp.Literal(':'),
    qp.Number('r1_low'),
    qp.Literal('-'),
    qp.Number('r1_high'),
    qp.Literal('or'),
    qp.Number('r2_low'),
    qp.Literal('-'),
    qp.Number('r2_high'),
    ])

  def __init__(self):
    self.col = -1

  def __str__(self):
    return '%s<%d-%d | %d-%d, col:%d>' % (self.name, self.r1_low, self.r1_high, self.r2_low, self.r2_high, self.col)

  def __repr__(self):
    return self.name

  @staticmethod
  def fromText(line):
    x = line.split(':')
    ret = Field()
    Field.rule_parser.parse(ret, line)
    return ret

  def is_valid(self, n):
    if ((self.r1_low <= n and n <= self.r1_high)
        or (self.r2_low <= n and n <= self.r2_high)):
      return True
    return False


class day16(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True

  def reset(self):
    pass

  def load_file(self, file):
    self.all = reader.FileReader(file, by_group=True).load()
    self.post_load()

  def load_str(self, s):
    self.all = reader.StringReader(s, by_group=True).load()
    self.post_load()

  def do_line(self, line):
    pass

  def post_load(self):
    self.fields = {}
    for field in self.all[0]:
      f = Field.fromText(field)
      self.fields[f.name] = f
      print('field', f)
    assert self.all[1][0] == 'your ticket:'

    self.me = [int(x) for x in self.all[1][1].split(',')]
    print('My ticket', self.me)

    self.near = []
    for t in self.all[2][1:]:
      self.near.append([int(x) for x in t.split(',')])

  def valid_fields(self, v):
    ret = []
    for f in self.fields.values():
      if f.is_valid(v):
         ret.append(f)
    return ret

  def get_invalid(self, tkt):
    ret = []
    for v in tkt:
      flds = self.valid_fields(v)
      if not flds:
        ret.append(v)
    return ret

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.result1 = None

    n_valid = 0
    rate = 0
    for tkt in self.near:
      iv = self.get_invalid(tkt)
      rate += sum(iv)
    self.result1 = rate

    print('part1', self.result1)
    return self.result1


  def part2(self):
    print('===== Start part 2')
    self.reset()

    n_valid = 0
    rate = 0
    ok = []
    for tkt in self.near:
      iv = self.get_invalid(tkt)
      if not iv:
        ok.append(tkt)

    def are_all_tickets_ok_for_f(fld, col):
      for tkt in ok:
        v = tkt[col]
        if not fld.is_valid(v):
          return False
      return True

    for fld in self.fields.values():
      fld.ok = set()
      for col in range(len(self.fields)):
        if are_all_tickets_ok_for_f(fld, col):
          print('col', col, 'can be', fld)
          fld.ok.add(col)
      if len(fld.ok) == 1:
        fld.col = list(fld.ok)[0]
        print('col', fld.col, '==IS==', fld)
 
    # remove good from other
    # while sum([1 for f in self.fields.values() if len(f.ok) > 1]) > 0:
    for i in range(len(self.fields)):
      for fld in self.fields.values():
        if fld.col >= 0:
          for f2 in self.fields.values():
            if fld != f2 and fld.col in f2.ok:
              # print('drop col', fld.col, 'from', f2.name)
              f2.ok.remove(fld.col)
              if len(f2.ok) == 1:
                f2.col = list(f2.ok)[0]
                print('final:', fld)
  
    result = 1
    for fld in self.fields.values():
      if fld.name.startswith('departure'):
        result *= self.me[fld.col]
    self.result2 = result

    print('part2', self.result2)
    return self.result2



sample_test("""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""", 71, None)

sample_test("""
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""", None, 1)

if __name__ == '__main__':
  main('input.txt', 27898, 2766491048287)
  pass
