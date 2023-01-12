#!/bin/bash
set -x

chmod +x $WORKSPACE/ci/resources/setup_ltp.sh
bash $WORKSPACE/ci/resources/setup_ltp.sh

cd $WORKSPACE/examples
for i in $(find -name '*.manifest.template');
do
  sed -i '$ a sgx.debug = true' $i;
  if [[ "$EDMM" == 1 ]]; then
    sed -i '$ a sgx.edmm_enable = true' $i;
  fi
done;

cd $WORKSPACE/gramine
cp -rf $WORKSPACE/stress-ng CI-Examples/
cp -rf $WORKSPACE/go_helloworld CI-Examples/
cp -rf $WORKSPACE/examples/* CI-Examples/
cp -rf $WORKSPACE/test_workloads.py . 
cp -rf $WORKSPACE/utils/openvino_setup.sh CI-Examples/openvino/

if [[ "$SGX" == 1 ]]; then
  cp -rf ~/jenkins/sandstone-50-bin CI-Examples/
  if [[ "$EDMM" == 1 ]]; then
    sed -i '$ a sgx.edmm_enable = true' CI-Examples/sandstone-50-bin/sandstone.manifest.template;
  fi

  cp -f $WORKSPACE/Patch/rename_protected_file.patch .
fi

sed -i 's/.release  = "3.10.0"/.release  = "5.10.0"/' libos/src/sys/libos_uname.c

if [[ "$base_os" == *"centos"* ]]; then
  echo "setting up workspace for centos"
  cp -rf $WORKSPACE/utils/rust_centos_setup/* CI-Examples/rust/
fi

if [[ "$EDMM" == 1 ]]; then
  for i in $(find -name '*manifest.template');
  do
    sed -i 's/sgx.preheat_enclave = true//' $i;
  done;
fi