#!/bin/bash
set -e
HPCG_DIR=`pwd`

# configurations
n_core=5
n_gpu=8 # 1 process per GPU
n_socket=2

export OMP_NUM_THREADS=$n_core
export MKL_NUM_THREADS=$n_core
export LD_LIBRARY_PATH=$HPCG_DIR:$LD_LIBRARY_PATH

export MONITOR_GPU=0
export TRSM_CUTOFF=1000000

export GPU_DGEMM_SPLIT=1
export RANK_PERF=3500

APP=$HPCG_DIR/xhpcg-3.1

GPUID=$[${OMPI_COMM_WORLD_LOCAL_RANK} % ${n_gpu}]
CPUID=$[${GPUID} / (${n_gpu}/${n_socket})]

# export KMP_AFFINITY="verbose,granularity=fine,proclist=[$(($lrank*4)),$(($lrank*4+1)),$(($lrank*4+2)),$(($lrank*4+3))],explicit"
# export KMP_AFFINITY=scatter
export CUDA_VISIBLE_DEVICES=$GPUID
numactl --cpunodebind=$CPUID $APP
