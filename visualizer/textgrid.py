#!/usr/bin/env python3
"""Receive state of a grid and chart it.

"""

import socket
import sys
import threading
import time
import tkinter
from typing import List

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

class VisualizerCore(object):

  def __init__(self, host='localhost', port=8888):
    self.server = RPCServer(self, host, port)

    self.tk_root = tkinter.Tk()
    self.canvas = Canvas(self.tk_root)
    self.verbose = 0

  def register_functions(self, rpc_server):
    rpc_server.register_function(lambda x: x, 'ping')
    rpc_server.register_function(self.quit)
    rpc_server.register_function(self.dims)
    rpc_server.register_function(self.grid)
    rpc_server.register_function(self.draw_cell)
    # self.register_demo(rpc_server)

  def register_demo(self, rpc_server):
    rpc_server.register_function(self.demo_arc1)
    rpc_server.register_function(self.demo_arc2)
    rpc_server.register_function(self.demo_arc3)

  def serve(self):
    self.server.start()
    print('call canvas.start')
    self.canvas.start()
    print('call mainloop')
    self.tk_root.mainloop()
    print('backfrom mainloop')
    print('VisualizerCore.serve: done serving')

  def quit(self):
    print('exiting')
    self.server.quit()
    self.tk_root.quit()

  def dims(self, **kwargs):
    print('DIMS', kwargs)
    return 'bar'

  def grid(self, height, width, cell_width=7):
    # print('grid:', height, width, cell_width)
    if not cell_width:
      cell_width = 5
    self.canvas.make_grid(height=height, width=width, cell_width=cell_width)

  def draw_cell(self, x, y, v, **kwargs):
    if self.verbose > 0:
      print('draw_cell', x, y, v)
    self.canvas.draw_cell(x, y, v)

  def demo_arc1(self):
     coord = 10, 10, 300, 300
     _ = self.canvas.arc(coord, start=0, extent=120, fill="red")
     _ = self.canvas.arc(coord, start=120, extent=215, fill="yellow")

  def demo_arc2(self):
     coord = 10, 10, 300, 300
     _ = self.canvas.arc(coord, start=120, extent=150, fill="blue")

  def demo_arc3(self):
     coord = 10, 10, 300, 300
     _ = self.canvas.arc(coord, start=180, extent=200, fill="green")



class Canvas(threading.Thread):

  def __init__(self, root, width=400, height=400):
    super(Canvas, self).__init__()
    self.daemon = False  # cargocult
    self.root = root
    self._done = False
    self.background = 'white'
    self.foreground = 'black'
    self.canvas = None
    self.cells = {}
    self.padding = 5
    self.resize(width, height)

  def resize(self, width, height):
    self.width = width + 2 * self.padding
    self.height = height + 2 * self.padding
    print('resize canvas to %d x %d' % (self.width, self.height))
    if self.canvas:
      self.canvas.configure(
          bg=self.background, width=self.width, height=self.height)
    else:
      self.canvas = tkinter.Canvas(
          self.root, width=self.width, height=self.height,
          bg=self.background, borderwidth=0)
    self.canvas.pack()

  def run(self):
    self.canvas.pack()

  def pack(self):
    self.canvas.pack()

  def arc(self, coord, start, extent, fill):
    _ = self.canvas.create_arc(coord, start=start, extent=extent, fill=fill)
    self.canvas.pack()

  def make_grid(self, width, height, cell_width):
    print('canvas.make_grid', width, height)
    self.grid_height = height
    self.grid_width = width
    self.cell_width = cell_width
    print('call resize', height*cell_width, width*cell_width)
    self.resize(height=height*cell_width, width=width*cell_width)

  def draw_cell(self, x, y, v):
    fill = self.foreground if v == 1 else self.background
    x_pos = x * self.cell_width + self.padding + 1
    y_pos = y * self.cell_width + self.padding + 1
    cell = self.cells.get((x,y))
    if cell:
      self.canvas.delete(cell)
    if v <= ord(' '):
      self.cells[(x, y)] = self.canvas.create_rectangle(
          x_pos, y_pos, x_pos + self.cell_width, y_pos + self.cell_width,
          fill=fill, outline=fill)
    else:
      self.cells[(x, y)] = self.canvas.create_text(
          x_pos+5, y_pos+5, text=chr(v))
    # self.pack()


class RPCServer(threading.Thread):
  """RPCServer wraps a SimpleJSONRPCServer in a thread."""

  def __init__(self, visualizer, host='localhost', port=8888):
    super(RPCServer, self).__init__()
    self.visualizer = visualizer
    self.server = SimpleJSONRPCServer((host, port), logRequests=False)
    self.visualizer.register_functions(self.server)

  def run(self):
    print("Calling serve_forever")
    self.server.serve_forever()
    print("Returned from serve_forever")

  def quit(self):
    print('RPCServer.quit')
    # kill myself in another thread so that the current RPC can return.
    threading.Timer(.5, self.server.shutdown).start()


def main(args: List[str]):
  visualizer = VisualizerCore('localhost', 8888)
  visualizer.serve()


if __name__ == '__main__':
  main(sys.argv)
