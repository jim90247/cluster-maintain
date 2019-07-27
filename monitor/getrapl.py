#!/usr/bin/env python3.6
import time
import sys

def collect_rapl(rapl_path):
    """collect cpu power (Watt) by socket"""
    for path in rapl_path:
        with open(path, 'r') as f:
            yield int(f.read()) / 10**6

rapl_path = [f'/sys/devices/virtual/powercap/intel-rapl/intel-rapl:{i}/energy_uj'
    for i in range(2)]

prev = power = [0] * 2
while True:
    prev, power = power, list(collect_rapl(rapl_path))
    p = [power[i] - prev[i] for i in range(2)]
    print('{:.2f} {:.2f}'.format(*p))
    sys.stdout.flush()
    time.sleep(1)
