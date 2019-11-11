#!/bin/bash
set -e

function run_cmd {
	echo "[exec] $@"
	$@
}

run_cmd tar zxf MLNX_OFED_LINUX-4.6-1.0.1.1-rhel7.6-x86_64.tgz
run_cmd modprobe -rv ib_isert rpcrdma ib_srpt
run_cmd MLNX_OFED_LINUX-4.6-1.0.1.1-rhel7.6-x86_64/mlnxofedinstall --force
run_cmd /etc/init.d/openibd restart

echo "Wait a few seconds and check ibstat"
