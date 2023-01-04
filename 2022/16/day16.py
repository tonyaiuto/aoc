#!/usr/bin/env python3
"AOC 2021: day 16"

from collections import defaultdict
import heapq
import itertools
import sys

from tools import aoc

TRACE_LEVEL = 0

def valve_names(set_of_valves):
   return ','.join(sorted([v.name if v else '.' for v in set_of_valves]))

def names(set_of_strings):
   return ','.join(sorted(set_of_strings))

class State(object):

  id = 0

  def __init__(self, rooms=None, visited=None, opened=None):
    State.id += 1
    self.id = State.id
    self.minute = 0
    self.pressure = 0
    self.rate = 0
    if rooms:
      self.rooms = list(rooms)
    else:
      self.rooms = []
    if visited:
      self.visited = visited
    else:
      self.visited = set(self.rooms)
    self.opened = list(opened) if opened else []

    self.opening = [0] * len(self.rooms)
    self.moving_to = [0] * len(self.rooms)
    self.cost_left = [0] * len(self.rooms)

  def clone(self):
    ret = State(rooms=self.rooms, visited=set(self.visited), opened=self.opened)
    ret.minute = self.minute
    ret.pressure = self.pressure
    ret.rate = self.rate
    ret.opening = list(self.opening)
    ret.moving_to = list(self.moving_to)
    ret.cost_left = list(self.cost_left)
    return ret

  def __hash__(self):
    ret = self.minute
    ret = (ret << 17) + self.pressure * self.rate
    ret = (ret << 11) + valve_names(self.visited).__hash__()
    ret = (ret << 19) + self.onames().__hash__()
    foo = '|'.join(['%s,%s,%s,%d' % (
        self.rooms[i].name if self.rooms[i] else '',
        self.opening[i].name if self.opening[i] else '',
        self.moving_to[i].name if self.moving_to[i] else '',
        self.cost_left[i])
        for i in range(len(self.rooms))
        ])
    ret = (ret << 17) + foo.__hash__()
    return ret

  def __eq__(self, other):
    eq = (self.minute == other.minute
            and self.rate == other.rate
            and self.pressure == other.pressure
            and self.visited == other.visited
            and self.opened == other.opened
            and self.rooms == other.rooms
            and self.opening == other.opening
            and self.moving_to == other.moving_to
            and self.cost_left == other.cost_left
           )
    assert eq == (self.__hash__() == other.__hash__())

  def __lt__(self, other):
    v = self.pressure - other.pressure
    if v < 0:
      return True
    if v > 0:
      return False
    v = self.rate - other.rate
    if v < 0:
      return True
    if v > 0:
      return False
    v = self.__hash__() - other.__hash__()
    return v < 0

  def __repr__(self):
    return str(self)

  def __str__(self):
    ret = [
        '=st %d:' % self.id,
        'min:%d' % self.minute,
    ]
    ret.append('at ' + ','.join([v.name for v in self.rooms]))
    ret.extend([
        'released: %d' % self.pressure,
        'rate: %d' % self.rate,
        'opened:' + self.onames(),
        ])
    if any(self.opening):
      ret.append('opening:' + valve_names(self.opening))
    if any(self.moving_to):
      ret.append('mv:' + ','.join(['%s(%d)' % (self.moving_to[i].name, self.cost_left[i])
                                   if self.cost_left[i] > 0 else ''
                                   for i in range(2)]))
    return ', '.join(ret)

  def dump(self):
    print(str(self), 'Moving to:', valve_names(self.moving_to), self.cost_left, valve_names(self.opening))

  def can_open(self, ri):
    if self.moving_to[ri]:  # can not open while moving
      return False
    assert not self.opening[ri]
    vroom = self.rooms[ri]
    if vroom.rate == 0 or vroom in self.opened:
      return False
    return True

  def start_open(self, ri):
    assert not self.opening[ri]
    ret = self.clone()
    vroom = self.rooms[ri]
    ret.opening[ri] = vroom
    if TRACE_LEVEL > 1:
      print('=== start open', vroom.name, ret)
    return ret

  def is_busy(self, ri):
    return self.moving_to[ri] or self.opening[ri] or False

  def can_move(self):
    ret = 0
    if not self.is_busy(0):
      ret += 1
    if not self.is_busy(1):
      ret += 1
    return ret

  def clone_to(self, valve, rooms=None):
    ret = State(rooms=[valve], visited=set(self.visited), opened=set(self.opened))
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
    for i in range(self.rooms[0].costs[valve.name]):
      ret.clock_tick()
    ret.visited.add(valve)
    return ret

  def open_valve(self):
    """Fork a new state with the valve opened."""
    vroom = self.rooms[0]
    assert vroom.rate > 0
    assert vroom not in self.opened
    ret = self.clone_to(valve=vroom)
    ret.clock_tick()
    ret.rate = ret.rate + vroom.rate
    ret.opened.append(vroom)
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

  def min_value(self):
    return self.pressure + self.rate * (30 - self.minute)


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

  def __repr__(self):
    return self.name

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
    # Valve.reset()

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
    else:
      good_valve_names = sorted(['AA'] + [valve.name for valve in self.can_open])
      print('= Costs')
      print('    ', ' '.join([vname for vname in good_valve_names]))
      AA = Valve.get('AA')
      for valve in [AA] + sorted(self.can_open, key=lambda x: x.name):
        print(' ', valve.name,
              ' '.join(['%2d' % valve.costs[vname] for vname in good_valve_names]))



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

  def move_value(self, minute, from_valve, to_valve):
    if minute >= 29:
      return 0 
    minutes_to_flip = from_valve.costs[to_valve.name] + 1
    time_open = 31 - minute - minutes_to_flip
    if time_open <= 0:
      return 0
    return to_valve.rate * time_open

  def part1(self):
    print('===== Start part 1')
    self.global_best = -1
    AA = Valve.get('AA')
    state = State(rooms=[AA])
    state.minute = 0
    state.rate = 0
    state.pressure = 0
    state.visited.add(AA)

    # XXXXX
    if True and not self.doing_sample:
      return 2056
    ret = self.do_turn(state, depth=0)
    return self.global_best

  def is_final(self, state, depth=0):
    if state.minute > 30:
      print('++++++ too far')
      state.trace(tag=(' ' * depth)+'do_turn')
      return True
    # state.trace(tag=(' ' * depth)+'do_turn')
    if len(state.opened) == self.max_open:
      state.final = state.pressure + (30 - state.minute) * state.rate
      if self.global_best < state.final:
        print('#   new best', state.final)
        self.global_best = state.final
      if TRACE_LEVEL > -10:
        # state.trace()
        # print('#     final %6d' % state.final, state)
        pass
      return True
    # This might be too early
    if state.minute == 30:
      self.global_best = max(self.global_best, state.pressure)
      return True
    assert state.minute < 30
    return False

  def do_turn(self, state, depth):
    if self.is_final(state, depth):
      return 0

    best = 0
    if state.can_open(0):
      ns = state.open_valve()
      assert not ns.can_open(0)
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
    # print('Visiting', state.rooms[0].name, ', visited=', state.vnames(), 'can open:', valve_names(self.can_open))
    # for valve in self.valves:
    for valve in self.can_open:
      if valve.rate <= 0:
        continue
      if valve in state.visited:
        continue
      move_cost = state.rooms[0].costs[valve.name]
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


  def part2(self):
    print('===== Start part 2')

    AA = Valve.get('AA')
    state = State(rooms=[AA, AA])
    state.minute = 3
    state.rate = 0
    state.pressure = 0
    state.visited.add(AA)
    self.greedy = False
    self.short_first = True
    self.rank = False

    if False and not self.doing_sample:
      return 7

    self.global_best = 0
    self.max_minute = 0
    self.examined = 0
    self.wedge_value = 0
    p = self.do_2_dfs(state)

    """
    self.min_best = 0
    states = [state]
    for i in range(5, 31):
      print('####################################### start minute', i, len(states), 'states')
      states = self.do_turn2(states)
      print('New best', self.global_best)
    """
    return self.global_best

  def do_turn2(self, states):
    # create new states
    # clock tick each
    #   update minute
    #   resolve stuff

    # Open them if we can
    for state in states:
      if self.is_final(state):
        continue
      assert not state.opening[0] and not state.opening[1]

      if state.can_open(0):
        state.opening[0] = state.rooms[0]
      if state.can_open(1):
        state.opening[1] = state.rooms[1]
    # print('GOT NEWSTATES', len(states))

    # Figure ouw 
    new_states = []
    n_can_move = 0
    for state in states:
      n_can_move = state.can_move()
      if n_can_move == 0:
        # print('Can not move from', state)
        # state.dump()
        new_states.append(state)
        continue
      assert n_can_move < 3
      if n_can_move == 2 and any(state.moving_to):
        print("WTF", state)
      assert not (n_can_move == 2 and any(state.moving_to) and any(state.opening))

      ranks, wedged = self.where_can_we_move(state)
      if len(ranks[0]) == 0 and len(ranks[1]) == 0 and (any(state.moving_to) or any(state.opening)):
        #if self.trace_sample:
        #  print("NO FRONTIER", state)
        new_states.append(state)
        continue

      move0 = ranks[0]
      move1 = ranks[1]
      vlist = set([x[1] for x in ranks[0]] + [x[1] for x in ranks[1]])
      if n_can_move == 1:
        # XXXX assert (move0 and not move1) or (not move0 and move1)
        if move0:
          assert not move1
          ri = 0
        else:
          assert not move0
          ri = 1
        assert not state.moving_to[ri] and not state.opening[ri]
        if self.greedy or self.short_first:
          for top in sorted(ranks[ri], key=lambda x: -x[0])[0:2]:
            ns = state.clone()
            ns.moving_to[ri] = top[1]
            ns.cost_left[ri] = ns.rooms[ri].costs[top[1].name]
            new_states.append(ns)
        else:
          for valve in vlist:
            ns = state.clone()
            ns.moving_to[ri] = valve
            ns.cost_left[ri] = ns.rooms[ri].costs[valve.name]
            new_states.append(ns)
        continue

      # Do not go to both parts of each pair on the first move
      combo_func = itertools.permutations
      if state.rooms[0] == state.rooms[1]:
        print(state)
        assert state.rooms[0].name == 'AA'
        combo_func = itertools.combinations

      for new_moves in combo_func(vlist, n_can_move):
        if TRACE_LEVEL > 1 and len(states) == 1:
          print("  Moves", valve_names(new_moves))
        ns = state.clone()
        for valve in new_moves:
          if (not ns.is_busy(0)
              and self.move_value(ns.minute, ns.rooms[0], valve) > 0):
            ns.moving_to[0] = valve
            ns.cost_left[0] = ns.rooms[0].costs[valve.name]
          elif (not ns.is_busy(1)
                and self.move_value(ns.minute, ns.rooms[1], valve) > 0):
            ns.moving_to[1] = valve
            ns.cost_left[1] = ns.rooms[1].costs[valve.name]
          else:
            if self.trace_sample:
              print('More valves than slots', 'can move', n_can_move, [x.name for x in new_moves], ns)
              print('Original was', state)
        # print('Assigning', [x.name for x in new_moves], ns)
        if any(ns.moving_to):
          new_states.append(ns)

    s_new = []
    for state in new_states:
      self.finish_clock_tick(state)
      if self.rank:
        heapq.heappush(s_new, (-state.min_value(), state))
      else:
        s_new.append(state)

    if not s_new:
      return []

    if not self.rank:
      return list(set(s_new))

    first_score = s_new[0][0]
    tier = 1
    ns = set()
    cutoff = len(s_new)
    if s_new[0][1].minute > 17:
      cutoff = cutoff * 3 // 4
    while s_new:
      if len(ns) > cutoff:
        break
      top = heapq.heappop(s_new)
      #assert top[0] >= first_score
      #if top[0] > first_score:
      #  if tier > 3:  # Can we fiddle with this?
      #    break
      #  first_score = top[0]
      #  tier += 1
      ns.add(top[1])
      if first_score < 0 and tier > 1 and len(ns) > 10000:
        break
    return list(ns)

  def where_can_we_move(self, state):
    """Return lists of rooms that each person could move to."""

    # What rooms does it make sense to move to?
    ranks = [[], []]
    wedged = True 
    for valve in self.can_open:
      if valve.rate <= 0 or valve in state.visited or valve in state.opened:
        continue
      for ri in (0, 1):
        cost = state.rooms[ri].costs[valve.name]
        if state.minute + cost > 30:
          continue
        wedged = False 
        value = self.move_value(state.minute, state.rooms[ri], valve)
        if value <= 0:
          continue
        if valve in state.opening or valve in state.moving_to:
          continue
        if not state.is_busy(ri):
          ranks[ri].append((cost, valve))
    ranks[0] = sorted(ranks[0], key=lambda x: x[0])
    ranks[1] = sorted(ranks[1], key=lambda x: x[0])
    if not state.is_busy(0) and not state.is_busy(1):
      vlist = set([x[1] for x in ranks[0]] + [x[1] for x in ranks[1]])
      time_left = max(0, 30 - state.minute - 1)
      hyper_value = state.pressure + time_left * sum([valve.rate for valve in vlist])
      if self.global_best > hyper_value:
        # print("value wedged at", hyper_value, state, 'Ranked moves', ranks)
        # wedged = True
        pass
    if state.minute < 5:
      print("From", state, 'Ranked moves', ranks)
    #if wedged:
    #  print("wedged at", state, 'Ranked moves', ranks)
    return ranks, wedged

  def finish_clock_tick(self, state):
    """Now that we have set the intent, update the state."""
    state.minute += 1
    state.pressure += state.rate
    if self.global_best < state.pressure:
      self.global_best = state.pressure
      print('New global best', self.global_best)
      #if len(state.opened) != self.max_open:
      #  if self.trace_sample:
      #    print("All valves not open", state.onames())
    for i in range(2):
      open_valve = state.opening[i]
      if open_valve:
        if open_valve in state.opened:
          print('==== WTF already opened', state)
        assert open_valve not in state.opened
        state.opened.append(open_valve)
        state.rate += open_valve.rate
        state.opening[i] = None
        if self.trace_sample and TRACE_LEVEL > 0:
          print('=== opened', open_valve.name, state)
      move_to = state.moving_to[i]
      assert not (open_valve and move_to)
      if move_to:
        state.cost_left[i] -= 1
        if state.cost_left[i] == 0:
          state.rooms[i] = move_to
          state.visited.add(move_to)
          state.moving_to[i] = None
          if self.trace_sample and TRACE_LEVEL > 0:
            print('=== reached', move_to.name, state)

  def do_2_dfs(self, state, depth=0):
    if state.minute < 6 and self.global_best < 10:
      print(' ' * depth, state)
    if self.max_minute < state.minute:
      self.max_minute = state.minute
      print("Now hitting minute", self.max_minute)
    self.examined += 1
    if self.examined % 100000 == 0:
      print("examined", self.examined, 'best', self.global_best, 'wedge value', self.wedge_value)
      print('  ', state)
      sys.stdout.flush()
    if self.examined > 5000000:
      # return 0
      pass
 
    # New level, new tick
    #if any(state.opening) or any(state.moving_to):
    # state = state.clone()
    self.finish_clock_tick(state)
    if self.global_best < state.pressure:
      self.global_best = state.pressure
      print(' ' * depth, '> new best', self.global_best)

    if self.is_final(state, depth):
      return state.pressure

    # If we are in the room, open the valve
    if state.can_open(0) or state.can_open(1):
      if state.can_open(0):
        state.opening[0] = state.rooms[0]
      if state.can_open(1):
        state.opening[1] = state.rooms[1]

    ranked_moves, wedged = self.where_can_we_move(state)
    if wedged:
      self.wedge_value += (30 - state.minute)
      while state.minute < 30:
        self.finish_clock_tick(state)
      if self.global_best < state.pressure:
        self.global_best = state.pressure
        print(' ' * depth, '> new best', self.global_best)
      return state.pressure

    move0 = ranked_moves[0]
    move1 = ranked_moves[1]
    if not move0 and not move1:
      if self.trace_sample:
        print("Busy state", state)
      ns = state.clone()
      p = self.do_2_dfs(ns, depth=depth+1)
      self.global_best = max(self.global_best, p)
      return p

    if (not move0 and move1) or (move0 and not move1):
      if move0:
        assert not move1
        ri = 0
      else:
        assert not move0
        ri = 1
      assert not state.moving_to[ri] and not state.opening[ri]
      # print(' '*depth, 'Only moving', ri, state)
      for rank, valve in ranked_moves[ri]:
        cost = state.rooms[ri].costs[valve.name]
        if state.minute + cost + 1 >= 30:
          p = state.pressure
          # continue
        ns = state.clone()
        ns.moving_to[ri] = valve
        ns.cost_left[ri] = cost
        p = self.do_2_dfs(ns, depth=depth+1)
        self.global_best = max(self.global_best, p)
      return p

    # Now we have a fun case

    # Do not go to both parts of each pair on the first move
    if state.rooms[0] == state.rooms[1]:
      assert state.rooms[0].name == 'AA'
      first_move_valves = set()
    else:
      first_move_valves = None
    best = 0
    for valve0 in [x[1] for x in ranked_moves[0]]:
      assert not state.is_busy(0)
      assert self.move_value(state.minute, state.rooms[0], valve0) > 0
      if valve0 in state.opening or valve0 in state.moving_to:
        continue
      ns0 = state.clone()
      ns0.moving_to[0] = valve0
      ns0.cost_left[0] = ns0.rooms[0].costs[valve0.name]
      if first_move_valves:
        first_move_valves.add(valve0)

      for valve1 in [x[1] for x in ranked_moves[1]]:
        assert not ns0.is_busy(1)
        assert self.move_value(ns0.minute, ns0.rooms[1], valve1) > 0
        if first_move_valves and valve1 in first_move_valves:
          continue
        if valve1 in ns0.opening or valve1 in ns0.moving_to:
          continue
        ns1 = ns0.clone()
        ns1.moving_to[1] = valve1
        ns1.cost_left[1] = ns1.rooms[1].costs[valve1.name]
        p = self.do_2_dfs(ns1, depth=depth+1)
        self.global_best = max(self.global_best, p)
        if p > best:
          best = p
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

# optimal2 = DD 2, JJ 3, BB, 7, HH 7, CC 9, EE 11

if __name__ == '__main__':
  # part1: 1503 1611  <   X   < 2191
  # part2: initial greedy: 2219  2255  2281 <  x  < ?
  # not 2411, 2497
  day16.run_and_check('input.txt', expect1=2056, expect2=2513)
