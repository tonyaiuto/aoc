#!/usr/bin/env python3
"""Try to reach the server and make it squawk.

"""

import sys
import time
from typing import List

import jsonrpclib

def main(args: List[str]):
  server = jsonrpclib.Server('http://localhost:8888')

  if len(args) > 1 and args[1].startswith('q'):
    print('quit =>', server.quit())

  # sanity(server)
  grid_demo(server)

  # time.sleep(3)
  # print('quit =>', server.quit())


def grid_demo(server):
  res = server.grid(width=40, height=40, cell_width=10)
  print('grid =>', res)

  for y in range(0, 40, 2):
    for x in range(0, 40, 2):
      time.sleep(.01)
      res = server.draw_cell(x, y, 1)
      if y > 5:
        res = server.draw_cell(x, y-4, 0)



def sanity(server):
  res = server.ping('is this not echo?')
  print('ping =>', res)
  res = server.dims(x=100, y=42, y_min=-7)
  print('dims =>', res)


def arc_demo(server):
  time.sleep(1)
  res = server.demo_arc1()
  print('demo_arc1 =>', res)

  time.sleep(1)
  res = server.demo_arc2()
  print('demo_arc2 =>', res)

  time.sleep(1)
  res = server.demo_arc3()
  print('demo_arc3 =>', res)


if __name__ == '__main__':
  main(sys.argv)

"""
print jsonrpclib.history.request
{"jsonrpc": "2.0", "params": [5, 6], "id": "gb3c9g37", "method": "add"}
print jsonrpclib.history.response
{'jsonrpc': '2.0', 'result': 11, 'id': 'gb3c9g37'}

	batch = jsonrpclib.MultiCall(server)
	batch.add(5, 6)
	batch.ping({'key':'value'})
	batch._notify.add(4, 30)
	results = batch()
	for result in results:
	  print result
"""
