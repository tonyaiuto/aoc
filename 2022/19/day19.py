#!/usr/bin/env python3
"AOC 2021: day 19"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Blueprint(object):

  def __init__(self, id):
    self.id = id

  def __str__(self):
    return 'bp %2d: ore=%d, clay=%d os=%2d,%2d geode=%2d,%2d' % (
        self.id, self.ore_ore, self.clay_ore, self.obs_ore, self.obs_clay, self.geode_ore, self.geode_obs)

  @staticmethod
  def from_str(s):
    parts = s.split(':')
    id = int(parts[0][10:])
    ret = Blueprint(id)
    robots = parts[1].strip().split('.')
    # Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
    ret.ore_ore = int(robots[0].strip().split(' ')[4])
    ret.clay_ore = int(robots[1].strip().split(' ')[4])
    ret.obs_ore = int(robots[2].strip().split(' ')[4])
    ret.obs_clay = int(robots[2].strip().split(' ')[7])
    ret.geode_ore = int(robots[3].strip().split(' ')[4])
    ret.geode_obs = int(robots[3].strip().split(' ')[7])
    return ret


class State(object):
   
  def __init__(self, clone=None):
    self.future_ore = 0
    self.future_clay = 0
    self.future_obs = 0
    self.future_geode = 0
    if clone:
      self.minute = clone.minute
      self.n_ore = clone.n_ore
      self.n_clay = clone.n_clay
      self.n_obs = clone.n_obs
      self.n_geode = clone.n_geode
      self.bot_ore = clone.bot_ore
      self.bot_clay = clone.bot_clay
      self.bot_obs = clone.bot_obs
      self.bot_geode = clone.bot_geode
      return

    self.minute = 0
    self.n_ore = 0
    self.n_clay = 0
    self.n_obs = 0
    self.n_geode = 0
    self.bot_ore = 1
    self.bot_clay = 0
    self.bot_obs = 0
    self.bot_geode = 0

  def __hash__(self):
    ret = self.minute
    ret = 0
    ret = ret * 100 + self.n_ore
    ret = ret * 100 + self.n_clay
    ret = ret * 100 + self.n_obs
    ret = ret * 100 + self.n_geode
    ret = ret * 100 + self.bot_ore
    ret = ret * 100 + self.bot_clay
    ret = ret * 100 + self.bot_obs
    ret = ret * 100 + self.bot_geode
    return ret

  def __eq__(self, other):
    return (
        # self.minute == other.minute
        self.n_ore == other.n_ore
        and self.n_clay == other.n_clay
        and self.n_obs == other.n_obs
        and self.n_geode == other.n_geode
        and self.bot_ore == other.bot_ore
        and self.bot_clay == other.bot_clay
        and self.bot_obs == other.bot_obs
        and self.bot_geode == other.bot_geode
        )

  def __str__(self):
    return ', '.join([
        'min: %d' % self.minute,
        'ore: %d' % self.n_ore,
        'clay: %d' % self.n_clay,
        'obsidian: %d' % self.n_obs,
        'geode: %d' % self.n_geode,
        'bot_ore: %d' % self.bot_ore,
        'bot_clay: %d' % self.bot_clay,
        'bot_obs: %d' % self.bot_obs,
        'bot_geode: %d' % self.bot_geode,
        'f_ore: %d' % self.future_ore,
        'f_clay: %d' % self.future_clay,
        ])

  def mine(self, trace=False):
    # Do the mining
    if trace:
      print('Mining:', self)
    self.n_ore += self.bot_ore
    self.n_clay += self.bot_clay
    self.n_obs += self.bot_obs
    self.n_geode += self.bot_geode
    if trace:
      print('   =>', self)
 
  def can_make_ore_bot(self, bp):
    return self.n_ore >= bp.ore_ore

  def can_make_clay_bot(self, bp):
    return self.n_ore >= bp.clay_ore

  def can_make_obs_bot(self, bp):
    return self.n_ore >= bp.obs_ore and self.n_clay >= bp.obs_clay

  def can_make_geode_bot(self, bp):
    return self.n_ore >= bp.geode_ore and self.n_obs >= bp.geode_obs


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
    self.blueprints = []
    self.max_minute = 24

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    blueprint = Blueprint.from_str(line)
    print(blueprint)
    self.blueprints.append(blueprint)

  def post_load(self):
    # called after all input is read

    for ore_rate in range(1, 6):
      n_ore = 1
      tot = 0
      to_build = 0
      for m in range(1, 25):
        # buy more
        while tot > 0 and tot % ore_rate == 0:
          tot -= ore_rate
          to_build += 1
        tot += n_ore
        # now fully made
        n_ore += to_build
      print('Max ore for', ore_rate, 'is', tot)

    for bp in self.blueprints:
      # need per geode
      need_clay = bp.geode_obs * bp.obs_clay
      need_ore = bp.geode_ore + need_clay * bp.clay_ore
      print('blueprint', bp.id, 'ore/geode:', need_ore)

  def part1(self):
    print('===== Start part 1')
    self.reset()

    best_geode = 0
    best_id = -1
    for bp in self.blueprints[0:1]:
      bp.max_g = 0
      self.do_blue(bp)
      if bp.max_g > best_geode:
        best_geode = bp.max_g
        best_id = bp.id

    # blueprint id * max geodes
    return best_id * best_geode


  def do_blue(self, bp):
    future_states = set([State()])
    for i in range(25):
      f_new = set()
      print('=#### minute', i, ', %d future states' % len(future_states))
      for state in future_states:
        fs = self.do_minute(bp, state)
        for f in fs:
          # print(f)
          f_new.add(f)
        # print('f_new len', len(f_new))
      future_states = f_new


  def do_minute(self, bp, state):
    # DFS bottom out
    if state.minute > self.max_minute:
      print("BOTTOM")
      if state.n_geode  > bp.max_g:
        bp.max_g = state.n_geode
      return

    state.minute += 1
    # print('== minute', state.minute)

    # spend first

    # future_states = set([state])
    future_states = [state]
    can_ore = state.n_ore // bp.ore_ore
    interesting = False
    for make_ore in range(0, can_ore + 1):
      # print('can make ore', can_ore)
      assert make_ore == 0 or state.can_make_ore_bot(bp)
      ore_s = State(clone=state)
      future_states.append(ore_s)
      ore_s.n_ore -= bp.ore_ore * make_ore
      ore_s.future_ore += make_ore

      can_clay = ore_s.n_ore // bp.clay_ore
      # print('can make clay', can_clay)
      for make_clay in range(0, can_clay + 1):
        clay_s = State(clone=ore_s)
        future_states.append(clay_s)
        clay_s.n_ore -= bp.clay_ore * make_clay
        clay_s.future_clay += make_clay

        # If we can not make either obs or geode, do not create new spurious states
        can_obs = min(clay_s.n_ore // bp.obs_ore, clay_s.n_clay // bp.obs_clay)
        can_geode = min(clay_s.n_ore // bp.geode_ore, clay_s.n_clay // bp.geode_obs)
        if can_obs == 0 and can_geode == 0:
          continue

        for make_obs in range(0, can_obs + 1):
          obs_s = State(clone=clay_s)
          future_states.append(obs_s)
          obs_s.n_ore -= bp.obs_ore * make_obs
          obs_s.n_clay -= bp.obs_clay * make_obs
          obs_s.future_obs += make_obs

          # only create new states if you can make one
          can_geode = min(obs_s.n_ore // bp.geode_ore, obs_s.n_obs // bp.geode_obs)
          if can_geode > 0:
            for make_geode in range(0, can_geode + 1):
              geode_s = State(clone=obs_s)
              future_states.append(geode_s)
              assert geode_s.n_obs >= bp.geode_obs * make_geode
              geode_s.n_ore -= bp.geode_ore * make_geode
              geode_s.n_obs -= bp.geode_obs * make_geode
              geode_s.future_geode += make_geode

    ret = set()
    for fs in future_states:
      # fs.mine(trace=fs.future_geode > 0)
      fs.mine()
      fs.bot_ore += fs.future_ore
      fs.bot_clay += fs.future_clay
      fs.bot_obs += fs.future_obs
      fs.bot_geode += fs.future_geode
      #if fs.future_geode > 0:
      #  print('   f>', fs)

      fs.future_ore = 0
      fs.future_clay = 0
      fs.future_obs = 0
      fs.future_geode = 0
      ret.add(fs)
    # print('generated future states', len(future_states), '=>', len(ret), 'unique.')
    return ret


    """ XXXXX
    while state.can_make_clay_bot(bp):
      state.n_ore -= bp.clay
      state.bot_clay += 1

    while state.can_make_ore_bot(bp):
      s = State(clone=state)
      s.n_ore -= bp.clay
      s.bot_ore += 1
      r = self.dp_minute(bp, s)
    """


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day19.sample_test("""
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
""", expect1=33, expect2=None)


if __name__ == '__main__':
  day19.run_and_check('input.txt', expect1=None, expect2=None)
