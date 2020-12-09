#!/usr/bin/env python3

from tools import elf_image


def part1():
  with open('input_08.txt', 'r') as inp:
    image = elf_image.ElfImage(25, 6)
    image.parse(inp.read().strip())
    min_0 = 25 * 6
    min_0_layer = None
    histos = image.histograms
    for layer in range(len(histos)):
      # print('layer', layer, 'count 0=', histos[layer][0])
      if min_0 > histos[layer].get(0, 0):
        min_0 = histos[layer].get(0, 0)
        min_0_layer = layer
        min_0_check = histos[layer][1] * histos[layer][2]
        print('NEW MIN layer', layer, 'count 0=', min_0)
        print('#1', histos[layer][1], 'x #2', histos[layer][2],
              ' =', min_0_check)
    # For my input
    assert min_0 == 6
    assert min_0_layer == 8
    assert min_0_check == 1703


def part2():
  with open('input_08.txt', 'r') as inp:
    image = elf_image.ElfImage(25, 6)
    image.parse(inp.read().strip())
    image.print()
    image.toPng('out_08.png')


if __name__ == '__main__':
  part1()
  part2()
