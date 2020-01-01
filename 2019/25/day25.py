#!/usr/bin/env python3

import sys
import textwrap

from graphviz import Digraph

from elf_image import ElfImage
import intcode


class Room(object):

  def __init__(self, name):
    self.name = name
    # map of direction to room
    self.doors = {}
    self.contains = set()

  def print(self):
    print('===', self.name)
    print(textwrap.indent(textwrap.fill(self.desc), prefix='    '))
    for door, to_room in sorted(self.doors.items()):
      if to_room:
        print('    %s -> %s' % (door, to_room.name))
      else:
        print('    %s -> <unknown>' % door)


  @property
  def dead_end(self):
    return len(self.doors) == 1

  def has_door(self, door):
    if door not in self.doors:
      self.doors[door] = None


class Item(object):

  next_id = 'A'
  all_items = {}

  def __init__(self, id, name):
    self.id = id
    self.name = name
    Item.all_items[id] = self
    print('== Added %s = %s' % (id, name))

  @staticmethod
  def getItem(name):
    # Find or add item
    item = Item.all_items.get(name)
    if not item:
      item_id = Item.next_id
      item = Item(name=name, id=item_id)
      Item.next_id = chr(ord(Item.next_id) + 1)
    return item

  @staticmethod
  def print_index():
    for _, item in sorted(Item.all_items.items()):
      print(item.id, item.name)

  @staticmethod
  def render_index(dot):
    all = ['<<table>']
    for i, (_, item) in enumerate(sorted(Item.all_items.items())):
      if i % 4 == 0:
        if i > 0:
          all.append('</tr>')
        all.append('<tr>')
      all.append('<td>%s</td><td>%s</td>' % (item.id, item.name))
      if i % 4 != 3:
        all.append('<td>&nbsp;</td>')
    all.append('</tr>')
    all.append('</table>>')
    dot.attr(label='\n'.join(all))

class Droid(object):

  def __init__(self, mem):
    self.computer = intcode.IntCode(list(mem))
    self.quit = False
    self.visited = {}
    self.x = 0
    self.y = 0
    self.visited[(0,0)] = '@'
    self.rooms = {}
    self.cur_room = None
    self.shortcuts = {
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',
        'i': 'inv',
        'm': 'map',
        'q': 'quit',
    }

  def send_program(self, prog):
    assert len(prog) <= 15
    for cmd in prog:
      print(cmd)
      ascii_code = intcode.code_to_ascii(cmd, sep=' ')
      self.computer.push_input(ascii_code)

  def do_turn(self):
    if not self.run_until_command():
      return
    while True:
      inp = input().strip()
      inp = self.shortcuts.get(inp) or inp
      if inp.startswith('qu'):
        self.quit = True
        return
      elif inp == 'map':
        self.print_map()
      else:
        command = inp.strip().split(' ')
        if command:
          self.do_command(command)
          return

  def run_until_command(self):
    state = ''
    while True:
      state += self.computer.run_until_terminator(['\r', '?'])
      if state.endswith('Command?'):
        break
      if self.computer.is_halted:
        print(state)
        print('Computer halted')
        self.quit = True
        return False
    print(state)
    self.analyze(state)
    return True


  def do_command(self, command):
    self.last_x = self.x
    self.last_y = self.y
    if command[0] == 'north':
      self.y -= 1
    elif command[0] == 'south':
      self.y += 1
    elif command[0] == 'east':
      self.x += 1
    elif command[0] == 'west':
      self.x -= 1
    if command[0] in ('north', 'south', 'east', 'west'):
      self.last_move = command[0]
    ascii_code = intcode.code_to_ascii(command, sep=' ')
    self.computer.push_input(ascii_code)

  def play(self):
    while not self.quit:
      self.do_turn()

  def analyze(self, state):
    getting_room = None
    desc = ''
    getting_doors = False
    getting_items = False
    got_item = False
    for line in state.split('\n'):
      if not line:
        if getting_room and desc:
          getting_room.desc = desc
        getting_room = None

      if not line or not line.startswith('- '):
        getting_doors = False
        getting_items = False

      if line.startswith('== '):
        getting_room = self.get_room(line)
        if self.cur_room and self.cur_room != getting_room:
          self.cur_room.doors[self.last_move] = getting_room
        self.cur_room = getting_room
        desc = ''

      elif getting_room:
        desc += line
        pass  # we printed it

      elif line == 'Doors here lead:':
        getting_doors = True
      elif getting_doors and line.startswith('-'):
        door = line[2:]
        self.cur_room.has_door(door)

      elif line == 'Items here:':
        getting_items = True
      elif getting_items and line.startswith('-'):
        got_item = True
        item = Item.getItem(line[2:])
        self.visited[(self.x, self.y)] = item.id
      elif line.startswith("""You can't go that way"""):
        self.visited[(self.x, self.y)] = '#'
        self.x = self.last_x
        self.y = self.last_y
      else:
        if line and not line.startswith('Command'):
          print('TODO: ', line)
    if not got_item:
      self.visited[(self.x, self.y)] = '.'

  def get_room(self, name):
    # print('lookup room', name)
    if name.startswith('== '):
      name = name[3:]
    if name.endswith(' =='):
      name = name[:-3]
    room = self.rooms.get(name)
    if not room:
      room = Room(name)
      self.rooms[name] = room
    return room

  def print_map(self):
    print('================')
    Item.print_index()
    if False:
      for k in sorted(self.items):
        print(k, self.items[k])
      print(self.visited)
      img = ElfImage.fromPoints(self.visited)
      img.print()

    for _, room in sorted(self.rooms.items()):
      room.print()

    self.render_map()


  def render_map(self):
    dot = Digraph(comment='Star Ship')
    un_count = 0
    for _, room in self.rooms.items():
      dot.node(room.name, label=room.name)

    for _, room in self.rooms.items():
      for door, to_room in room.doors.items():
        if not to_room:
          node_name = 'q%d' % un_count
          dot.node(node_name, label='?')
          un_count += 1
        else:
          node_name = to_room.name
        dot.edge(room.name, node_name, label=door)

    Item.render_index(dot)
    dot.render('ship.gv', format='png', view=True)


def part1(args):
  mem = intcode.load_intcode('input_25.txt')
  droid = Droid(list(mem))
  if args:
    with open(args[0], 'r') as pre_cmd:
      for line in pre_cmd:
        if line.startswith('#'):
          break
        droid.run_until_command()
        droid.do_command(line.strip().split(' '))
  droid.play()


if __name__ == '__main__':
  part1(sys.argv[1:])
