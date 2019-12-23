#!/usr/bin/env python3

import sys
import textwrap

# from elf_image import ElfImage
import intcode

def asc_to_str(s):
  try:
    return ''.join(chr(c) for c in s)
  except ValueError as e:
    return s


class NIC(object):

  def __init__(self, id, mem, network):
    # The computers on the network are standard Intcode computers
    # that communicate by sending packets to each other. There are
    # 50 of them in total, each running a copy of the same Network
    # Interface Controller (NIC) software (your puzzle input). The
    # computers have network addresses 0 through 49; when each computer
    # boots up, it will request its network address via a single input
    # instruction. Be sure to give each computer a unique network
    # address.
    self.id = id
    self.computer = intcode.IntCode(list(mem),
        input=[self.id], get_input=lambda: self.idle())
    self.network = network
    self.packet = None
    self.idle_count = 0

  def send_to(self, word):
    self.computer.push_input(word)

  def idle(self):
    # print('idle func for nic', self.id)
    self.idle_count += 1
    return -1

  def step(self):
    self.computer.step(output=lambda word: self.proc_output(word))

  def proc_output(self, word):
    self.idle_count = 0
    # print('nic', self.id, 'output', word)
    if not self.packet:
      self.packet = [word]
    else:
      self.packet.append(word)
      if len(self.packet) == 3:
        snd = self.packet
        self.packet = None
        self.network.send(self.id, snd)
    

class Network(object):

  def __init__(self, mem):
    self.nics = []
    for i in range(50):
      self.nics.append(NIC(mem=mem, id=i, network=self))
    self.start_idle_check = False
    self.nat_last_y = -1
    self.shutdown = False

  def run(self):
    while not self.shutdown:
      for nic in self.nics:
        nic.step()
      self.nat_check()

  def send(self, from_nic, packet):
    nic_id = packet[0]
    if nic_id == 255:
      print('nic', from_nic, 'send to NAT', packet)
      self.nat(packet)
    if nic_id >= 50:
      print('nic', from_nic, 'send packet out of range', packet)
      return
    print('nic', from_nic, 'send', packet)
    self.nics[nic_id].send_to(packet[1])
    self.nics[nic_id].send_to(packet[2])


  def nat(self, packet):
    self.nat_x = packet[1]
    self.nat_y = packet[2]
    self.start_idle_check = True

  def nat_check(self):
    if not self.start_idle_check:
      return
    is_idle = True
    for nic in self.nics:
      if nic.idle_count == 0:
        is_idle = False
        break
    if is_idle:
      self.start_idle_check = False
      print('network seems idle')
      packet = [0, self.nat_x, self.nat_y]
      if self.nat_y == self.nat_last_y:
        print('NAT send Y twice', self.nat_y)
        assert 11319 == self.nat_y
        self.shutdown = True
      self.nat_last_y = self.nat_y
      self.send(255, packet)


def part1():
  mem = intcode.load_intcode('input_23.txt')
  network = Network(mem)
  network.run()


if __name__ == '__main__':
  part1()
  # part2()
