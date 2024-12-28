#!/usr/bin/env python3
"AOC 2023: day 21"

from collections import defaultdict
import sys

from tools import aoc
from tools import gridutils

VERBOSE = 1

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

numeric_map = {
 0: { 1: {'^<'}, 2: {'^'}, 3: {'^>', '>^'}, 4: {'^^<', '^<^'}, 5: {'^^'}, 6: {'^^>', '>^^', '^>^'},
      7: {'^^^<', '^^<^', '^<^^'}, 8: {'^^^'}, 9: {'>^^^', '^^^>', '^>^^', '^^>^'}, 10: {'>'} },
 1: { 0: {'>v'}, 2: {'>'}, 3: {'>>'}, 4: {'^'}, 5: {'^>', '>^'}, 6: {'^>>', '>>^', '>^>'},
      7: {'^^'}, 8: {'^^>', '>^^', '^>^'}, 9: {'^^>>', '^>>^', '^>^>', '>>^^', '>^^>', '>^>^'},
     10: {'>>v', '>v>'} },
 2: { 0: {'v'}, 1: {'<'}, 3: {'>'}, 4: {'^<', '<^'}, 5: {'^'}, 6: {'^>', '>^'},
      7: {'^^<', '<^^', '^<^'}, 8: {'^^'}, 9: {'^^>', '>^^', '^>^'}, 10: {'v>', '>v'} },
 3: { 0: {'v<', '<v'}, 1: {'<<'}, 2: {'<'}, 4: {'^<<', '<<^', '<^<'}, 5: {'^<', '<^'}, 6: {'^'},
      7: {'<^^<', '<^<^', '^^<<', '<<^^', '^<^<', '^<<^'}, 8: {'^^<', '<^^', '^<^'}, 9: {'^^'}, 10: {'v'} },
 4: { 0: {'v>v', '>vv'}, 1: {'v'}, 2: {'v>', '>v'}, 3: {'v>>', '>>v', '>v>'}, 5: {'>'}, 6: {'>>'},
      7: {'^'}, 8: {'^>', '>^'}, 9: {'>>^', '^>>', '>^>'},
     10: {'>>vv', '>v>v', '>vv>', 'v>>v', 'v>v>' } },

 5: { 0: {'vv'}, 1: {'v<', '<v'}, 2: {'v'}, 3: {'v>', '>v'}, 4: {'<'}, 6: {'>'},
      7: {'^<', '<^'}, 8: {'^'}, 9: {'^>', '>^'}, 10: {'vv>', 'v>v', '>vv'} },
 6: { 0: {'<vv', 'v<v', 'vv<'}, 1: {'<<v', 'v<<', '<v<'}, 2: {'v<', '<v'}, 3: {'v'}, 4: {'<<'}, 5: {'<'},
      7: {'^<<', '<<^', '<^<'}, 8: {'^<', '<^'}, 9: {'^'}, 10: {'vv'} },
 7: { 0: {'v>vv', '>vvv', 'vv>v'}, 1: {'vv'}, 2: {'vv>', 'v>v', '>vv'},
      3: {'>>vv', 'vv>>', 'v>>v', 'v>v>', '>v>v', '>vv>'},
      4: {'v'}, 5: {'v>', '>v'}, 6: {'v>>', '>>v', '>v>'}, 8: {'>'}, 9: {'>>'},
      10: {'>>vvv', '>v>vv', '>vv>v', '>vvv>', 'v>>vv', 'v>v>v', 'v>vv>', 'vv>>v', 'vv>v>'} },
 8: { 0: {'vvv'}, 1: {'<vv', 'v<v', 'vv<'}, 2: {'vv'}, 3: {'vv>', 'v>v', '>vv'}, 4: {'v<', '<v'}, 5: {'v'},
      6: {'v>', '>v'}, 7: {'<'}, 9: {'>'}, 10: {'vvv>', 'vv>v', 'v>vv', '>vvv'} },
 9: { 0: {'vvv<', 'v<vv', 'vv<v', '<vvv'}, 1: {'vv<<', '<<vv', 'v<v<', '<vv<', '<v<v', 'v<<v'},
      2: {'<vv', 'v<v', 'vv<'}, 3: {'vv'}, 4: {'<<v', 'v<<', '<v<'}, 5: {'v<', '<v'}, 6: {'v'},
      7: {'<<'}, 8: {'<'}, 10: {'vvv'} },
10: { 0: {'<'}, 1: {'^<<', '<^<'}, 2: {'^<', '<^'}, 3: {'^'}, 4: {'<^^<', '<^<^', '^<^<', '^<<^', '^^<<'},
      5: {'^^<', '<^^', '^<^'}, 6: {'^^'},
      7: {'^^^<<', '^^<^<', '^^<<^', '^<^^<', '^<^<^', '^<<^^', '<^^^<', '<^^<^', '<^<^^'},
      8: {'<^^^', '^^<^', '^^^<', '^<^^'}, 9: {'^^^'} },
}

