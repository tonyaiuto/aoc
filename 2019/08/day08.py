#!/usr/bin/env python3


def parse_image(image, w, h):
  n_layers = len(image) // (w * h)
  if len(image) != w * h * n_layers:
    raise Exception('Length of image (%d) != %d x %d x %d' % (
                    len(image), w, h, n_layers))
  min_0 = w * h + 1
  min_0_layer = None
  final = [2] * w * h
  for layer in range(n_layers):
    start = w * h * layer
    end = w * h * (layer + 1)
    digit_hist = {}

    for pi in range(w * h):
      pixel = int(image[start+pi])
      if final[pi] == 2:
        final[pi] = pixel
      digit_hist[pixel] = digit_hist.get(pixel, 0) + 1
    # print('layer', layer, 'count 0=', digit_hist[0])
    if min_0 > digit_hist.get(0, 0):
      min_0 = digit_hist.get(0, 0)
      min_0_layer = layer
      min_0_check = digit_hist[1] * digit_hist[2]
      print('NEW MIN layer', layer, 'count 0=', min_0)
      print('#1', digit_hist[1], 'x #2', digit_hist[2],
            ' =', min_0_check)
  if n_layers > 5:
    assert min_0 == 6
    assert min_0_layer == 8
    assert min_0_check == 1703
  return final

parse_image('123456789012', 3, 2)


def part1():
  with open('input_08.txt', 'r') as inp:
    image = parse_image(inp.read().strip(), 25, 6)
    for h in range(6):
      row = ['*' if pix == 1 else ' ' for pix in image[h*25:(h+1)*25]]
      print(''.join(row))


if __name__ == '__main__':
  part1()
