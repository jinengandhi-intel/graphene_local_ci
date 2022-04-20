#!/bin/bash

dir = $1
sed -i 's/sgx.preheat_enclave_size/#sgx.preheat_enclave_size/g' ./LibOS/shim/test/regression/openmp.manifest.template
edmm_update="sgx.edmm_enable_heap = true\nsgx.preheat_enclave_size = \"64M\"\nsgx.edmm_lazyfree_th = 15\n"

if [[ "$optimization" == "naive" ]];
then
    edmm_update="sgx.edmm_enable_heap = true\n"
elif [[ "$optimization" == "hybrid" ]];
then
    edmm_update="sgx.edmm_enable_heap = true\nsgx.preheat_enclave_size = \"64M\"\n"
elif [[ "$optimization" == "lazy" ]];
then
    edmm_update="sgx.edmm_enable_heap = true\nsgx.edmm_lazyfree_th = 15\n"
fi

for i in $(find $dir -name '*.manifest.template');
do
    echo $i
    echo -e $edmm_update >> $i
done;
# Type the text that you want to append
#read -p 'sgx.edmm_enable_heap = true\nsgx.preheat_enclave_size = "128M"\nsgx.edmm_lazyfree_th=15\n' newtext

# Check the new text is empty or not
#if [ "$newtext" != "" ]; then
      # Append the text by using '>>' symbol
#echo -e "sgx.edmm_enable_heap = true\nsgx.preheat_enclave_size = \"128M\"\nsgx.edmm_lazyfree_th = 15\n" >> $filename
#fi
