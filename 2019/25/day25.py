#!/usr/bin/env python3

import sys
import textwrap

from elf_image import ElfImage
import intcode


class Room(object):

  def __init__(self, name):
    self.name = name
    # map of direction to room
    self.doors = {}
    self.contains = set()


class Droid(object):

  def __init__(self, mem):
    self.computer = intcode.IntCode(list(mem))
    self.quit = False
    self.visited = {}
    self.x = 0
    self.y = 0
    self.items = {}
    self.next_item = 'A'
    self.visited[(0,0)] = '@'
    self.rooms = {}
    self.cur_room = None
    self.shortcuts = {
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',
        'i': 'inv',
        'q': 'quit',
    }

  def send_program(self, prog):
    assert len(prog) <= 15
    for cmd in prog:
      print(cmd)
      ascii_code = intcode.code_to_ascii(cmd, sep=' ')
      self.computer.push_input(ascii_code)

  def loop(self):
    state = ''
    while True:
      state += self.computer.run_until_terminator(['\r', '?'])
      if state.endswith('Command?'):
        break
    print(state)
    self.analyze(state)

    while True:
      inp = input().strip()
      inp = self.shortcuts.get(inp) or inp
      if inp.startswith('qu'):
        self.quit = True
        return
      elif inp == 'map':
        self.printmap()
      else:
        command = inp.strip().split(' ')
        if command:
          self.do_command(command)
          return


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
      self.loop()

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
        pass  # we printed it

      elif line == 'Items here:':
        getting_items = True
      elif getting_items and line.startswith('-'):
        got_item = True
        item = line[2:]
        item_id = self.items.get(item)
        if not item_id:
          item_id = self.next_item
          self.items[item_id] = item
          print('== Added %s = %s' % (item_id, item))
          self.next_item = chr(ord(self.next_item) + 1)
        self.visited[(self.x, self.y)] = item_id
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
    print('lookup room', name)
    if name.startswith('== '):
      name = name[3:]
    if name.endswith(' =='):
      name = name[:-3]
    room = self.rooms.get(name)
    if not room:
      room = Room(name)
      self.rooms[name] = room
    return room

  def printmap(self):
    print('================')
    if False:
      for k in sorted(self.items):
        print(k, self.items[k])
      print(self.visited)
      img = ElfImage.fromPoints(self.visited)
      img.print()

    for name, room in sorted(self.rooms.items()):
      print('===', name)
      print(textwrap.indent(textwrap.fill(room.desc), prefix='    '))
      for door, to_room in sorted(room.doors.items()):
        print('    %s -> %s' % (door, to_room.name))


def part1():
  mem = intcode.load_intcode('input_25.txt')
  droid = Droid(list(mem))

  droid.play()


if __name__ == '__main__':
  part1()
