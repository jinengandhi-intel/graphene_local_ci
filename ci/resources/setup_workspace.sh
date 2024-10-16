#!/bin/bash
set -x

python3 $WORKSPACE/utils/env_setup.py

cd $WORKSPACE/examples
for i in $(find -name '*manifest.template');
do
  sed -i '$ a sgx.debug = true' $i;
done;

cd $WORKSPACE/gramine
cp -rf $WORKSPACE/stress-ng CI-Examples/
cp -rf $WORKSPACE/sd-test CI-Examples/
cp -rf $WORKSPACE/go-helloworld CI-Examples/
cp -rf $WORKSPACE/examples/* CI-Examples/
cp -rf $WORKSPACE/test_workloads.py . 
cp -rf $WORKSPACE/utils/openvino_setup.sh CI-Examples/openvino/
cp -rf $WORKSPACE/utils/tfserving CI-Examples/

if [[ "$SGX" == 1 ]]; then
  if [[ -d ~/jenkins/sd-test ]]; then
    cp -rf ~/jenkins/sd-test/* CI-Examples/sd-test/
  fi
  cp -f $WORKSPACE/Patch/rename_protected_file.patch .
  git apply rename_protected_file.patch
fi

sed -i 's/.release  = "3.10.0"/.release  = "5.10.0"/' libos/src/sys/libos_uname.c

if [[ "$base_os" == *"centos"* ]]; then
  echo "setting up workspace for centos"
  cp -rf $WORKSPACE/utils/rust_centos_setup/* CI-Examples/rust/
fi

if [[ "$GRAMINE_MUSL" == "1" ]] || [[ "$base_os" = *"alpine"* ]]; then
  chmod +x $WORKSPACE/ci/resources/setup_musl.sh
  bash $WORKSPACE/ci/resources/setup_musl.sh
fi

if [[ "$base_os" != *"alpine"* ]]; then
  cd $WORKSPACE
  chmod +x $WORKSPACE/ci/resources/setup_ltp.sh
  bash $WORKSPACE/ci/resources/setup_ltp.sh
fi

if [[ "$node_label" == "graphene_oot" ]]; then
  cd $WORKSPACE
  for i in $(find -name '*manifest.template');
  do
    sed -i 's/sgx.use_exinfo/sgx.insecure__allow_memfaults_without_exinfo/' $i;
  done;
fi

# Temporary fix
cd $WORKSPACE/gramine
sed -i 's/wrk -c /wrk -R 10000 -c /' CI-Examples/common_tools/benchmark-http.sh
