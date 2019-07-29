#!/bin/bash
set -xe
HPL_DIR=`pwd`

# MPI launch command:
# mpirun -H <host>:<process>[,<host>:<process>] --map-by slot:pe=5 --bind-to core ./run_hpl.sh

# configurations
n_core=5
n_gpu=8 # 1 process per GPU
n_socket=2


export OMP_NUM_THREADS=$n_core
export MKL_NUM_THREADS=$n_core
export LD_LIBRARY_PATH=$HPL_DIR:$LD_LIBRARY_PATH

export MONITOR_GPU=0
export TRSM_CUTOFF=1000000

export GPU_DGEMM_SPLIT='0.98'
export RANK_PERF=3500
APP=$HPL_DIR/xhpl_GPU_cuda90103_static_mkl_2016_static_ompi_1.10.2_sm35_sm60_sm70

GPUID=$[${OMPI_COMM_WORLD_LOCAL_RANK} % ${n_gpu}]
CPUID=$[${GPUID} / (${n_gpu}/${n_socket})]

export KMP_AFFINITY=scatter
export CUDA_VISIBLE_DEVICES=$GPUID
numactl --cpunodebind=$CPUID $APP
