#!/usr/bin/env python3.6
import time
import sys
import socket
import zmq
import datetime

def collect_rapl(rapl_path):
    """collect cpu power (Watt) by socket"""
    for path in rapl_path:
        with open(path, 'r') as f:
            yield int(f.read()) / 10**6

rapl_path = [f'/sys/devices/virtual/powercap/intel-rapl/intel-rapl:{i}/energy_uj'
    for i in range(2)]

hostname = socket.gethostname()

context = zmq.Context()
sock = context.socket(zmq.DEALER)
sock.setsockopt_string(zmq.IDENTITY, hostname)
sock.connect("tcp://10.19.0.1:2321")

prev = power = [0] * 2

while True:
    prev, power = power, list(collect_rapl(rapl_path))
    p = [power[i] - prev[i] for i in range(2)]
    # print('{:.2f} {:.2f}'.format(*p))
    # sys.stdout.flush()
    ts = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    sock.send_string('{:.2f} {:.2f} {}'.format(*p, ts))
    time.sleep(1)
    ack = sock.recv()
