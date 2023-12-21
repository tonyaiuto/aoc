#!/usr/bin/env python3
"AOC 2023: day 20"

from collections import defaultdict
from collections import deque

from tools import aoc
from tools import gridutils
from tools import qparser

FF = 1
CONJ = 2
CAST = 3

HIGH = True
LOW = False

class Module(object):
 
  # &pf -> pp, tv, rl, pm, hk
  def __init__(self, s):
    parts = s.replace(', ', ' ').replace('  ', ' ').split(' ')
    assert parts[1] == '->'
    name = parts[0]
    if name[0] == '%':
      self.name = name[1:]
      self.type = FF
    elif name[0] == '&':
      self.name = name[1:]
      self.type = CONJ
      self.inputs = {}
    elif name == 'broadcaster':
      self.name = name
      self.type = CAST
    else:
      print("WACKY", s)
      assert False
    self.outputs_s = parts[2:]
    if not self.outputs_s:
      self.outputs = []
    self.state = False
    self.in_list = None

  def __str__(self):
    return '%s %d -> %s' % (self.name, self.type, self.outputs_s)

  def __repr__(self):
    return self.name

  def short_str(self):
    return '%s:%c' % (self.name, 'H' if self.state else 'L')

  def as_bits(self):
    if self.type == FF:
      return '1' if self.state else '0'
    order = self.in_list if self.in_list else self.inputs
    return ' %s:%s' % (
        self.name,
        ''.join(['1' if o.state else '0' for o in order])
    )


class day20(aoc.aoc):

  def __init__(self):
    super(day20, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.modules = {}
    self.done = False

  def reset(self):
    self.done = False

  def do_line(self, line):
    m = Module(line)
    self.modules[m.name] = m
    # print(m)

  def post_load(self):
    # called after all input is read
    # do the lookups and find the conjunctions
    to_add = {}
    for m in self.modules.values():
      m.outputs = []
      for out in m.outputs_s:
        actual = self.modules.get(out)
        if not actual:
          actual = to_add.get(out)
        if not actual:
          print("Creating dummy sink", out)
          actual = Module("%%%s ->" % out)
          to_add[actual.name] = actual
        m.outputs.append(actual)

      for out in m.outputs:
        if out.type == CONJ:
          out.inputs[m] = LOW

    for m in to_add.values():
      self.modules[m.name] = m

    # special ones
    self.broadcaster = self.modules['broadcaster']
    self.rx = self.modules.get('rx')

    # make the printing nicer
    self.state_order = [
      self.modules[m] for m in (
         sorted([m.name for m in self.modules.values() if m.type == FF])
         + sorted([m.name for m in self.modules.values() if m.type == CONJ]))
    ]

    for m in self.modules.values():
      if m.type == CONJ:
        print('CONJ', m, "===", m.inputs)

    pf = self.modules.get('pf')
    if pf:
      self.set_in_list(pf, ['hk', 'qn', 'zr', 'vx', 'lj', 'fl', 'zn', 'vh', 'cb'])
    xd = self.modules.get('xd')
    if xd:
      self.set_in_list(xd, ['qz', 'xv', 'vl',      'gb', 'hd', 'mg', 'vj'])

  def set_in_list(self, module, module_names):
    print(module.name, [m.name for m in module.inputs])
    in_list = [self.modules[name] for name in module_names]
    done = set(in_list)
    for m in module.inputs:
      if m not in done:
        in_list.append(m)
    in_list.reverse()
    assert set(in_list) == set(module.inputs)
    module.in_list = in_list
    print(module.name, '->', [m.name for m in module.in_list])

  def part1(self):
    print('===== Start part 1')
    self.reset()

    if self.doing_sample:
      for m in self.modules.values():
        if m.type == CONJ:
          print('CONJ', m, "===", m.inputs)

    self.counts = {'low': 0, 'high': 0}
    for i in range(1000):
      self.do_button()
    ret = self.counts['low'] * self.counts['high']
    print(self.counts, '=>', ret)
    return ret

  def part2(self):
    if self.doing_sample:
      print('===== sample: skipping part 2')
      return 1

    print('===== Start part 2')
    self.reset()
    self.counts = {'low': 0, 'high': 0}

    ret = 0
    self.show_state()
    while not self.done:
      if ret == 1024 * 16:
        break
      ret += 1
      if ret % 1024 == 0:
        print("press", ret)
      if ret % 1024 == 0 or ret < 1024:
        self.show_state(tag = '%5d' % ret)
      self.do_button(stop_on=self.rx)

    for m in self.modules.values():
      if m.type == CONJ:
        order = m.in_list if m.in_list else m.inputs
        print('CONJ', m.name, [x.name for x in order])
    return ret

  def do_button(self, stop_on=None):
    pulses = deque()
    self.send_pulse(None, self.broadcaster, LOW, pulses)
    while len(pulses) > 0 and not self.done:
      # print(pulses)
      what = pulses.popleft()
      from_m = what[0]
      to_m = what[1]
      pulse = what[2]
      if (stop_on == to_m) and pulse == LOW:
        self.done = True
        return True
      self.send_pulse(from_m, to_m, pulse, pulses)
    return False

  def send_pulse(self, from_m, to_module, pulse, pulses):
    self.counts['high' if pulse else 'low'] += 1
    if to_module.type == CAST:
      for m in to_module.outputs:
        pulses.append((to_module, m, pulse))
      return

    if to_module.type == FF:
      if pulse == HIGH:
        return
      to_module.state = not to_module.state
      for m in to_module.outputs:
        pulses.append((to_module, m, to_module.state))
      return

    if to_module.type == CONJ:
      to_module.inputs[from_m] = pulse
      all_high = True
      for state in to_module.inputs.values():
        if state != HIGH:
          all_high = False
          break
      if all_high:
        pulse = LOW
      else:
        pulse = HIGH
      for m in to_module.outputs:
        pulses.append((to_module, m, pulse))
      return

    assert "can not reach" == 'here'

  def show_state(self, tag=''):
    # print(' '.join([m.short_str() for m in self.state_order]))
    out = []
    for m in self.state_order:
      out.append(m.as_bits())
    print(tag, ''.join(out)) 


day20.sample_test("""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""", expect1=32000000, expect2=None)

day20.sample_test("""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx
""", expect1=11687500, expect2=1)


if __name__ == '__main__':
  day20.run_and_check('input.txt', expect1=711650489, expect2=None)
