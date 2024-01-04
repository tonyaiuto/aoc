#!/usr/bin/env python3
"AOC 2023: day 19"

from collections import defaultdict
import copy
import functools

from tools import aoc
from tools import gridutils
from tools import qparser


# Fake workflow names
MORE = "_MORE_"
FINAL_A = "_FINAL_"


class Rule(object):
  
  REV_COND = {
      '<': '>=',
      '>': '<=',
  }

  def __init__(self, s):
    p = s.split(':')
    self.var = s[0]
    self.cond = s[1]
    self.value = int(p[0][2:])
    self.action = p[1]

  def __str__(self):
    return '%s %s %d : %s' % (self.var, self.cond, self.value, self.action)

  def __repr__(self):
    return str(self)

  def eval(self, rating, verbose=False):
    val = rating.get_var(self.var)
    if self.cond == '<':
      ok = val < self.value
    elif self.cond == '>':
      ok = val > self.value
    else:
      assert str(self) == 'bogus'
    if verbose:
      print('  ', self, 'got', val, '=>', ok)
    return ok

  def cond_p(self):
    # Printable clause that makes rule succeed
    if self.action == 'R':
      expr = '%s %s %d' % (self.var, Rule.REV_COND[self.cond], self.value)
      if self.cond == '<':
        cond = Range(self.var, self.value, 4000)
      else:
        cond = Range(self.var, 1, self.value)
      return expr, cond, MORE
    expr = '%s %c %d' % (self.var, self.cond, self.value)
    if self.cond == '<':
      cond = Range(self.var, 1, self.value-1)
    else:
      cond = Range(self.var, self.value+1, 4000)
    if self.action == 'A':
      return expr, cond, FINAL_A
    return expr, cond, self.action

class Range(object):

  def __init__(self, var, low, high):
    self.var = var
    self.low = low
    self.high = high

  def __str__(self):
    return '(%s, %4d, %4d)' % (self.var, self.low, self.high)

  @staticmethod
  def cmp(a, b):
    diff = ord(a.var) - ord(b.var)
    if diff != 0:
      return diff
    diff = a.low - b.low
    if diff != 0:
      return diff
    diff = a.high - b.high
    if diff != 0:
      return diff
    return 0

def cmp_range_set(a, b):
  diff = len(a) - len(b)
  if diff != 0:
    return diff
  for i in range(len(a)):
    diff = Range.cmp(a[i], b[i])
    if diff:
      return diff
  return 0

def fill_win(win):
  got = set([x.var for x in win])
  need = set(['a', 'm', 's', 'x']) - got
  return win + [(n, 1, 4000) for n in need]


class Workflow(object):

  parser = qparser.QParser([
    qparser.Text('name'),
    qparser.Literal('{'),
    qparser.List('rules_raw', qparser.Text(), delim=','),
    qparser.Literal('}'),
  ])

  def __init__(self, s):
    Workflow.parser.parse(self, s)
    self.next = self.rules_raw[-1]
    self.rules_raw = self.rules_raw[0:-1]
    self.rules = []
    for rr in self.rules_raw:
      self.rules.append(Rule(rr)) 

  def __str__(self):
    return '%s { %s } => %s' % (self.name, ', '.join([str(r) for r in self.rules]), self.next)

  def __repr__(self):
    return str(self)


class Rating(object):

  # {x=787,m=2655,a=1222,s=2876}
  parser = qparser.QParser([
    qparser.Literal('{'),
    qparser.Literal('x='),
    qparser.Number('x'),
    qparser.Literal(',m='),
    qparser.Number('m'),
    qparser.Literal(',a='),
    qparser.Number('a'),
    qparser.Literal(',s='),
    qparser.Number('s'),
    qparser.Literal('}'),
  ])

  def __init__(self, s):
    Rating.parser.parse(self, s)
    self.total = self.x + self.m + self.a + self.s

  def __str__(self):
    return '%d {x=%d, m=%d, a=%d, s=%d}' % (self.total, self.x, self.m, self.a, self.s)

  def __repr__(self):
    return str(self)

  def get_var(self, var):
    if var == 'm':
      return self.m
    if var == 'x':
      return self.x
    if var == 'a':
      return self.a
    if var == 's':
      return self.s
    assert var == 'WTF, undefined'


