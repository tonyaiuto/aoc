"AOC 2021: day 10"

from tools import aoc

OPENS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
} 
CLOSERS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
} 
POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
C_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


class day10(aoc.aoc):

  def __init__(self):
    super(day10, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })

  def part1(self):
    print('===== Start part 1')

    ret = 0
    for line in self.all_input:
      _, points = self.find_first_error(line)
      ret += points
    return ret

  @staticmethod
  def find_first_error(s):
    stack = []
    for pos,c in enumerate(s):
      # print(c, pos, stack)
      want = CLOSERS.get(c)
      if not want:
        stack.append(c)
      else:
        if len(stack) == 0:  #underflow
          print('underflow at ', pos)
          return pos, POINTS[c]
        if stack[-1] != want:
          # print('unmatch at ', pos, POINTS[c])
          return pos, POINTS[c]
        stack.pop()
    return -1,0

  def part2(self):
    print('===== Start part 2')

    scores = []
    for line in self.all_input:
      pos, _ = self.find_first_error(line)
      if pos < 0:
        scores.append(self.complete(line))

    scores = sorted(scores)
    mid = len(scores) // 2
    return scores[mid]

  @staticmethod
  def complete(s):
    stack = []
    for pos,c in enumerate(s):
      want = CLOSERS.get(c)
      if not want:
        stack.append(c)
      else:
        assert len(stack) != 0  #underflow
        assert stack[-1] == want
        stack.pop()

    score = 0
    while len(stack) > 0:
      c = stack.pop()
      score = score * 5 + C_POINTS[OPENS[c]]
    return score


day10.sample_test("""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""", expect1=26397, expect2=288957)


if __name__ == '__main__':
  day10.run_and_check('input.txt', expect1=392421, expect2=2769449099)

