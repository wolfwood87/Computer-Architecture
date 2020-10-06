#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

file_to_run = sys.argv[1]
cpu = CPU()

cpu.load(file_to_run)
cpu.run()