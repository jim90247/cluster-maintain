#!/bin/bash
set -xe

# run this script on each nodes seperately,
# since some kernel modules will be built/insert during make

cuda_home=/usr/local/cuda-10.0
prefix=/opt/pkg/bin/gdrcopy
mkdir -p $prefix/lib64 $prefix/include

make PREFIX=$prefix CUDA=$cuda_home all install

# insert modules
./insmod.sh
