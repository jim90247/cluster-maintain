#!/usr/bin/env python3.6
import zmq
import threading
import time
import datetime

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:2321")

power = {}


def server_thread():
    while True:
        [host, contents] = socket.recv_multipart()
        data = contents.split()
        cpu0, cpu1 = float(data[0]), float(data[1])
        timestr = str(data[2], encoding='utf-8')
        ts = datetime.datetime.strptime(timestr, '%Y-%m-%d_%H:%M:%S')
        power[host] = (cpu0 + cpu1, ts)
        socket.send_multipart([host, b'ok'])

thread = threading.Thread(target=server_thread)
thread.start()

while True:
    now = datetime.datetime.now()
    msg = ''
    for k, v in sorted(power.items()):
        host = str(k, encoding='utf-8')
        if (now - v[1]).total_seconds() > 10:
            msg += '{}: n/a    '.format(host)
        else:
            msg += '{}: {:6.2f} '.format(host, v[0])
    
    if len(msg) > 0:
        print(msg)
    time.sleep(1)