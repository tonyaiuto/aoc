#!/usr/bin/env python3

import sys
import textwrap

from graphviz import Digraph

from elf_image import ElfImage
import intcode


class Room(object):

  all = []

  def __init__(self, name):
    self.name = name
    # map of direction to room
    self.doors = {}
    self.contains = set()
    Room.all.append(self)

  def __repr__(self):
    return '<%s>' % self.name

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

  def has_item(self, item):
    if item.in_room:
      item.in_room.contains.remove(item)
    self.contains.add(item)
    item.in_room = self

  def find_path_to(self, room):
    path, dirs = self._find_path_helper(room, '@', [], [])
    # print('path:', path)
    # print('dirs:', dirs)
    if not path:
      print('No path to', room.name)
    return dirs

  def _find_path_helper(self, to_room, via, path, dirs):
    print('try path from', self.name, 'to', to_room.name)
    path = path + [self]
    dirs = dirs + [via]
    if self == to_room:
      return path, dirs
    for dir, next_room in self.doors.items():
      if next_room and next_room not in path:
        n_path, n_dirs = next_room._find_path_helper(to_room, dir, path, dirs)
        if n_path:
          return n_path, n_dirs
    return None, []


class Item(object):

  next_id = 0
  all_items = {}

  def __init__(self, index, name):
    self.index = index
    self.id = Item._text_for(index)
    self.name = name
    self.in_room = None
    # Track them all
    Item.all_items[self.name] = self
    print('== Added %s = %s' % (self.id, self.name))


  @staticmethod
  def get_item(name):
    # Find or add item
    item = Item.all_items.get(name)
    if not item:
      item = Item(index=Item.next_id, name=name)
      Item.next_id = Item.next_id + 1
    return item

  @staticmethod
  def _text_for(id_index):
    prefix = ''
    while id_index >= 26:
      id_index -= 26
      prefix += 'A'
    return prefix + chr(ord('A') + id_index)

  @staticmethod
  def print_index():
    for _, item in sorted(Item.all_items.items()):
      print(item.id, item.name)

  @staticmethod
  def render_index(dot):
    if not Item.all_items:
      return
    holding = []
    all = ['<<table>']
    for i, (_, item) in enumerate(
        sorted(Item.all_items.items(), key=lambda kv: kv[1].index)):
      if item.in_room == None:
        holding.append(item.name)
      if i % 4 == 0:
        if i > 0:
          all.append('</tr>')
        all.append('<tr>')
      all.append('<td><b>%s</b></td><td>%s</td>' % (item.id, item.name))
      if i % 4 != 3:
        all.append('<td>&nbsp;</td>')
    all.append('</tr>')
    if holding:
      all.append('<tr><td> </td></tr>')
      all.append('<tr>')
      all.append('<td><b>Holding</b></td>')
      all.append('<td>' + ','.join(holding) + '</td>')
      all.append('</tr>')
    all.append('</table>>')
    dot.attr(label='\n'.join(all))

  def carry(self):
    if self.in_room:
      self.in_room.contains.remove(self)
    self.in_room = None


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
    self.pending_commands = []
    self.shortcuts = {
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',
        'i': 'inv',

        'm': 'map',
        'p': 'pick',
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
      if self.pending_commands:
        inp = self.pending_commands[0]
        self.pending_commands = self.pending_commands[1:]
      else:
        inp = input().strip()
      inp = self.shortcuts.get(inp) or inp
      if inp.startswith('qu'):
        self.quit = True
        return
      elif inp == 'map':
        self.print_map()
        continue

      if inp:
        if self.do_command(inp):
          return

  def queue_command(self, raw_command):
    self.pending_commands.append(raw_command)

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

  def do_command(self, raw_command):
    command = raw_command.split(' ')
    if command[0] == 'pick':
      if len(self.cur_room.contains) == 1:
        command = ['take'] + [
            item.name for item in self.cur_room.contains][0].split(' ')
      else:
        print('Can only take with exactly one item in the room')
        return False
    if command[0] == 'go':
      target_room = ' '.join(command[1:])
      route = self.find_path(self.cur_room, target_room)
      for door in route:
        self.queue_command(door)
      return False

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
    return True

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
        item = Item.get_item(line[2:])
        self.cur_room.has_item(item)
        self.visited[(self.x, self.y)] = item.id

      elif line.startswith("""You take the"""):
        # 'You take the foo.' => 'foo'
        item_name = line[13:][0:-1]
        # print('======== take:', item_name)
        Item.get_item(item_name).carry()

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

  def match_room(self, target_name):
    found = None
    target_name = target_name.lower()
    for name, room in self.rooms.items():
      if name.lower().startswith(target_name):
        if found:
          print('Not unique name', target_name, 'Matches', found.name, name)
          return None
        found = room
    return found

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

  def find_path(self, from_room, target_room):
    to_room = self.match_room(target_room)
    if not to_room:
      print('Unknown room:', target_room)
      return False
    return from_room.find_path_to(to_room)

  def render_map(self):
    # Render to graphviz
    dot = Digraph(comment='Star Ship')
    un_count = 0
    for _, room in self.rooms.items():
      label = room.name
      if len(room.contains) > 0:
        label += '[' + ' '.join(item.id for item in room.contains) + ']'
      attrs = {}
      if room == self.cur_room:
        attrs['font'] = 'bold'
        attrs['style'] = 'bold'
      dot.node(room.name, label=label, **attrs)

    for _, room in self.rooms.items():
      for door, to_room in room.doors.items():
        attrs = {}
        if not to_room:
          node_name = 'q%d' % un_count
          attrs['style'] = 'bold'
          attrs['font'] = 'bold'
          dot.node(node_name, label='?', **attrs)
          un_count += 1
        else:
          node_name = to_room.name
        dot.edge(room.name, node_name, label=door, **attrs)

    Item.render_index(dot)
    dot.render('ship.gv', format='png', view=True)


def part1(args):
  mem = intcode.load_intcode('input_25.txt')
  droid = Droid(list(mem))
  if args:
    with open(args[0], 'r') as pre_cmd:
      for line in pre_cmd:
        if line.startswith('#'):
          continue
        droid.queue_command(line.strip())
  droid.play()


if __name__ == '__main__':
  part1(sys.argv[1:])
