#!/bin/bash
echo $PWD
echo $1

config=$1

if [ "${config}" = "native" ]
then
    cmd="python3"
    export LD_PRELOAD="/usr/local/lib/libmimalloc.so.1.7"
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
    models/models/language_modeling/tensorflow/bert_large/inference/run_squad.py \
    --init_checkpoint=data/bert_large_checkpoints/model.ckpt-3649 \
    --vocab_file=data/wwm_uncased_L-24_H-1024_A-16/vocab.txt \
    --bert_config_file=data/wwm_uncased_L-24_H-1024_A-16/bert_config.json \
    --predict_file=data/wwm_uncased_L-24_H-1024_A-16/dev-v1.1.json \
    --precision=int8 \
    --output_dir=output/bert-squad-output \
    --predict_batch_size=$predict_batch_size \
    --experimental_gelu=True \
    --optimized_softmax=True \
    --input_graph=data/fp32_bert_squad.pb \
    --do_predict=True --mode=benchmark \
    --inter_op_parallelism_threads=1 \
    --intra_op_parallelism_threads=$cores_per_socket > output_${config}_${i}.txt
done

sleep 5