#!/usr/bin/env python3.6

import os
import subprocess
from argparse import ArgumentParser
import ipaddress # for IP address testing

parser=ArgumentParser()
parser.add_argument('subnet', help='comma seperated list of subnets')
parser.add_argument('dir', help='comma seperated lists of directories to share on NFS')

args = parser.parse_args()

subnets = args.subnet.split(',')
dirs = args.dir.split(',')

# check if subnets are valid
for subnet in subnets:
    ipaddress.ip_network(subnet,strict=False)

# check if directories are valid
for d in dirs:
    if not os.path.exists(d):
        print(f"[ERROR] {d} does not exist!")
        exit(1)

subprocess.run(['yum', 'install', '-y', 'nfs-utils'])

f = open('/etc/exports', 'w')

for d in dirs:
    line = d
    for subnet in subnets:
        line += f" {subnet}(rw,async,no_root_squash)"
    line += "\n"
    f.write(line)

f.close()

subprocess.run(['systemctl', 'enable', 'nfs-server', '--now'])
subprocess.run(['exportfs', '-rv'])


