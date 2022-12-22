#!/usr/bin/env python3
"AOC 2021: day 16"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils

TRACE_LEVEL = 0

def valve_names(set_of_valves):
   return ','.join(sorted([v.name for v in set_of_valves]))

def names(set_of_strings):
   return ','.join(sorted(set_of_strings))

class State(object):

  def __init__(self, valve, visited=None, opened=None):
    self.valve = valve
    self.pressure = 0
    self.visited = visited or set()
    self.opened = opened or set()

  def __hash__(self):
    ret = self.minute
    ret = ret * 37 + self.valve.__hash__()
    ret = ret * 37 + self.pressue.__hash__()
    ret = ret * 37 + self.visited.__hash__()
    ret = ret * 37 + self.opened.__hash__()
    return ret

  def __eq__(self, other):
    return (self.minute == other.minute
            and self.valve == other.valve
            and self.pressure == other.pressure
            and self.visited == other.visited
            and self.opened == other.opened)

  def __str__(self):
    return ', '.join([
        '== minute %d' % self.minute,
        'at ' + self.valve.name,
        'released: %d' % self.pressure,
        'rate: %d' % self.rate,
        'opened:' + self.onames(),
        ])

  def can_open(self, valve):
    return valve.rate > 0 and valve not in self.opened

  def clock_tick(self):
    # self.trace()
    self.minute += 1
    # increase pressure at old rate
    self.pressure += self.rate

  def clone_to(self, valve):
    ret = State(valve, visited=set(self.visited), opened=set(self.opened))
    ret.minute = self.minute
    ret.rate = self.rate
    ret.pressure = self.pressure
    return ret

  def move_to(self, valve):
    ret = self.clone_to(valve)
    # ret.trace(tag='Moving to')
    for i in range(self.valve.costs[valve.name]):
      ret.clock_tick()
    ret.visited.add(valve)
    return ret

  def open_valve(self):
    assert self.valve.rate > 0
    ret = self.clone_to(self.valve)
    ret.clock_tick()
    ret.rate = self.rate + self.valve.rate
    ret.opened.add(self.valve)
    # ret.trace(tag='open_valve')
    return ret

  def vnames(self):
     return ','.join([v.name for v in self.visited])

  def onames(self):
     return ','.join([v.name for v in self.opened])

  def trace(self, tag=None, level=-1):
    if level < TRACE_LEVEL:
      return
    print(tag or '', str(self))


class Valve(object):

  name_to_valve = {}

  def __init__(self, name, rate, tunnels):
    self.name = name
    self.rate = rate
    self.tunnels = tunnels
    self.costs = defaultdict(int)
    Valve.name_to_valve[name] = self

  def __str__(self):
    return '%s: rate=%d, to:%s' % (self.name, self.rate, self.tunnels)

  @staticmethod
  def get(name):
    return Valve.name_to_valve[name]

  @staticmethod
  def reset():
    Valve.name_to_valve = {}

  def comp_dist_to(self, name, visited=None):
    if not visited:
      visited = set()
    # print('comp', self.name, 'to', name)
    if name == self.name:
      return 0
    # memoized
    ret = self.costs.get(name)
    if ret > 0:
      return ret
    target_valve = Valve.get(name)
    if name in self.tunnels:
      self.costs[name] = 1
      target_valve.costs[self.name] = 1
      return 1

    # Ask my directly connected ones for the distance?
    visited.add(self.name)
    for t in self.tun:
      dist = t.costs.get(name) or -1
      if dist > 0:
        self.costs[name] = dist + 1
        target_valve.costs[self.name] = dist + 1
        return dist+1

      if name not in visited:
        print("ASKING CHILD", t.name, 'dist to', target_valve.name)
        dist = t.comp_dist_to(name, visited=visited)
        assert dist > 0
        self.costs[name] = dist + 1
        target_valve.costs[self.name] = dist + 1
        return dist+1


