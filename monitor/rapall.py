#!/usr/bin/env python3.6

import os
import argparse
import threading
import subprocess


P0 = '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:0/constraint_0_power_limit_uw'
P1 = '/sys/devices/virtual/powercap/intel-rapl/intel-rapl:1/constraint_0_power_limit_uw'


def make_command(watts):
    wattss = f'{watts:d}000000'
    return ['echo', wattss, '>', P0, ';', 'echo', wattss, '>', P1]


def rapl(node, watts):
    r = subprocess.run(
        ['ssh', f'root@10.18.0.10{node}', '--'] + make_command(watts)
    )
    print(f'isc{node} exited with status {r.returncode}')


def rapall(watts):
    threads = [
        threading.Thread(target=rapl, args=(node, watts))
        for node
        in [1, 2, 3, 4, 5, 6]
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('power', help='max power in watts', type=int)
    args = parser.parse_args()
    rapall(args.power)


if __name__ == '__main__':
    main()