def check_path_map():
  for key in range(11):
    for other in range(key+1, 11):
      from_paths = numeric_map[key][other]
      back_paths = numeric_map[other][key]
      if len(from_paths) != len(back_paths):
        print('mismatch # paths', key, other, from_paths, back_paths)
        sys.exit(1)
      for p in from_paths:
        rev = p[::-1]
        if '^' in rev:
          need = rev.replace('^', 'v')
        else:
          need = rev.replace('v', '^')
        if '>' in need:
          need = need.replace('>', '<')
        else:
          need = need.replace('<', '>')
        if need not in back_paths:          
          print('no back path', key, other, need, back_paths)
          sys.exit(1)


def make_numeric_shortest_map():
  map = {}
  for key in range(0, 11):
    map[key] = {}
  map[0][10] = set(['>'])
  map[0][2] = set(['^'])
  map[0][5] = set(['^^'])
  map[0][8] = set(['^^^'])
  # map[1][0] = set(['>v'])
  # map[1][10] = set(['>>v', '>v>'])
  map[2][0] = set(['v'])
  map[5][0] = set(['vv'])
  map[8][0] = set(['vvv'])
  map[10][0] = set(['<'])
  map[3][10] = set(['v'])
  map[6][10] = set(['vv'])
  map[9][10] = set(['vvv'])
  map[10][3] = set(['^'])
  map[10][6] = set(['^^'])
  map[10][9] = set(['^^^'])
  for key in range(1, 10):
    if key % 3 == 1:  # 1, 4, 7
      map[key].update({key+1: set(['>']), key+2: set(['>>'])})
      if key + 4 <= 9:
        map[key][key+4] = set(['>^', '^>'])
      if key + 7 <= 9:
        map[key][key+7] = set(['>^^', '^>^', '^^>'])
    elif key % 3 == 2:  # 2, 6, 8
      map[key].update({key-1: set(['<']), key+1: set(['>'])})
      if key + 4 <= 9:
        map[key][key+4] = set(['>^', '^>'])
      if key + 7 <= 9:
        map[key][key+7] = set(['>^^', '^>^', '^^>'])
      if key + 2 <= 9:
        map[key][key+2] = set(['<^', '^<'])
      if key + 5 <= 9:
        map[key][key+5] = set(['<^^', '^<^', '^^<'])
    else:  # 3, 6, 9
      map[key].update({key-1: set(['<']), key-2: set(['<<'])})
      if key + 2 <= 9:
        map[key][key+2] = set(['<^', '^<'])
      if key + 5 <= 9:
        map[key][key+5] = set(['<^^', '^<^', '^^<'])

    if (key-1) //  3 == 0:
      map[key].update({key+3: set(['^']), key+6: set(['^^'])})
    elif (key-1) // 3 == 1:
      map[key].update({key+3: set(['^']), key-3: set(['v'])})
    elif (key-1) // 3 == 2:
      map[key].update({key-3: set(['v']), key-6: set(['vv'])})

  print_map(map)
  """
  for key in range(0, 11):
    directs = map[key].keys()
    for ok in range(0, 11):
      if ok not in directs:
        map[key][ok] = set()
  """

  """
  for key in range(0, 11):
    my_moves = dict(map[key])
    directs = list(map[key].keys())
    for direct in directs:
      # Who can I reach from things I can reach directly?
      for other_key, moves_to in map[direct].items():
        if key == other_key or other_key in directs:
          continue
        print("looking for way from", key, "to", other_key, "via", direct)
        for first_move in my_moves[direct]:
          for second_move in map[direct][other_key]:
            new_moves = first_move + second_move
            new_len = len(new_moves)
            if new_len > 5:
              continue
            # is this better than my existing moves from key to other_key?
            old_moves = map[key].get(other_key) or set()
            if old_moves:
              cur_path_len = min([len(path) for path in old_moves])
            else:
              cur_path_len = new_len + 1
            if new_len > cur_path_len:
              continue
            if new_len == cur_path_len:
              map[key][other_key].add(new_moves)
              print("Adding path from", key, "to", other_key, 'via', direct, new_moves)
            else:
              assert new_len < cur_path_len
              map[key][other_key] = set([new_moves])
              print("Replacing path from", key, "to", other_key, 'via', direct, new_moves)
  """
  """
    for to_key in range(key+1, 11):
      to_moves = my_moves.get(to_key)
      if to_moves:
        # I can reach to_key with these moves.
        # what can I reach from that
        for move in to_moves:
          map[to_key]
        for moves 
    
    done = set(map[key].keys())
    for to_key in range(11):
      if to_key in mk:
        if k
        continue
  """
  print_map(map)

