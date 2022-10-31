#!/usr/bin/env python3

"""
nop
jump start

0x90
0xEB
0xFD

reset vector
FFFF0
"""

buff = b"\x90\xEB\xFD"
open("out.bin", "wb").write(buff)

