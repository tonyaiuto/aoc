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
   return ','.join(sorted([v.name if v else '.' for v in set_of_valves]))

def names(set_of_strings):
   return ','.join(sorted(set_of_strings))

class State(object):

  def __init__(self, valve=None, rooms=None, visited=None, opened=None):
    self.minute = 0
    self.valve = valve
    self.pressure = 0
    self.rate = 0
    self.visited = visited or set([valve])
    self.opened = opened or set()
    self.rooms = rooms or []
    self.moving_to = [0] * len(self.rooms)
    self.cost_left = [0] * len(self.rooms)
    self.opening = [0] * len(self.rooms)

  def clone(self):
    ret = State(rooms=self.rooms, visited=set(self.visited), opened=set(self.opened))
    ret.minute = self.minute
    ret.valve = self.valve
    ret.pressure = self.pressure
    ret.rate = self.rate
    ret.moving_to = list(self.moving_to)
    ret.cost_left = list(self.cost_left)
    ret.opening = list(self.opening)
    return ret

  def __hash__(self):
    ret = self.minute
    ret = ret * 37 + self.valve.__hash__()
    ret = ret * 73 + self.pressue.__hash__()
    ret = ret * 101 + self.visited.__hash__()
    ret = ret * 19 + self.opened.__hash__()
    ret = ret * 37 + self.rooms.__hash__()
    ret = ret * 37 + self.moving_to.__hash__()
    ret = ret * 37 + self.cost_left.__hash__()
    ret = ret * 37 + self.opening.__hash__()
    return ret

  def __eq__(self, other):
    return (self.minute == other.minute
            and self.valve == other.valve
            and self.pressure == other.pressure
            and self.visited == other.visited
            and self.opened == other.opened
            and self.rooms == other.rooms
            and self.moving_to == other.moving_to
            and self.cost_left == other.cost_left
            and self.opening == other.opening
           )

  def can_move(self):
    ret = 0
    for i in range(2):
      if not self.moving_to[i] and not self.opening[i]:
        ret += 1
    return ret

  def __str__(self):
    ret = [
        '== minute %d' % self.minute,
    ]
    if self.rooms:
        ret.append('at ' + ','.join([v.name for v in self.rooms]))
    else:
        ret.append('at ' + self.valve.name)
    ret.extend([
        'released: %d' % self.pressure,
        'rate: %d' % self.rate,
        'opened:' + self.onames(),
        ])
    return ', '.join(ret)

  def dump(self):
    print(str(self), 'Moving to:', valve_names(self.moving_to), self.cost_left, valve_names(self.opening))

  def can_open_self(self):
    return self.valve.rate > 0 and self.valve not in self.opened

  def clone_to(self, valve, rooms=None):
    ret = State(valve, visited=set(self.visited), opened=set(self.opened))
    ret.minute = self.minute
    ret.rate = self.rate
    ret.pressure = self.pressure
    return ret

  def clock_tick(self):
    # self.trace()
    self.minute += 1
    self.pressure += self.rate

  def move_to(self, valve):
    ret = self.clone_to(valve)
    # ret.trace(tag='Moving to')
    for i in range(self.valve.costs[valve.name]):
      ret.clock_tick()
    ret.visited.add(valve)
    return ret

  def open_valve(self):
    assert self.valve.rate > 0
    assert self.valve not in self.opened
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
    all_valve_names = [v.name for v in self.valves]
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
    if self.trace_sample:
      print('= Costs')
      print('    ', ' '.join([vname for vname in all_valve_names]))
      for valve in self.valves:
        print(' ', valve.name,
              ' '.join(['%2d' % valve.costs[vname] for vname in all_valve_names]))

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
        # XXX v.costs[valve.name] = 1

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
            # if dist > 0:
            if dist == i:
              # print('  can reach', name, 'via', v.name)
              valve.to_get_dist.remove(name)
              valve.costs[name] = dist + 1
              vv = Valve.get(name)
              # vv.costs[valve.name] = dist + 1
              did_something = True
              break


  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.global_best = 0
    AA = Valve.get('AA')
    state = State(AA)
    state.minute = 0
    state.rate = 0
    state.pressure = 0
    state.visited.add(AA)

    ret = self.do_turn(state, depth=0)
    return self.global_best

  def is_final(self, state, depth=0):
    if state.minute > 30:
      print('++++++ too far')
      state.trace(tag=(' ' * depth)+'do_turn')
      return True
    # state.trace(tag=(' ' * depth)+'do_turn')
    if len(state.opened) == self.max_open:
      final = state.pressure + (30 - state.minute) * state.rate
      self.global_best = max(self.global_best, final)
      if TRACE_LEVEL > -10:
        # state.trace()
        print('     final %6d' % final, state)
      return True
    if state.minute == 30:
      self.global_best = max(self.global_best, state.pressure)
      return True
    assert state.minute < 30
    return False

  def do_turn(self, state, depth):
    if self.is_final(state, depth):
      return 0

    best = 0
    if state.can_open_self():
      ns = state.open_valve()
      assert not ns.can_open_self()
      # ns.trace('    just opened')
      # try again with the valve open
      p = self.do_turn(ns, depth=depth+1)
      self.global_best = max(self.global_best, p)
      if p > best:
        best = p
      return best  # XXX

    p = self.visit_valves(state, depth=depth+1)
    self.global_best = max(self.global_best, p)
    if p > best:
      best = p
    return best


  def visit_valves(self, state, depth):
    best = 0
    # print('Visiting', state.valve.name, ', visited=', state.vnames(), 'can open:', valve_names(self.can_open))
    # for valve in self.valves:
    for valve in self.can_open:
      if valve.rate <= 0:
        continue
      if valve in state.visited:
        continue
      move_cost = state.valve.costs[valve.name]
      if state.minute + move_cost > 30:
        p = state.pressure + (30 - state.minute) * state.rate
        # print('RUN OUT CLOCK =>', p, 'or maybe', p + state.rate)
      else:
        ns = state.move_to(valve)
        p = self.do_turn(ns, depth=depth+1)
      self.global_best = max(self.global_best, p)
      if p > best:
        best = p
    return best

  def XXXvisit_children(self, state, depth):  # OBS
    best = 0
    print('Visiting', state.valve.name, ', visited=', state.vnames())
    for tunnel in state.valve.tun:
      if tunnel in state.visited:
         continue
      ns = state.move_to(tunnel)
      p = self.do_turn(ns, depth=depth+1)
      self.global_best = max(self.global_best, p)
      if p > best:
        best = p
    return best

  def part2(self):
    print('===== Start part 2')
    self.reset()
    # return 1707

    AA = Valve.get('AA')
    state = State(rooms=[AA, AA])
    state.minute = 4
    state.rate = 0
    state.pressure = 0
    state.visited.add(AA)

    self.global_best = 0
    states = [state]
    for i in range(26):
      states = self.do_turn2(states)
    return self.global_best

  def do_turn2(self, states, depth=0):

    # create new states
    # clock tick each
    #   update minute
    #   resolve stuff

    best = 0
    new_states = []
    for state in states:
      if self.is_final(state):
        continue
      new_states.append(state)
      for i, valve_room in enumerate(state.rooms):
        opn = list(state.opening)
        if (valve_room.rate > 0
            and valve_room not in state.visited
            and valve_room not in opn):
          ns = state.clone()
          ns.opening[i] = valve_room
          opn.append(valve_room)
          print('=== TO OPEN', valve_room.name, ns)
          new_states.append(ns)

    state = new_states
    new_states = []
    n_can_move = 0
    for state in states:
      n_can_move = state.can_move()
      if n_can_move == 0:
        # print('Can not move from', state)
        state.dump()
        new_states.append(state)
        continue

      # state.dump()

      # p = self.visit_valves2(state, depth=depth+1)
      vlist = []
      for valve in self.can_open:
        if valve.rate <= 0 or valve in state.visited:
          continue
        if valve in state.opening or valve in state.moving_to:
          continue
        # print("  We could move to valve", valve)
        vlist.append(valve)

      for new_moves in itertools.permutations(vlist, n_can_move):
        print('Assigning', [x.name for x in new_moves])

        ns = state.clone()
        for valve in new_moves:
          if not ns.moving_to[0] and not ns.opening[0]:
            ns.moving_to[0] = valve
            ns.cost_left[0] = ns.rooms[i].costs[valve.name]
          elif not ns.moving_to[1] and not ns.opening[1]:
            ns.moving_to[1] = valve
            ns.cost_left[1] = ns.rooms[i].costs[valve.name]
          else:
            print('More valves than slots', [x.name for x in new_moves], ns)
        new_states.append(ns)

    for state in new_states:
      state.minute += 1
      state.pressure += state.rate
      self.global_best = max(self.global_best, state.pressure)
      for i in range(2):
        open_valve = state.opening[i]
        if open_valve:
          state.opened.add(open_valve)
          state.rate += open_valve.rate
          state.opening[i] = None
          print('=== opened', open_valve.name)
        move_to = state.moving_to[i]
        if move_to:
          state.cost_left[i] -= 1
          if state.cost_left[i] == 0:
            state.rooms[i] = move_to
            state.visited.add(move_to)
            state.moving_to[i] = None
            print('=== reached', move_to.name, 'rate, p', state.rate, state.pressure)

    return new_states

  def visit_valves2(self, state, depth):
    best = 0
    # print('Visiting', state.valve.name, ', visited=', state.vnames(), 'can open:', valve_names(self.can_open))

    """
      if state.minute + move_cost > 30:
        p = state.pressure + (30 - state.minute) * state.rate
        # print('RUN OUT CLOCK =>', p, 'or maybe', p + state.rate)
      else:
        ns = state.move_to(valve)
        p = self.do_turn2(ns, depth=depth+1)
      self.global_best = max(self.global_best, p)
      if p > best:
        best = p
    """
    return best


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
""", expect1=1651, expect2=1707)


if __name__ == '__main__':
  # part1: 1503 1611  <   X   < 2191
  day16.run_and_check('input.txt', expect1=2056, expect2=None)
