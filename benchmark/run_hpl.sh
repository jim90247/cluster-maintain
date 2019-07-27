#!/bin/bash
set -xe
HPL_DIR=`pwd`

# configurations
n_core=4
n_gpu=4 # 1 process per GPU
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

# export KMP_AFFINITY="verbose,granularity=fine,proclist=[$(($lrank*4)),$(($lrank*4+1))],explicit"
# export KMP_AFFINITY="granularity=fine,proclist=[$(($lrank*4)),$(($lrank*4+1)),$(($lrank*4+2)),$(($lrank*4+3))],explicit"
export KMP_AFFINITY=scatter
export CUDA_VISIBLE_DEVICES=$GPUID
numactl --cpunodebind=$CPUID $APP
