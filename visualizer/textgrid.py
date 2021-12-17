#!/usr/bin/env python3
"""Receive state of a grid and chart it.

"""
import socket
import sys
from typing import List

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


def main(args: List[str]):
  server = SimpleJSONRPCServer(('localhost', 8888))
  server.register_function(lambda x: x, 'ping')
  server.register_function(dims)
  server.serve_forever()


def dims(**kwargs):
  print('DIMS', kwargs)
  return 'bar'


if __name__ == '__main__':
  main(sys.argv)
