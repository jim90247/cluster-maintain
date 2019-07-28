import time
import subprocess
import threading

getrapl_script = '/home/jim90247/monitor/getrapl.py'

power = {}

def remote_getrapl(node):
    cmd = ['ssh', node, getrapl_script]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as p:
        for line in iter(p.stdout.readline, b''):
            power_socket = line.split()
            power[node] = float(power_socket[0]) + float(power_socket[1])


def main():
    threads = []
    for i in range(1, 7):
        threads.append(threading.Thread(target=remote_getrapl, args=('qct0{}'.format(i),)))

    for thread in threads:
        thread.start()
    
    while True:
        if len(power) == 6:
            log = ""
            for node, pw in sorted(power.items()):
                if pw >= 200:
                    color = '\033[91m'
                elif pw >= 120:
                    color = '\033[93m'
                else:
                    color = '\033[92m'

                log += "{}: {}{:6.2f}\033[0m ".format(node, color, pw)

            log += "total: {:7.2f}".format(sum(power.values()))
            print(log)
        # print(power)
        time.sleep(1)

if __name__ == '__main__':
    main()
