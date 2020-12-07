"AOC 2020: day 7"

from collections import defaultdict

class Bag(object):

  bags = {}
  container = defaultdict(list)

  def __init__(self, key):
    # print('create bag', key)
    self.key = key
    self.holds = []
    self.inside = set()

  def __str__(self):
    return '%s' % (self.key)

  def dump(self):
    return '%s: %s' % (self.key, ','.join(['%d %s' % (x[0],x[1]) for x in self.holds]))

  def find_bag(desc):
    if desc[-1] in ('bag', 'bags'):
      desc = desc[0:-1]
    key = ','.join(desc)
    bag = Bag.bags.get(key)
    if bag:
      return bag
    b = Bag(key)
    Bag.bags[key] = b
    return b

  def add_contents(self, n, bag):
    self.holds.append((n, bag))
    Bag.container[bag].append(self)
    bag.inside.add(self)


class day7(object):

  def __init__(self):
    pass

  def load(self, file):
    n_rules = 0
    with open(file, 'r') as inp:
      for line in inp:
        l = line.strip()
        n_rules += 1
        self.parse(l)


  def parse(self, line):
    assert line.endswith('.')
    line = line[0:-1]
    assert line.find(' contains ') < 0

    i_contain = line.find(' contain ')
    assert  i_contain > 0
    bag = Bag.find_bag(line[0:i_contain].split(' '))
    rules = line[i_contain+9:].split(',')
    for r in rules:
      words = [w for w in r.split(' ') if w]
      if words[0] == 'no':
        # print('End bag', str(bag), words);
        return
      assert words[-1] in ('bag', 'bags')
      # print(words[0:-1])
      n = int(words[0])
      assert n > 0
      has_bag = Bag.find_bag(words[1:-1])
      bag.add_contents(n, has_bag)

  def part1(self):
    shiny_gold = Bag.find_bag(['shiny', 'gold'])
    # print(Bag.container[shiny_gold])
    visited = set()

    def walk_up(bag):
      if bag in visited:
        return
      visited.add(bag)
      for b in bag.inside:
        walk_up(b)

    walk_up(shiny_gold)
    part1 = len(visited)-1
    print('part1', part1)
    assert part1 == 226

  def part2(self):
    shiny_gold = Bag.find_bag(['shiny', 'gold'])

    def walk_down(bag):
      # print(bag.dump())
      if not bag.holds:
        return 1

      containted_bags = 0
      for h in bag.holds:
        n = h[0]
        other_bag = h[1]
        containted_bags += n * walk_down(other_bag)
      return 1 + containted_bags
 
    part2 = walk_down(shiny_gold) - 1
    print('part2', part2)
    assert part2 == 9569


def main(input):
  puzz = day7()
  puzz.load(input)
  puzz.part1()
  puzz.part2()



if __name__ == '__main__':
  main('input.txt')
