#!/usr/bin/env python3


W1_PATH='R997,D443,L406,D393,L66,D223,R135,U452,L918,U354,L985,D402,R257,U225,R298,U369,L762,D373,R781,D935,R363,U952,L174,D529,L127,D549,R874,D993,L890,U881,R549,U537,L174,U766,R244,U131,R861,D487,R849,U304,L653,D497,L711,D916,R12,D753,R19,D528,L944,D155,L507,U552,R844,D822,R341,U948,L922,U866,R387,U973,R534,U127,R48,U744,R950,U522,R930,U320,R254,D577,L142,D29,L24,D118,L583,D683,L643,U974,L683,U985,R692,D271,L279,U62,R157,D932,L556,U574,R615,D428,R296,U551,L452,U533,R475,D302,R39,U846,R527,D433,L453,D567,R614,U807,R463,U712,L247,D436,R141,U180,R783,D65,L379,D935,R989,U945,L901,D160,R356,D828,R45,D619,R655,U104,R37,U793,L360,D242,L137,D45,L671,D844,R112,U627,R976,U10,R942,U26,L470,D284,R832,D59,R97,D9,L320,D38,R326,U317,L752,U213,R840,U789,L152,D64,L628,U326,L640,D610,L769,U183,R844,U834,R342,U630,L945,D807,L270,D472,R369,D920,R283,U440,L597,U137,L133,U458,R266,U91,R137,U536,R861,D325,R902,D971,R891,U648,L573,U139,R951,D671,R996,U864,L749,D681,R255,U306,R154,U706,L817,D798,R109,D594,R496,D867,L217,D572,L166,U723,R66,D210,R732,D741,L21,D574,L523,D646,R313,D961,L474,U990,R125,U928,L58,U726,R200,D364,R244,U622,R823,U39,R918,U549,R667,U935,R372,U241,L56,D713,L735,U735,L812,U700,L408,U980,L242,D697,L580,D34,L266,U190,R876,U857,L967,U493,R871,U563,L241,D636,L467,D793,R304,U103,L950,D503,R487,D868,L358,D747,L338,D273,L485,D686,L974,D724,L534,U561,R729,D162,R731,D17,R305,U712,R472,D158,R921,U827,L944,D303,L526,D782,R575,U948,L401,D142,L48,U766,R799,D242,R821,U673,L120'
W2_PATH='L991,D492,L167,D678,L228,U504,R972,U506,R900,U349,R329,D802,R616,U321,R252,U615,R494,U577,R322,D593,R348,U140,L676,U908,L528,D247,L498,D79,L247,D432,L569,U206,L668,D269,L25,U180,R181,D268,R655,D346,R716,U240,L227,D239,L223,U760,L10,D92,L633,D425,R198,U222,L542,D790,L596,U667,L87,D324,R456,U366,R888,U319,R784,D948,R641,D433,L519,U950,L689,D601,L860,U233,R21,D214,L89,U756,L361,U258,L950,D483,R252,U206,L184,U574,L540,U926,R374,U315,R357,U512,R503,U917,R745,D809,L94,D209,R616,U47,R61,D993,L589,D1,R387,D731,R782,U771,L344,U21,L88,U614,R678,U259,L311,D503,L477,U829,R861,D46,R738,D138,L564,D279,L669,U328,L664,U720,L746,U638,R790,D242,R504,D404,R409,D753,L289,U128,L603,D696,L201,D638,L902,D279,L170,D336,L311,U683,L272,U396,R180,D8,R816,D904,L129,D809,R168,D655,L459,D545,L839,U910,L642,U704,R301,D235,R469,D556,L624,D669,L174,D272,R515,D60,L668,U550,L903,D881,L600,D734,R815,U585,R39,D87,R198,D418,L150,D964,L818,D250,L198,D127,R521,U478,L489,D676,L84,U973,R384,D167,R372,D981,L733,D682,R746,D803,L834,D421,R153,U752,L381,D990,R216,U469,L446,D763,R332,D813,L701,U872,L39,D524,L469,U508,L700,D382,L598,U563,R652,D901,R638,D358,L486,D735,L232,U345,R746,U818,L13,U618,R881,D647,R191,U652,R358,U423,L137,D224,R415,U82,R778,D403,R661,D157,R393,D954,L308,D986,L293,U870,R13,U666,L232,U144,R887,U364,L507,U520,R823,D11,L927,D904,R618,U875,R143,D457,R459,D755,R677,D561,L499,U267,L721,U274,L700,D870,L612,D673,L811,D695,R929,D84,L578,U201,L745,U963,L185,D687,L662,U313,L853,U314,R336'


class Path(object):

  def __init__(self, path_string):
    self.moves = []
    self.h_min = 0
    self.h_max = 0
    self.v_min = 0
    self.v_max = 0
    h = 0
    v = 0
    for move in path_string.split(','):
      dir = move[0].lower()
      dist = int(move[1:])
      self.moves.append((dir, dist))
      if dir == 'u':
        v += dist
        self.v_max = max(self.v_max, v)
      elif dir == 'd':
        v -= dist
        self.v_min = min(self.v_min, v)
      elif dir == 'r':
        h += dist
        self.h_max = max(self.h_max, h)
      elif dir == 'l':
        h -= dist
        self.h_min = min(self.h_min, h)
    print('[%d,%d] x [%d,%d]' % (self.h_min, self.h_max, self.v_min, self.v_max))

  def points(self):
    h = 0
    v = 0
    for move in self.moves:
      dir = move[0]
      dist = move[1]
      if dir == 'u':
        for d in range(dist):
          yield (h,v+1+d)
        v += dist
      elif dir == 'd':
        for d in range(dist):
          yield (h,v-1-d)
        v -= dist
      elif dir == 'r':
        for d in range(dist):
          yield (h+1+d,v)
        h += dist
      elif dir == 'l':
        for d in range(dist):
          yield (h-1-d,v)
        h -= dist


def min_dist(p1_str, p2_str):
  ret = 999999999999
  p1 = Path(p1_str)
  points1 = set()
  for p in p1.points():
    points1.add(p)
  p2 = Path(p2_str)
  for p in p2.points():
    if p in points1:
      dist = abs(p[0]) + abs(p[1])
      ret = min(ret, dist)
      print('Intersection at %s. Dist=%d' % (str(p), dist))
  return ret


def part1():
  assert min_dist('R75,D30,R83,U83,L12,D49,R71,U7,L72',
                  'U62,R66,U55,R34,D71,R55,D58,R83') == 159
  assert min_dist('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                  'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135
  dist = min_dist(W1_PATH, W2_PATH)
  print('part1:', dist)


def min_path(p1_str, p2_str):
  ret = 999999999999
  p1 = Path(p1_str)
  p2 = Path(p2_str)
  points1 = {}
  step = 0
  for p in p1.points():
    step += 1
    if p not in points1:
      points1[p] = step
  step = 0
  for p in p2.points():
    step += 1
    p1_steps = points1.get(p) or None
    if p1_steps is not None:
      dist = p1_steps + step
      ret = min(ret, dist)
      print('Intersection at %s. Dist=%d' % (str(p), dist))
  return ret

def part2():
  assert min_path('R75,D30,R83,U83,L12,D49,R71,U7,L72',
                  'U62,R66,U55,R34,D71,R55,D58,R83') == 610
  assert min_path('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                  'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410
  dist = min_path(W1_PATH, W2_PATH)
  print('part2:', dist)


if __name__ == '__main__':
  part1()
  part2()
