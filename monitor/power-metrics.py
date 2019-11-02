#!/usr/bin/env python3.6
import argparse
import sys
import re
import time
import subprocess
import shlex
import threading

# some constants
update_interval = 1 # second
cpu_freq_re = re.compile(r'cpu MHz\s+:\s+(\d+\.\d+)')
cpu_temp_re = re.compile(r'\s+temp1_input:\s+(\d+\.\d+)')
ipmi_power_re = re.compile(r'(\d+)\s+watts')
n_sockets = 2

metrics = {
    'cpu': {},
    'fan': {},
    'gpu': {},
    'ipmi_power': 0
}

def cpu_power():
    last = None
    cur = None
    while True:
        last = cur
        cur = []
        for socket in range(n_sockets):
            with open(f'/sys/devices/virtual/powercap/intel-rapl/intel-rapl:{socket}/energy_uj', 'r') as f:
                cur.append(int(f.read()) / 10**6)
        
        if last:
            metrics['cpu']['power'] = [cur[socket] - last[socket] for socket in range(n_sockets)]

        time.sleep(update_interval)

def cpu_freq():
    while True:
        freq = []
        with open('/proc/cpuinfo', 'r') as f:
            lines = f.read().splitlines()
            for l in lines:
                x = cpu_freq_re.match(l)
                if x:
                    freq.append(float(x.group(1)))

        metrics['cpu']['freq'] = freq
        time.sleep(update_interval)

def cpu_temp():
    while True:
        temp = []
        lines = subprocess.check_output(['sensors', '-u']).decode('utf-8').splitlines()
        for l in lines:
            x = cpu_temp_re.match(l)
            if x:
                temp.append(float(x.group(1)))

        metrics['cpu']['temp'] = temp
        time.sleep(update_interval)


def fan_rpm():
    fan_rpm_cmd = 'sudo ipmitool sensor reading'
    for fan in range(1, 10):
        fan_rpm_cmd += f' FAN{fan}'
    fan_rpm_cmd += ' -c'

    while True:
        rpm = []
        lines = subprocess.check_output(shlex.split(fan_rpm_cmd)).decode('utf-8').splitlines()
        for l in lines:
            [fan_id, fan_rpm] = l.split(',')
            rpm.append(int(fan_rpm))

        metrics['fan']['rpm'] = rpm
        time.sleep(update_interval)

def ipmi_power():
    ipmi_power_cmd = 'sudo /usr/local/bin/ipmicfg/ipmicfg -nm oemgetpower'
    while True:
        reading = subprocess.check_output(shlex.split(ipmi_power_cmd)).decode('utf-8')
        metrics['ipmi_power'] = int(ipmi_power_re.match(reading).group(1))
        time.sleep(update_interval)

def main():
    threads = []
    threads.append(threading.Thread(target=cpu_power))
    threads.append(threading.Thread(target=cpu_freq))
    threads.append(threading.Thread(target=cpu_temp))
    threads.append(threading.Thread(target=fan_rpm))
    threads.append(threading.Thread(target=ipmi_power))

    for t in threads:
        t.start()

    while True:
        time.sleep(update_interval)
        print("[{:16.5f}] {}".format(time.time(), metrics))
        sys.stdout.flush()

if __name__ == '__main__':
    main()