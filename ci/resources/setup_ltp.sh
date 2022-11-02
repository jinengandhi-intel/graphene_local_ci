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
if [[ "$base_os" != *"centos"* ]] && [[ "$base_os" != *"ubuntu"* ]]
then
    cp -f manifest_RHEL.template manifest.template
fi

if [[ "$base_os" == *"18.04"* ]]
then
    cp -f manifest_18_04.template manifest.template
fi
if [[ "$base_os" == *"20.04"* ]] || [[ "$base_os" == *"22.04"* ]]
then
    cp -f manifest_20_04_21_10.template manifest.template
fi
