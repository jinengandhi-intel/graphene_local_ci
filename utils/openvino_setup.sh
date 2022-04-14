#!/bin/bash
wget https://apt.repos.intel.com/openvino/2021/GPG-PUB-KEY-INTEL-OPENVINO-2021
sudo apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2021
echo "deb https://apt.repos.intel.com/openvino/2021 all main" | sudo tee /etc/apt/sources.list.d/intel-openvino-2021.list
sudo apt update
if [ "${os_version}" = "18.04" ]
then
    sudo apt-get install -y intel-openvino-dev-ubuntu18-2021.4.752
elif [ "${os_version}" = "20.04" ]
then
    sudo apt-get install -y intel-openvino-dev-ubuntu20-2021.4.752
fi