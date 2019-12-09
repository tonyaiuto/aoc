#!/usr/bin/env python3


class ElfImage(object):

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.layer_span = w * h
    self.do_histograms = True
    self.histos = None

  @property
  def histograms(self):
    return self.histos

  @property
  def image(self):
    return self.final

  def parse(self, image):
    self.n_layers = len(image) // (self.layer_span)
    if len(image) != self.layer_span * self.n_layers:
      raise Exception('Length of image (%d) != %d x %d x %d' % (
                      len(image), self.w, self.h, self.n_layers))
    self.final = [2] * self.layer_span
    if self.do_histograms:
      self.histos = []

    for layer in range(self.n_layers):
      start = self.layer_span * layer
      end = start + self.layer_span
      digit_hist = {}
      for pi in range(self.layer_span):
        pixel = int(image[start+pi])
        if self.final[pi] == 2:
          self.final[pi] = pixel
        digit_hist[pixel] = digit_hist.get(pixel, 0) + 1
      if self.do_histograms:
        self.histos.append(digit_hist)
    return self.final


def self_check():
  i = ElfImage(3, 2)
  i.parse('123456789012')


self_check()
