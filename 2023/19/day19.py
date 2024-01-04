#!/usr/bin/env python3
"AOC 2023: day 19"

from collections import defaultdict
import copy

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
      return expr, MORE
    expr = '%s %c %d' % (self.var, self.cond, self.value)
    if self.action == 'A':
      return expr, FINAL_A
    return expr, self.action


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
    self.expand(workflow, clauses)

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
            print("replace fallback", remove.name, "with %s in" % remove.next, rule)
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


  def expand(self, workflow, clauses):
    if self.doing_sample:
      print(" . expand workflow", workflow)
    # hqn{a<2457:bjm,x<2335:qql,s>1648:tbn,tgg}
    # 
    orig_clauses = copy.copy(clauses)
    for rule in workflow.rules:
      expr, nxt = rule.cond_p()
      clauses.append(expr)
      if nxt == MORE:
        continue
      if nxt == FINAL_A:
        print("A:", ' and '.join(clauses))
      else:
        next_workflow = self.workflows[nxt]
        self.expand(next_workflow, copy.copy(clauses))

      if workflow.next == 'A':  # accept          
        print("A:", ' and '.join(clauses))
        return
      if workflow.next == 'R':  # accept          
        print("REJECT:", ' and '.join(clauses))
        return
      next_workflow = self.workflows[workflow.next]
      self.expand(next_workflow, orig_clauses)


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


  def bind_w(self, workflow):
    for r in workflow.rules:
      r.var

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
