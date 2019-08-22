#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

args = sys.argv
if len(args) < 2:
  print("missing argument - format should be: python ls8.py <path to program file>")
  exit()
else:
  file = sys.argv[1]

cpu = CPU()

cpu.load(file)
cpu.run()