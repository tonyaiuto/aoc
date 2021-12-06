#!/usr/bin/env python3

import sys
import intcode

def dump():
  mem = intcode.load_intcode('input_25.txt')
  with open('input_25.bin', 'wb') as out:
    txt = ''
    for word in mem:
      if word > ord(' ') and word < 255:
        txt += chr(word)
    out.write(txt.encode('utf-8'))

if __name__ == '__main__':
  dump()
