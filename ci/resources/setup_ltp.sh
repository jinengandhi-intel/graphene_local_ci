#!/bin/bash
set -x

cd $WORKSPACE/gramine
cp -rf $WORKSPACE/ltp_src libos/test/ltp/
cp -rf $WORKSPACE/ltp_config/* libos/test/ltp/
cp -rf $WORKSPACE/ltp_scripts/* scripts/

cd libos/test/ltp
if [ "${SGX}" == "1" ]
then
    cp -f toml_files/tests_sgx.toml tests.toml
else
    cp -f toml_files/tests_direct.toml tests.toml
fi

if [[ "$base_os" == *"centos"* ]]
then
    cp -f manifest_CentOS.template manifest.template
fi

if [[ "$base_os" == *"rhel"* ]]
then
    cp -f manifest_RHEL.template manifest.template
fi

if [[ "$base_os" == *"ubuntu"* ]]
then
    cp -f manifest_20_04_21_10.template manifest.template
fi

if [[ "$base_os" == *"debian"* ]]
then
    cp -f manifest_Debian_11.template manifest.template
fi
