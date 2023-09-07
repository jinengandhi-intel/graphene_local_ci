#!/usr/bin/env bash
set -ex

if [[ "$BUILD_OS" = *"ubuntu"* ]]; then
    apt-get update && env DEBIAN_FRONTEND=noninteractive apt-get install -y python3
elif [[ "$BUILD_OS" = "centos:8" ]]; then
    sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-*
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-*
    echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf && yum update -y && yum install -y python3
elif [[ "$BUILD_OS" = "redhat/ubi8:8.8" ]]; then
    yum update -y && yum install -y python3
elif [[ "$BUILD_OS" = "redhat/ubi8-minimal:8.8" ]]; then
    microdnf update -y && microdnf install -y python3;
fi