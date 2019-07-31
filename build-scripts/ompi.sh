#!/bin/bash
cc=gcc
cxx=g++
f=gfortran
opt_flag="-O3"
CONFIG=configure
PREFIX=/opt/pkg/bin/ompi-3.1.4/gcc-4.8.5

mkdir build
cd build
# for cuda support, add --with-cuda=<path_to_cuda> --with-ucx=<path_to_ucx_cuda>
CC=${cc} CXX=${cxx} FC=${f} \
  CFLAGS=${opt_flag} CXXFLAGS=${opt_flag} FCFLAGS=${opt_flag} \
  ../${CONFIG} --prefix=${PREFIX} --enable-orterun-prefix-by-default \
  --enable-mpi-cxx --with-platform=../contrib/platform/mellanox/optimized
make all -j
make install
