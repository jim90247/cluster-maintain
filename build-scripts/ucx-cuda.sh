#!/bin/bash
set -xe

# depencencies: cuda gdrcopy

prefix=/opt/pkg/bin/ucx-cuda
cuda_home=/usr/local/cuda-10.0
gdrcopy=/opt/pkg/bin/gdrcopy

../configure --prefix=$prefix --with-cuda=$cuda_home --with-gdrcopy=$gdrcopy
make -j install
