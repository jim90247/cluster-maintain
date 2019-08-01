#!/usr/bin/env python

from __future__ import print_function
import argparse
import subprocess
import platform


p = argparse.ArgumentParser()
p.add_argument('percentage', type=int)
o = p.parse_args()
assert 16 <= o.percentage <= 100
px = hex(o.percentage)

# 4 set of fans
for i in range(4):
    output = subprocess.check_output(['sudo', 'ipmitool', 'raw', '0x30', '0x39', '0x00', '0x00', '0x0{}'.format(i), px])
    print(i, output.strip())
    #assert output.strip() == b'00'
print('set', platform.node(), 'fan to', o.percentage)
