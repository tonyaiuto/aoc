#!/usr/bin/env python3
"""AOC 2021: day 19

This does it mostly brute force, by running out lots of states and finding the best.

A better solution would figure out the recurrence relation and compute what is possible.
"""

from tools import aoc


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
    ret = (((self.minute * 37 + self.n_ore) *23 + self.n_clay) * 37 + self.n_obs) * 37 + self.n_geode
    ret = (((        ret * 37 + self.bot_ore) *23 + self.bot_clay) * 37 + self.bot_obs) * 37 + self.bot_geode
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

    ret = 0
    for bp in self.blueprints:
      bp.max_g = 0
      self.do_blueprint(bp)
      print('blueprint', bp.id, 'max g', bp.max_g)
      quality = bp.id * bp.max_g
      ret += quality
    return ret


  def do_blueprint(self, bp):
    future_states = set([State()])
    for i in range(self.max_minute):
      f_new = []
      print('=#### minute', i+1, ', %d future states' % len(future_states))
      max_ore = max_clay = max_obs = max_geode = 0
      for i, state in enumerate(future_states):
        #if i % 5000 == 0:
        #  print("  > future state", i)
        fs = self.do_minute(bp, state)
        for f in fs:
          # print(f)
          if f.n_obs > max_obs:
            max_obs = f.n_obs
            # print('Could have', max_obs, 'obsidian')
          if f.n_geode  > bp.max_g:
            bp.max_g = state.n_geode
            print('Could have', bp.max_g, 'geodes')

          # Do some heuristic pruning or we get too many states
          if f.n_geode <= bp.max_g - 3:  # cull the laggards
            continue
          if f.n_obs > 2 * bp.geode_obs:  # Making obs, but no geodes?
            continue
          if f.n_clay > 2 * bp.obs_clay and f.n_obs == 0:  # Making clay, but no obs?
            continue
          if f.n_ore > 2 * bp.clay_ore and f.n_clay == 0 and f.n_obs == 0:  # Making only ore
            continue
          if f.n_obs < max_obs - 10 and f.bot_geode == 0:
            continue
          f_new.append(f)
        # print('f_new len', len(f_new))
      future_states = set(f_new)


  def do_minute(self, bp, state):
    # DFS bottom out
    if state.minute > self.max_minute:
      print("BOTTOM")
      if state.n_geode  > bp.max_g:
        bp.max_g = state.n_geode
        print('Could have', bp.max_g, 'geodes')
      return

    state.minute += 1
    # print('== minute', state.minute)

    # spend first

    # future_states = set([state])
    future_states = []
    future_states = [state]
    interesting = False
    can_ore = min(state.n_ore // bp.ore_ore, 1)
    if state.n_ore > bp.clay_ore * bp.obs_clay:
      # we are building up too many
      can_ore = 0
    # print('can make ore', can_ore)
    for make_ore in range(0, can_ore + 1):
      assert make_ore == 0 or state.can_make_ore_bot(bp)
      ore_s = State(clone=state)
      future_states.append(ore_s)
      ore_s.n_ore -= bp.ore_ore * make_ore
      ore_s.future_ore += make_ore
      if ore_s.future_ore > 0:
        continue

      can_clay = min(ore_s.n_ore // bp.clay_ore, 1)
      if state.n_clay > 3 * bp.obs_clay:
        # we are building up too many
        can_clay = 0
        # print('can make clay', can_clay)
      for make_clay in range(0, can_clay + 1):
        clay_s = State(clone=ore_s)
        future_states.append(clay_s)
        clay_s.n_ore -= bp.clay_ore * make_clay
        clay_s.future_clay += make_clay
        if clay_s.future_clay > 0:
          continue

        if clay_s.can_make_geode_bot(bp):
          geode_s = State(clone=clay_s)
          future_states.append(geode_s)
          assert geode_s.n_obs >= bp.geode_obs
          geode_s.n_ore -= bp.geode_ore
          geode_s.n_obs -= bp.geode_obs
          geode_s.future_geode = 1
          continue

        if clay_s.n_obs > bp.geode_obs:
          # Stop making more of these
          continue

        if clay_s.can_make_obs_bot(bp):
          obs_s = State(clone=clay_s)
          future_states.append(obs_s)
          obs_s.n_ore -= bp.obs_ore
          obs_s.n_clay -= bp.obs_clay
          obs_s.future_obs = 1
          continue

    ret = []
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
      ret.append(fs)
    # print('generated future states', len(future_states), '=>', len(ret), 'unique.')
    return set(ret)


  def part2(self):
    print('===== Start part 2')
    self.max_minute = 32
    ret = 1
    for bp in self.blueprints[0:3]:
      bp.max_g = 0
      self.do_blueprint(bp)
      print('blueprint', bp.id, 'max g', bp.max_g)
      ret *= bp.max_g
    return ret


day19.sample_test("""
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
""", expect1=33, expect2=3472)


if __name__ == '__main__':
  day19.run_and_check('input.txt', expect1=2193, expect2=7200)
