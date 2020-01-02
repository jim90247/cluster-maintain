#!/bin/bash
set -e
script_dir=`pwd`
echo ">>> Install information <<<"
version=$1
prefix=$2
[ "x$version" == "x" ] && echo "No version specified!"
if [ "x$prefix" == "x" ]; then
	echo "No install prefix specified!"
else
	echo "Install prefix is $prefix"
fi
cd gcc-$version

echo ">>> Checking prerequisites <<<"
dep_missing=false
for pkg in gmp-devel mpfr-devel libmpc-devel; do
	[ "x$(rpm -qa $pkg)" == "x" ] && dep_missing=true
done
if $dep_missing; then
	echo "Missing prequisites, download them from internet."
	./contrib/download_prequisites
fi

mkdir build && cd build
echo ">>> Configure <<<"
../configure --prefix=$prefix --disable-multilib > $script_dir/config.log.$version 2>&1
echo ">>> Build <<<"
make -j > $script_dir/make.log.$version 2>&1
echo ">>> Install <<<"
make install > $script_dir/make-install.log.$version 2>&1

echo ">>> Installation to $prefix complete <<<"

