#!/bin/bash

# export REDIS_PATH=/home/sdp/redis-5.0.8
export REDIS_PATH=/home/intel/redis-6.0.6

# export MEMTIER_PATH=/home/sdp
export MEMTIER_PATH=/home/intel/memtier_benchmark
export REDIS_NUM=1
export BIND_SOCKET=0
export NUM_FILL_REQ=100000
export DATA_SIZE=128     # default value

export HOST="10.219.139.69"  # server's P2P ip address
export MASTER_START_PORT=9001  # Port number where redis server is running in server machine
#export MASTER_START_PORT=6378
if [ $# != 5 ] ; then
	echo "Please provide DATA_SIZE RATIO CONFIG RUN DURATION"
	exit 1
fi

DATA_SIZE=$1
RATIO=$2
CONFIG=$3
RUN=$4
DURATION=$5
PIPELINE=6

echo "Data size="$DATA_SIZE" Num fill req="$NUM_FILL_REQ

##export Workloads=(set get lpush lpop hset hrem sadd spop zadd zrem) #remove lpush for ddr
export Workloads=(set)
declare -A Empty_Workloads
Empty_Workloads=([get]="set" [lpop]="lpush" [hdel]="hset" [spop]="sadd" [zrem]="zadd")

#---------------------------check cpu configuration------------------------------------------
THREADS=`lscpu |grep "Thread(s) per core:"|awk -F ":" '{print $2'}|tr -d '[:space:]'`
CORES=`lscpu |grep "Core(s) per socket:"|awk -F ":" '{print $2'}|tr -d '[:space:]'`
LOCAL_THREAD=`lscpu |grep "NUMA node${BIND_SOCKET} CPU(s):"| awk '{print $(NF)}'|awk -F ',' '{print $1}'|awk -F '-' '{print $1}'`
REMOTE_THREAD=$(($LOCAL_THREAD + $CORES*2))

for workload in `echo ${Workloads[*]}`
do
    [ ! -d ${REDIS_PATH}/log/${workload} ] && mkdir -p ${REDIS_PATH}/log/${workload}

    echo -e "Start benchmark"
    for (( instances=1; instances <= $REDIS_NUM; instances++ ))
    do
        port=$(($MASTER_START_PORT + ${instances}))
        core_config=$((${LOCAL_THREAD}+${instances}-1))
        log_file="${REDIS_PATH}/log/${workload}/config-${CONFIG}_data-size-${DATA_SIZE}_ratio-${RATIO}_run-${RUN}_benchmark.csv"
        cmd="numactl -m ${BIND_SOCKET} taskset -c $core_config ${MEMTIER_PATH}/memtier_benchmark -s $HOST -p ${port} --key-maximum=${NUM_FILL_REQ} -d ${DATA_SIZE} --randomize --test-time=${DURATION} --ratio=${RATIO} --pipeline=${PIPELINE} -c 6 -t 7 --distinct-client-seed --out-file=${log_file}"
        echo -e $cmd
        $cmd &
    done
    while [ $(ps -ef | grep -c memtier_benchmark) -gt 1 ];do
        echo -e "Waiting for $(($(ps -ef | grep -c memtier_benchmark)-1)) memtier_benchmark to finish"
        sleep 5
    done

done

