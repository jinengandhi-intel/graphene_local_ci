#!/usr/bin/bash

rm corpus/*
rm cipher_corpus/*

echo "Apple" > corpus/Apple.txt
echo "aPple" > corpus/aPple.txt
echo "apPle" > corpus/apPle.txt

#gramine-sgx-pf-crypt encrypt -w files/wrap_key -i corpus -o cipher_corpus

clang -g -fsanitize=fuzzer example.c -o example_fuzzer

#./example_fuzzer -max_total_time=180s corpus

#kill -INT 888

#rm corpus/Apple.txt corpus/aPple.txt corpus/apPle.txt

cp corpus/* cipher_corpus/

gramine-sgx-pf-crypt encrypt -w files/wrap_key -i corpus -o cipher_corpus

make clean

make SGX=1

#gramine-sgx ./libfuzz -seed=1 cipher_corpus/aPple.txt
gramine-sgx ./libfuzz cipher_corpus 2>&1|tee libfuzz_gramine-sgx.log

