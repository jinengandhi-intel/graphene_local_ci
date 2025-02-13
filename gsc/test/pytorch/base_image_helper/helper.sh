# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2022 Intel Corporation

# exit when any command fails
set -e

CUR_DIR=$(pwd)
MY_PATH=$(dirname "$0")
cd $MY_PATH


if [ "$1"  = "debug" ]; then
     image_name='pytorch-encrypted-debug'
elif [ "$1" = "debugoptimized" ]; then
     image_name='pytorch-encrypted-debugoptimized'
else
     image_name='pytorch-encrypted'
fi

rm -rf examples
git clone https://github.com/gramineproject/examples.git
cd examples/pytorch
git checkout $(git tag --list 'v*.*' --sort=taggerdate | tail -1)

# Download and save the pre-trained model
python3 download-pretrained-model.py
cd ../../

# Commenting below statement of generation of encryption_key as 
# it is being checked-in the repo.
#dd if=/dev/urandom bs=16 count=1 > encryption_key

gramine-sgx-pf-crypt encrypt -w encryption_key -i examples/pytorch/input.jpg -o input.jpg
gramine-sgx-pf-crypt encrypt -w encryption_key -i examples/pytorch/classes.txt -o classes.txt
gramine-sgx-pf-crypt encrypt -w encryption_key -i examples/pytorch/alexnet-pretrained.pt -o \
alexnet-pretrained.pt

mv examples/pytorch/pytorchexample.py ./

# Build pytorch base image
docker rmi -f $image_name >/dev/null 2>&1
docker build -t $image_name .

rm -rf examples
rm pytorchexample.py input.jpg classes.txt alexnet-pretrained.pt
cd $CUR_DIR

echo -e '\n\nCreated base image `'$image_name'`.'
echo -e 'Please refer to `Intel-Confidential-Compute-for-X/workloads/pytorch/README.md` to ' \
'generate a Gramine-protected version of this Docker image.\n'
