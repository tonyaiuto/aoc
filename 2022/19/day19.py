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
        self.id, self.ore, self.clay, self.obs_ore, self.obs_clay, self.geode_ore, self.geode_clay)

  @staticmethod
  def from_str(s):
    parts = s.split(':')
    id = int(parts[0][10:])
    ret = Blueprint(id)
    robots = parts[1].strip().split('.')
    # Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
    ret.ore = int(robots[0].strip().split(' ')[4])
    ret.clay = int(robots[1].strip().split(' ')[4])
    ret.obs_ore = int(robots[2].strip().split(' ')[4])
    ret.obs_clay = int(robots[2].strip().split(' ')[7])
    ret.geode_ore = int(robots[3].strip().split(' ')[4])
    ret.geode_clay = int(robots[3].strip().split(' ')[7])
    return ret


class State(object):
   
  def __init__(self, clone=None):
    if clone:
      self.minute = self.minute
      self.n_ore = self.n_ore
      self.n_clay = self.n_ore
      self.n_obs = self.n_obs
      self.n_geode = self.n_geode
      self.bot_ore = self.bot_ore
      self.bot_clay = self.bot_clay
      self.bot_obs = self.bot_obs
      self.bot_geode = self.bot_geode
    self.minute = 0
    self.n_ore = 1
    self.n_clay = 0
    self.n_obs = 0
    self.n_geode = 0
    self.bot_ore = 0
    self.bot_clay = 0
    self.bot_obs = 0
    self.bot_geode = 0

  def __hash__(self):
    ret = self.minute
    ret = ret * 100 + self.n_ore
    ret = ret * 100 + self.n_clay
    ret = ret * 100 + self.n_obs
    ret = ret * 100 + self.n_geode
    ret = ret * 100 + self.bot_ore
    ret = ret * 100 + self.bot_clay
    ret = ret * 100 + self.bot_obs
    ret = ret * 100 + self.bot_geode
    return ret

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
        ])

  def mine(self):
    # Do the mining
    self.n_ore += self.bot_ore
    self.n_clay += self.bot_clay
    self.n_obs += self.bot_obs
    self.n_geode += self.bot_geode


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
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()

    bp = self.blueprints[0]
    state = State()
    self.do_minute(bp, state)

    # blueprint id * max geodes
    return 42


  def do_minute(self, bp, state):
    state.minute += 1
    print('== minute', state.minute)
    # spend first
 
    while state.n_ore >= bp.geode_ore and state.n_geode >= bp.geode_clay:
      state.n_ore -= bp.geode_ore
      state.n_geode >= bp.geode_clay
      state.bot_geode += 1

    while state.n_ore >= bp.obs_ore and state.n_geode >= bp.obs_clay:
      state.n_ore -= bp.obs_ore
      state.n_geode >= bp.obs_clay
      state.bot_obs += 1

    while state.n_ore >= bp.clay:
      state.n_ore -= bp.clay
      state.bot_clay += 1

    while state.n_ore >= bp.ore:
      state.n_ore -= bp.clay
      state.bot_ore += 1

    can_ore = state.n_ore // bp.ore
    can_clay = state.n_ore // bp.clay

    state.mine()
    print(' ', state)


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
