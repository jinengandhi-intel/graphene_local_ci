#!/bin/bash

if [ $# != 1 ] ; then
        echo "Please provide CONFIG"
        exit 1
fi

config=$1

for ((i=1;i<=2;i++));
do
        sleep 5
        ./instance_benchmark.sh 48 1:9 $config $i 180
done

sleep 5

cd /home/intel/redis-6.0.6/log/set
rename 's/:/0/' *

# Zipping the data collected
cd /home/intel/redis-6.0.6/log
zip -r  $config.zip set

# Removing the old data and copying the new data
mv $config.zip $WORKSPACE/CI-Examples/redis/
rm set/config*

# Here 
# Main script "instance_benchmark.sh"
# Before starting the runs please modify REDIS_PATH, MEMTIER_PATH, and HOST variable values in instance_benchmark.sh
# Number of runs = 2
# Output directory: Please check REDIS_PATH/log in instance_benchmark.sh 
# Data size = 48B
# Set:Get ratio = 1:9
# Duration for the test = 180 sec
# config variable can have these values {native,graphene,graphene_sgx_same_core,graphene_sgx_diff_core,graphene_sgx_single_thread,graphene_sgx_single_thread_exitless and few more}

# Userful Link for memtier: https://redis.com/blog/memtier_benchmark-a-high-throughput-benchmarking-tool-for-redis-memcached/ 
