#!/bin/bash
pkgs=(
	htop
	tree
	kernel-devel-3.10.0-957.el7.x86_64
	aria2
	ntp
	nfs-utils
	yp-tools
	ypbind
	ypserv
	libc++-static
	libcurl-devel
	openssl-devel
	python-pip
	python-devel
	cmake3
	zsh
	perf
	autogen
	gettext-devel
	libtool
	tcl
	tcl-devel
	tk
	perl-XML-LibXML
	perl-Switch
	p7zip
	mpfr
	mpfr-devel
	gmp
	gmp-devel
	hwloc
	hwloc-devel
	libmpc-devel
	tkinter
	numactl
	numactl-devel
	git2u
	tmux2u
	python36u
	python36u-libs
	python36u-devel
	python36u-pip
)

yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum groupinstall development -y
yum groupinstall 'Server with GUI' -y --skip-broken
#rpm -e --nodeps git-1.8.3.1-20.el7.x86_64
yum remove git -y # use newer git in ius
yum install ${pkgs[@]} -y
