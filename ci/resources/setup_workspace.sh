#!/bin/bash
set -x

cd $WORKSPACE/gramine
cp -rf $WORKSPACE/ltp_src LibOS/test/ltp/
cp -rf $WORKSPACE/ltp_config/* LibOS/test/ltp/
cp -rf $WORKSPACE/ltp_scripts/* Scripts/
cp -rf $WORKSPACE/stress-ng CI-Examples/
cp -rf $WORKSPACE/go_helloworld CI-Examples/
cp -rf $WORKSPACE/examples/* CI-Examples/
cp -rf $WORKSPACE/test_workloads.py . 
cp -rf $WORKSPACE/utils/openvino_setup.sh CI-Examples/openvino/

if [[ "$SGX" == 1 ]]; then
  cp -rf ~/jenkins/sandstone-50-bin CI-Examples/
  cp -f $WORKSPACE/Patch/rename_protected_file.patch .

  if [[ "$base_os" == "ubuntu18.04" ]]; then
    cp -rf $WORKSPACE/Python/* CI-Examples/python/
  fi
fi

sed -i 's/.release  = "3.10.0"/.release  = "5.10.0"/' LibOS/src/sys/shim_uname.c

if [[ "$base_os" == *"centos"* ]]; then
  echo "setting up workspace for centos"
  cp -rf $WORKSPACE/utils/rust_centos_setup/* CI-Examples/rust/
  sed -i -e '/dist\|apport/c\' CI-Examples/python/python.manifest.template
fi