#!/usr/bin/env python3
"""Try to reach the server and make it squawk.

"""

import sys
from typing import List

import jsonrpclib

def main(args: List[str]):
  server = jsonrpclib.Server('http://localhost:8888')

  res = server.ping('is this not echo?')
  print('ping =>', res)
  res = server.dims(x=100, y=42, y_min=-7)
  print('dims =>', res)

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