def print_map(map):
  for key in range(11):
    m = map[key]
    print(
        '%2d: {' % key,
        ', '.join(['%d: %s' % (k, m[k]) for k in sorted(m.keys())]),
        '},'
    )


"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
dir_map = {
  'A': {'<': ['<v<','v<<'], '>': ['v'], '^': ['<'],        'v': ['<v','v<']},
  '^': {'<': ['v<'], '>': ['v>', '>v'],                    'v': ['v'], 'A': ['>']},
  'v': {'<': ['<'],  '>': ['>'],        '^': ['^'],                    'A': ['^>', '>^']},
  '<': {             '>': ['>>'],       '^': ['>^'],       'v': ['>'], 'A': ['>>^', '>^>']},
  '>': {'<': ['<<'],                    '^': ['^<', '<^'], 'v': ['<'], 'A': ['^']},
}



class day21(aoc.aoc):

  def __init__(self):
    super(day21, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.codes = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.codes.append(line)

  def post_load(self):
    # called after all input is read
    # make_numeric_shortest_map()
    check_path_map()


  def find_presses(self, cur_button, new_button):
    return numeric_map[cur_button][new_button]


  def part1(self):
    print('===== Start part 1')
    self.reset()
    want = set(['<A^A>^^AvvvA', '<A^A^>^AvvvA', '<A^A^^>AvvvA'])
    got = self.all_presses_for_code('029A')
    assert want == got
    want = 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A'
    got = sorted(self.get_dir_presses_for('<A^A>^^AvvvA'))
    if want not in got:
      print("Expected", want, "in", got)
      sys.exit(1)

    total_complexity = 0
    for code in self.codes:
      all_presses = self.all_presses_for_code(code)
      print(code, all_presses)
      shortests = None
      len_shortest = -1
      for presses in all_presses:
        robot2 = list(self.get_dir_presses_for(presses))
        for r2 in robot2:
          dir_presses = list(self.get_dir_presses_for(r2))
          if len_shortest < 0:
            len_shortest = len(dir_presses[0])
            shortests = set([dir_presses[0]])
          for dp in dir_presses:
            if len(dp) < len_shortest:  
              len_shortest = len(dp)
              shortests = set([dp])
            if len(dp) == len_shortest:  
              shortests.add(dp)
      print(code, '=>', sorted(shortests)[0])
      complexity = len_shortest * int(code[0:3])
      total_complexity += complexity
      if code == '029A':
        assert len_shortest == 68
        assert complexity == len_shortest * 29

    if code == '029A':
      assert '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' in shortests

    return total_complexity

  def get_dir_presses_for(get, presses):
    pos = 'A'  # second keyboard at A
    all_presses = set([''])
    for next in presses:  # for next button you need to hit
      new_presses = set()
      more = dir_map[pos].get(next, [''])
      for first_part in all_presses:
        for next_part in more:
          new_presses.add(first_part + next_part + 'A')
      all_presses = new_presses
      pos = next
      # print('  ', pos, '=>', next, all_presses)
    return all_presses

  def all_presses_for_code(self, code):
    pos = 10
    all_presses = set([''])
    for digit in code:
      next = int(digit, 16)
      new_presses = set()
      for next_path in self.find_presses(pos, next):
        for first_part in all_presses:
          new_presses.add(first_part + next_path + 'A')
      all_presses = new_presses
      if self.doing_sample and VERBOSE > 1:
        print(code, '%2d' % pos, '=>', '%2d' % next, all_presses)
      pos = next
    return all_presses

# <A^A>^^AvvvA, <A^A^>^AvvvA,     <A^A^^>AvvvA'}


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day21.sample_test("""
029A
980A
179A
456A
379A
""", expect1=126384, expect2=None)


if __name__ == '__main__':
  day21.run_and_check('input.txt', expect1=278748, expect2=None)