class day16(aoc.aoc):

  def __init__(self):
    super(day16, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.valves = []
    Valve.reset()

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    # Valve AA has flow rate=27; tunnels lead to valves DD, II, BB
    x = line.split(';')
    name = line[6] + line[7]
    x2 = x[0].split('=')
    rate = int(x2[1])
    tunnels = [s.strip() for s in x[1][23:].split(',')]
    v = Valve(name=name, rate=rate, tunnels=tunnels)
    if self.trace > 1:
      print(v)
    self.valves.append(v)

  def post_load(self):
    self.valves = sorted(self.valves, key=lambda x: x.name)
    # turn tunnel names into pointers
    can_open = set()
    for valve in self.valves:
      valve.tun = [Valve.get(tunnel) for tunnel in valve.tunnels]
      if valve.rate > 0:
        can_open.add(valve)
    self.can_open = sorted(can_open, key=lambda x: -x.rate)
    self.max_open = len(self.can_open)
    print('GOOD VALVES', ','.join([v.name for v in self.can_open]))

    self.compute_travel_costs()
    # Sanity check the costs
    for valve in self.valves:
      for vname,cost in valve.costs.items():
        if vname != valve.name:
          # print(valve, vname, cost)
          assert cost > 0


  def compute_travel_costs(self):
    all_valve_names = [v.name for v in self.valves]
    # baseline table
    for valve in self.valves:
      valve.to_get_dist = set(all_valve_names)
      valve.to_get_dist.remove(valve.name)
      for vname in all_valve_names:
        valve.costs[vname] = 0
      for v in valve.tun:
        valve.to_get_dist.remove(v.name)
        valve.costs[v.name] = 1
        # remove?
        v.costs[valve.name] = 1

    did_something = True
    i = 0
    while did_something:
      i = i + 1
      assert i < 20
      did_something = False
      for valve in self.valves:
        # print('LOOP', i, valve.name, 'get', names(valve.to_get_dist))
        for name in set(valve.to_get_dist):
          for v in valve.tun:
            dist = v.costs.get(name, -1)
            if dist > 0:
              # print('  can reach', name, 'via', v.name)
              valve.to_get_dist.remove(name)
              valve.costs[name] = dist + 1
              vv = Valve.get(name)
              vv.costs[valve.name] = dist + 1
              did_something = True
              break

    print('= Costs')
    print('    ', ' '.join([vname for vname in all_valve_names]))
    for valve in self.valves:
      print(' ', valve.name,
            ' '.join(['%2d' % valve.costs[vname] for vname in all_valve_names]))


  def part1(self):
    print('===== Start part 1')
    self.reset()

    AA = Valve.get('AA')
    state = State(AA)
    state.minute = 0
    state.rate = 0
    state.pressure = 0
    state.visited.add(AA)

    ret = self.do_turn(state, depth=0)
    return ret

  def do_turn(self, state, depth):
    if state.minute > 30:
      print('++++++ too far')
      state.trace(tag=(' ' * depth)+'do_turn')
      return -1
    # state.trace(tag=(' ' * depth)+'do_turn')

    if len(state.opened) == self.max_open:
      final = state.pressure + (30 - state.minute) * state.rate
      if TRACE_LEVEL > -10:
        # state.trace()
        print('     final %6d' % final, state)
      return final

    if state.minute == 30:
      return state.pressure
    assert state.minute < 30

    best = 0
    if state.can_open(state.valve):
      ns = state.open_valve()
      # ns.trace('    just opened')
      # try again with the valve open
      p = self.do_turn(ns, depth=depth+1)
      if p > best:
        best = p
      return best  # XXX

    p = self.visit_valves(state, depth=depth+1)
    if p > best:
      best = p
    return best


  def visit_valves(self, state, depth):
    best = 0
    # print('Visiting', state.valve.name, ', visited=', state.vnames())
    for valve in self.can_open:
      if valve in state.visited:
         continue
      move_cost = state.valve.costs[valve.name]
      if state.minute + move_cost >= 30:
        p = state.pressure + (30 - state.minute) * state.rate
        # print('RUN OUT CLOCK =>', p, 'or maybe', p + state.rate)
      else:
        ns = state.move_to(valve)
        p = self.do_turn(ns, depth=depth+1)
      if p > best:
        best = p
    return best

  def visit_children(self, state, depth):  # OBS
    best = 0
    print('Visiting', state.valve.name, ', visited=', state.vnames())
    for tunnel in state.valve.tun:
      if tunnel in state.visited:
         continue
      ns = state.move_to(tunnel)
      p = self.do_turn(ns, depth=depth+1)
      if p > best:
        best = p
    return best

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day16.sample_test("""
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""", expect1=1651, expect2=None)


if __name__ == '__main__':
  # part1: 1503  to low
  # part1: 1611  to low
  day16.run_and_check('input.txt', expect1=111, expect2=None)
