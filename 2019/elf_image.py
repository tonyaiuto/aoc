#!/usr/bin/env python3

import io
import sys
import textwrap

from PIL import Image
from PIL import ImageDraw

class ElfImage(object):

  def __init__(self, width, height, min_x=0, min_y=0):
    self.width = width
    self.height = height
    self.min_x = min_x
    self.min_y = min_y
    self.layer_span = width * height
    self.do_histograms = True
    self.histos = None
    self.image = None
    self.text_font = None

  @property
  def histograms(self):
    return self.histos

  def parse(self, image):
    self.n_layers = len(image) // (self.layer_span)
    if len(image) != self.layer_span * self.n_layers:
      raise Exception('Length of image (%d) != %d x %d x %d' % (
                      len(image), self.width, self.height, self.n_layers))
    self.image = [2] * self.layer_span
    if self.do_histograms:
      self.histos = []

    for layer in range(self.n_layers):
      start = self.layer_span * layer
      end = start + self.layer_span
      digit_hist = {}
      for pi in range(self.layer_span):
        pixel = int(image[start+pi])
        if self.image[pi] == 2:
          self.image[pi] = pixel
        digit_hist[pixel] = digit_hist.get(pixel, 0) + 1
      if self.do_histograms:
        self.histos.append(digit_hist)
    return self.image

  @staticmethod
  def fromPoints(points, to_color=lambda x: x):
    min_x = min([pos[0] for pos in points.keys()])
    max_x = max([pos[0] for pos in points.keys()])
    min_y = min([pos[1] for pos in points.keys()])
    max_y = max([pos[1] for pos in points.keys()])
    # print(min_x, max_x, min_y, max_y)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    ret = ElfImage(width=width, height=height, min_x=min_x, min_y=min_y)
    ret.image = [0] * (width * height)
    ret.update(points, to_color)
    return ret

  def update(self, points, to_color=lambda x: x):
    for pos, color in points.items():
      x = pos[0] - self.min_x
      y = pos[1] - self.min_y
      self.image[y * self.width + x] = to_color(color)

  def print(self, color_map=None, out=sys.stdout):
    if not color_map:
      color_map = (lambda pix:
          ' 'if pix == 0
          else '#' if pix == 1
          else pix if (isinstance(pix, str) and 1 == len(pix))
          else '?')
    start = 0
    for row in range(self.height):
      print(''.join(
          [color_map(pix) for pix in self.image[start:start+self.width]]),
          file=out)
      start += self.width

  def toPng(self, out_file, scale=10, legend=None):
    image_height = self.height*scale
    if legend:
      image_height += 20
    im = Image.new('L', (self.width*scale, image_height), 255)
    draw = ImageDraw.Draw(im)
    start = 0
    for row in range(self.height):
      for col in range(self.width):
        bounds = [(col*scale, row*scale), ((col+1)*scale, (row+1)*scale)]
        pix = self.image[start+col]
        if pix == ' ' or pix == 0:
          fill = 255
        elif pix == 'b':
          fill = 128
        elif pix == '-':
          bounds = [(col*scale, row*scale+scale/3),
                    ((col+1)*scale, (row+1)*scale-scale/3)]
          draw.rectangle(bounds, fill=42)
          continue
        elif pix == 'o':
          bounds = [(col*scale+1, row*scale+1),
                    ((col+1)*scale-1, (row+1)*scale-1)]
          draw.arc(bounds, start=0, end=360, fill=0, width=5)
          continue
        else:
          fill = 0
        draw.rectangle(bounds, fill=fill)
      start += self.width
    if legend:
      xy = (0, self.height*scale)
      draw.text(xy, text=legend, fill=0)
    im.save(out_file)


def self_check():
  i = ElfImage(3, 2)
  i.parse('123456789012')
  # print(i.image)
  assert i.image == [1, 8, 3, 4, 5, 6]

  points = {(0,0): 'C'}
  points.update({(1,1): 1})
  points.update({(-1,1): '-'})
  points.update({pos: 1 for pos in [(-5, i) for i in range(-4, 4)]})
  points.update({pos: 1 for pos in [(i, 2) for i in range(-6, 4)]})
  i = ElfImage.fromPoints(points)
  expected = [
      0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 1, 0, 0, 0, 0, 'C', 0, 0, 0,
      0, 1, 0, 0, 0, '-', 0, 1, 0, 0,
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
      0, 1, 0, 0, 0, 0, 0, 0, 0, 0
  ]
  assert expected == i.image
  expected = textwrap.dedent("""\
       #        
       #        
       #        
       #        
       #    C   
       #   - #  
      ##########
       #        
      """)
  got = io.StringIO()
  i.print(out=got)
  assert expected == got.getvalue()

self_check()
