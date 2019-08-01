#!/usr/bin/env python
from __future__ import print_function
import argparse
import subprocess
import platform
import shlex


parser = argparse.ArgumentParser()
parser.add_argument('percentage', type=int)
parser.add_argument('--zone', type=int, default=0, choices=[0, 1, 2])
args = parser.parse_args()
assert 20 <= args.percentage <= 100
px = hex(args.percentage)

cmd = 'sudo ipmitool -H 10.0.18.7 -U admin -P cmb9.admin -t 0x68 raw 0x36 0x08 {} 0x0{}'.format(px, args.zone)
output = subprocess.check_output(shlex.split(cmd))
print('set', platform.node(), 'fan to', args.percentage)
