#!/bin/bash
set -x

cd $WORKSPACE/examples
for i in $(find -name '*.manifest.template');
do
  sed -i '$ a sgx.debug = true' $i;
done;

cd $WORKSPACE/gramine
cp -rf $WORKSPACE/ltp_src libos/test/ltp/
cp -rf $WORKSPACE/ltp_config/* libos/test/ltp/
cp -rf $WORKSPACE/ltp_scripts/* scripts/
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

sed -i 's/.release  = "3.10.0"/.release  = "5.10.0"/' libos/src/sys/libos_uname.c

if [[ "$base_os" == *"centos"* ]]; then
  echo "setting up workspace for centos"
  cp -rf $WORKSPACE/utils/rust_centos_setup/* CI-Examples/rust/
fi

if [[ "$base_os" != *"ubuntu"* ]]; then
  echo "Updating Python manifest file for centos/rhel"
  sed -i -e '/dist\|apport/c\' CI-Examples/python/python.manifest.template
fi