#!/bin/bash
set -x

cp -rf $WORKSPACE/test_workloads.py . 
cp -rf $WORKSPACE/verify_package_version.py . 

if [[ "$base_os" == *"ubi"* ]]; then
    cp -rf /etc/yum.repos.d/redhat.repo .
    cp -rf /etc/rhsm/ca/redhat-uep.pem .
    cp -rf /etc/pki/entitlement/ .
fi