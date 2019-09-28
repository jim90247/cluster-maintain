#!/bin/bash

[ "x$1" == "x" ] || subnet=$1
[ "x$2" == "x" ] || pub_ip=$2
[ "x$3" == "x" ] || oif=$3

echo "subnet: $subnet, public ip: $pub_ip, outbound network interface: $oif"

set -xe

yum install -y nftables > /dev/null

nft flush ruleset
nft add table nat
nft add chain nat prerouting { type nat hook prerouting priority 0 \; }
nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
nft add rule nat postrouting ip saddr $subnet oif $oif snat $pub_ip

systemctl enable nftables --now
nft list ruleset >> /etc/sysconfig/nftables.conf

echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf
sysctl -p

