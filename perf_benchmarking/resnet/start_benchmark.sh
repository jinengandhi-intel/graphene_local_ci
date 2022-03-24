#!/bin/bash
echo $PWD
echo $1

config=$1

if [ "${config}" = "native" ]
then
    cmd="python3"
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
fi
if [ "${config}" = "gramine-direct" ]
then
    cmd="gramine-direct ./python"
fi            
if [ "${config}" = "gramine-sgx" ]
then
    cmd="gramine-sgx ./python"
fi
export PATH=$PREFIX:$PATH
which gramine-sgx
echo "LD_PRELOAD : "
echo $LD_PRELOAD
for ((i=1;i<=3;i++));
do
    sleep 5

    OMP_NUM_THREADS=$cores_per_socket KMP_AFFINITY=granularity=fine,verbose,compact,1,0 taskset -c ${numa_nodes} ${cmd} \
    models/models/image_recognition/tensorflow/resnet50v1_5/inference/eval_image_classifier_inference.py \
    --input-graph=resnet50v1_5_int8_pretrained_model.pb \
    --num-inter-threads=1 \
    --num-intra-threads=$cores_per_socket \
    --batch-size=$predict_batch_size \
    --warmup-steps=50 \
    --steps=500 > output_${config}_${i}.txt
done

sleep 5