class day19(aoc.aoc):

  def __init__(self):
    super(day19, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.workflows = {}
    self.ratings = []
    self.doing_workflows = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    if not line:
      self.doing_workflows = False
      return
    if self.doing_workflows:
      wf = Workflow(line)
      if self.doing_sample:
        print('WORKFLOW', wf)   
      self.workflows[wf.name] = wf
    else:
      rating = Rating(line)
      self.ratings.append(rating)
      if self.doing_sample:
        print('Rating:', rating)   

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    ret = 0
    for rating in self.ratings:
      print("==== Rating", rating)
      accept = self.part1_eval(rating)
      if accept:
        if self.doing_sample:
          print("  ACCEPTING:", rating, "tot +=", rating.total)
        ret += rating.total
      else:
        if self.doing_sample:
          print("  REJECTING:", rating)
        pass

    print("part1", ret)
    return ret

  def part1_eval(self, rating):
    workflow = self.workflows['in']
    while True:
      if self.doing_sample:
        print(" . eval workflow", workflow)
      next_workflow = None

      for rule in workflow.rules:
        # hqn{a<2457:bjm,x<2335:qql,s>1648:tbn,tgg}
        ok = rule.eval(rating, verbose=(workflow.name == 'hqn'))
        if ok:
          action = rule.action
          if action == 'A':  # accept          
            # print("   OK, ACCEPT")
            return True
          if action == 'R':  # accept          
            # print("   OK, REJECT")
            return False
          # print("   OK, Move to workflow", action)
          next_workflow = self.workflows[action]
          break

      # assert: Rules done or changed workspace

      if next_workflow:
        workflow = next_workflow
        continue

      # Rules all done, use workspace default
      if workflow.next == 'A':  # accept          
        return True
      if workflow.next == 'R':  # accept          
        print("REJECT")
        return False
      workflow = self.workflows[workflow.next]

    print("WTF")
    return False

  def part2(self):
    print('===== Start part 2')
    self.useless_verify()

    reduced = self.reduce_workflows()
    original_n_wf = len(self.workflows)
    self.workflows = {w.name: w for w in reduced}
    new_n_wf = len(self.workflows)
    print('==== DONE WITH REDUCE. From', original_n_wf, 'to', new_n_wf)
    for w_n in sorted(self.workflows):
      print(self.workflows[w_n])

    workflow = self.workflows['in']
    clauses = []
    pclauses = []
    self.wins = []
    self.expand(workflow, clauses, pclauses)
    wins = self.wins
    for win in wins:
      print("WIN:", ' '.join([str(c) for c in win]))

    # wins = [fill_win(w) for w in wins]
    wins = [sorted(w, key=functools.cmp_to_key(Range.cmp)) for w in wins]
    wins = sorted(wins, key=functools.cmp_to_key(cmp_range_set))
    print("=== FILLED & cond sorted and sorted")
    for win in wins:
      print("WIN:", ' '.join([str(c) for c in win]))

    print("=== EVAL")

    ret = 0
    for win in wins:
      s = [4000] * 4
      for ic, cond in enumerate(win):
        s[ic] = cond.high - cond.low + 1
      ok_count = s[0] * s[1] * s[2] * s[3]
      print("WIN:", "%11d" % ok_count, ' '.join([str(c) for c in win]))
      ret += ok_count

    print("too high by", ret - 167409079868000)
    return ret

  def reduce_workflows(self):
    workflows = set(self.workflows.values())
    while True:
      reducible = self.find_reducible(workflows)
      if not reducible:
        break
      for remove in  reducible:
        workflows.remove(remove)
        for w in workflows:
          for rule in w.rules:
            if rule.action == remove.name:
              print("replace", remove.name, "with %s in" % remove.next, rule)
              rule.action = remove.next
          if w.next == remove.name:
            print("replace fallback", remove.name, "with %s in" % remove.next, w)
            w.next = remove.next
    return workflows

  def find_reducible(self, workflows):
    reducible = []
    for workflow in workflows:
      if workflow.next == 'A':
        always_true = True
        for rule in workflow.rules:
          if rule.action != 'A':
            always_true = False
            break
        if always_true:
          reducible.append(workflow)
          print("Can reduce", workflow)
      if workflow.next == 'R':
        always_true = True
        for rule in workflow.rules:
          if rule.action != 'R':
            always_true = False
            break
        if always_true:
          reducible.append(workflow)
          print("Can reduce", workflow)
    return reducible 

  def expand(self, workflow, clauses, pclauses):
    if False and self.doing_sample:
      print(" . expand workflow", workflow)
    orig_clauses = copy.copy(clauses)
    orig_pclauses = copy.copy(pclauses)
    for rule in workflow.rules:
      expr, cond, nxt = rule.cond_p()
      clauses.append(cond)
      pclauses.append(expr)
      if nxt == MORE:
        continue
      if nxt == FINAL_A:
        #print("A:", ' and '.join(pclauses))
        print("A:", ' and '.join([str(c) for c in clauses]))
        self.add_win(clauses)
      else:
        next_workflow = self.workflows[nxt]
        self.expand(next_workflow, copy.copy(clauses), copy.copy(pclauses))

    if workflow.next == 'A':  # accept          
      #print("A:", ' and '.join(pclauses))
      print("A:", ' and '.join([str(c) for c in clauses]))
      self.add_win(clauses)
      return
    if workflow.next == 'R':  # accept          
      # print("REJECT:", ' and '.join(pclauses))
      return
    next_workflow = self.workflows[workflow.next]
    self.expand(next_workflow, orig_clauses, orig_pclauses)

  def add_win(self, clauses):
    have = {}
    for c in clauses:
      dup = have.get(c.var)
      if dup:
        low = max(c.low, dup.low)
        high = min(c.high, dup.high)
        if low > high:
          return  
        c = Range(c.var, low, high)
      have[c.var] = c
    self.wins.append(have.values())

  def useless_verify(self):
    # Explore the data a bit
    counts = defaultdict(int)
    for workflow in self.workflows.values():
      for rule in workflow.rules:
        if rule.action not in ('A', 'R'):
          counts[rule.action] += 1
      if workflow.next not in ('A', 'R'):
        counts[workflow.next] += 1
    for k, v in counts.items():
      if v != 1:
        print("More than 1 of", k, v)
        assert False
    # Each rule is only used once.  Does this matter?


day19.sample_test("""
in{s<1351:px,qqz}
crn{x>2662:A,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}
lnx{m>1548:A,A}
pv{a>1716:R,A}
px{a<2006:qkq,m>2090:A,rfg}
qkq{x<1416:A,crn}
qqz{s>2770:qs,m<1801:hdj,R}
qs{s>3448:A,lnx}
rfg{s<537:gd,x>2440:R,A}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""", expect1=19114, expect2=167409079868000)


if __name__ == '__main__':
  day19.run_and_check('input.txt', expect1=397643, expect2=None)
