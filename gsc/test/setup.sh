#!/usr/bin/env bash
set -ex

if [[ "$BUILD_OS" = *"ubuntu"* ]]; then
    apt-get update && env DEBIAN_FRONTEND=noninteractive apt-get install -y python3
elif [[ "$BUILD_OS" = "redhat/ubi9:9.4" ]] || [[ "$BUILD_OS" = *"quay.io/centos/centos"* ]]; then
    yum update -y && yum install -y python3
elif [[ "$BUILD_OS" = "redhat/ubi9-minimal:9.4" ]]; then
    microdnf install -y python3;
elif [[ "$BUILD_OS" = "registry.suse.com/suse/sle15:15.4" ]]; then
    zypper -n update  && zypper -n install python3;
fi
