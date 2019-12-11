#!/usr/bin/env python3

from elf_image import ElfImage
import intcode

class Robot(object):

  def __init__(self):
    self.x = 0
    self.y = 0
    self.dir = 0  # 0 up, 1 right, 2, down, 3 left
    self.painted = {}


  def turn(self, dir):
    if dir == 0:
      self.dir -= 1
      if self.dir < 0:
        self.dir += 4
    else:
      self.dir = (self.dir + 1) % 4


  def move(self):
    if self.dir == 0:
      self.y -= 1
    elif self.dir == 1:
      self.x += 1
    elif self.dir == 2:
      self.y += 1
    elif self.dir == 3:
      self.x -= 1
    else:
      raise Exception('bad dir: %d' % self.dir)


  def paint(self, computer):
    while True:
      computer.push_input(self.painted.get((self.x, self.y), 0))
      color = computer.run_until_output()
      dir = computer.run_until_output()
      # print('paint %d,%d %s' % (self.x, self.y, 'black' if color == 0 else 'white'))
      if computer.is_halted:
        break
      self.painted[(self.x, self.y)] = color
      self.turn(dir)
      self.move()


def part1():
  mem = intcode.load_intcode('input_11.txt')
  ic = intcode.IntCode(list(mem))
  robot = Robot()
  robot.paint(ic)
  print('part1:', len(robot.painted))

def part2():
  mem = intcode.load_intcode('input_11.txt')
  ic = intcode.IntCode(list(mem))
  robot = Robot()
  robot.painted[(0, 0)] = 1
  robot.paint(ic)

  image = ElfImage.fromPoints(robot.painted)
  image.print()
  """
   #  # ####  ##  #### #  # ###  #    ###    
   #  #    # #  # #    # #  #  # #    #  #   
   #  #   #  #  # ###  ##   ###  #    #  #   
   #  #  #   #### #    # #  #  # #    ###    
   #  # #    #  # #    # #  #  # #    #      
    ##  #### #  # #### #  # ###  #### #      
  """
  image.toPng('out_11.png')


if __name__ == '__main__':
  part1()
  part2()
