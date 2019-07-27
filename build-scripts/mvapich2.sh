#!/bin/bash
cc=gcc
cxx=g++
f=gfortran
opt_flag="-O3"
CONFIG=configure
PREFIX=/opt/pkg/bin/mvapich2-2.3.1/gcc-4.8.5

mkdir build
cd build
CC=${cc} CXX=${cxx} FC=${f} CFLAGS=${opt_flag} CXXFLAGS=${opt_flag} FCFLAGS=${opt_flag} FFLAGS=${opt_flag} ../${CONFIG} --prefix=${PREFIX}
make -j
make install
