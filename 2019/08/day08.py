#!/usr/bin/env python3

from PIL import Image

import elf_image


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
    for h in range(6):
      row = ['#' if pix == 1 else ' ' for pix in image.image[h*25:(h+1)*25]]
      print(''.join(row))

  im = Image.frombytes('L', (25,6), bytes([255 if pix == 0 else 0 for pix in image.image]))
  im.save('aoc.png')


if __name__ == '__main__':
  part1()
  part2()
