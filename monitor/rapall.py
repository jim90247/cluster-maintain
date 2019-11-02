#!/usr/bin/env python3.6

import os
import argparse
import threading
import subprocess
import re

P0 = '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/constraint_0_power_limit_uw'
P1 = '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:1/constraint_0_power_limit_uw'


def make_command(watts):
    wattss = f'{watts:d}000000'
    return ['echo', wattss, '>', P0, ';', 'echo', wattss, '>', P1]


def rapl(node, watts):
    r = subprocess.run(
        ['ssh', f'root@10.19.0.{node}', '--'] + make_command(watts)
    )
    print(f'qct{node} exited with status {r.returncode}')


def rapall(watts, node_list):
    nodes = []
    segments = node_list.split(',')
    for seg in segments:
        l = seg.split('-')
        if len(l) == 1:
            nodes.append(int(seg))
        elif len(l) == 2:
            for i in range(int(l[0]), int(l[1])+1):
                nodes.append(i)

    threads = [
        threading.Thread(target=rapl, args=(node, watts))
        for node in nodes
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('power', help='max power in watts', type=int)
    parser.add_argument('nodes', help='nodes to adjust')
    args = parser.parse_args()
    rapall(args.power, args.nodes)


if __name__ == '__main__':
    main()
