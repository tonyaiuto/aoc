"AOC 2020: day 21"

from collections import defaultdict
import math

from tools import reader
from tools import qparser as qp


def sample_test(s, expect, expect2=None):
  puzz = day21()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    # puzz = day21()
    # puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day21()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  # puzz = day21()
  # puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Food(object):

  count = 0

  rule_parser = qp.QParser([
    qp.List('ingredients', qp.Text(), delim=' '),
    qp.Literal('(contains '),
    qp.List('allerg', qp.Text(), delim=','),
    qp.Literal(')'),
    ])


  def __init__(self, s):
    Food.count = Food.count + 1
    self.n = Food.count
    Food.rule_parser.parse(self, s)
    self.ingredients = set(self.ingredients)
    self.allerg = set(self.allerg)
    self.col = -1


  def __str__(self):
    return '%d: i:%s, a:%s' % (self.n, self.ingredients, self.allerg)

  @staticmethod
  def from_string(s):
    return Food(s)




class day21(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.foods = []

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
    f = Food(line)
    # print(f)
    self.foods.append(f)
    pass

  def post_load(self):
    pass



  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.result1 = None

    # map of i to what they could have
    self.could_contain = defaultdict(set)
    # map of a to i
    could_be_in = defaultdict(set)
    all_a = set()
    all_i = set()
    for f in self.foods:
      for a in f.allerg:
        all_a.add(a)
        for i in f.ingredients:
          all_i.add(i)
          self.could_contain[i].add(a)
          could_be_in[a].add(f)

    print('=== phase1')
    for f in self.foods:
      for a in f.allerg:
        for otherf in could_be_in[a]:
          if f == otherf:
            continue 
          common = f.ingredients.intersection(otherf.ingredients)
          print(common, 'are in two foods with', a)
          for i in f.ingredients-common:
            print('remove', i, a, 'from', f)
            if a in self.could_contain[i]:
              self.could_contain[i].remove(a)

    print('=== phase3')
    safe = set()
    self.danger = set()
    for i in all_i:
      # print(i, 'could contain', ','.join((a for a in self.could_contain[i])))
      if len(self.could_contain[i]) == 0:
        print(i, 'is safe')
        safe.add(i)
      else:
        self.danger.add(i)

    cnt = 0
    for f in self.foods:
      for i in f.ingredients:
        if i in safe:
          cnt += 1

    self.result1 = cnt
    print('part1', self.result1)
    return self.result1



  def part2(self):
    print('===== Start part 2')
    self.reset()

    dlist = set()
    while len(dlist) < len(self.danger):
      for i in self.danger:
        print(i, 'could contain', ','.join((a for a in self.could_contain[i])))
        if len(self.could_contain[i]) == 1:
          a = list(self.could_contain[i])[0]
          dlist.add((a, i))
          for otheri in self.danger:
            if i == otheri:
              continue
            if a in self.could_contain[otheri]:
              self.could_contain[otheri].remove(a)

    dl = list(dlist)
    dl.sort(key=lambda x: x[0])
    print(dl)

    self.result2 = ','.join(x[1] for x in dl)
    print('part2', self.result2)
    return self.result2



sample_test("""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""", 5, 'mxmxvkd,sqjhc,fvjkl')



if __name__ == '__main__':
  main('input.txt', 2380, 'ktpbgdn,pnpfjb,ndfb,rdhljms,xzfj,bfgcms,fkcmf,hdqkqhh')
