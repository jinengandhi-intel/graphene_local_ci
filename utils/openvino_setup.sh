if [ "${os_release_id}" = "ubuntu" ]
then
    if [ "${os_version}" = "18.04" ]
    then
        wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4.2/l_openvino_toolkit_dev_ubuntu18_p_2021.4.752.tgz
        tar xzf l_openvino_toolkit_dev_ubuntu18_p_2021.4.752.tgz
        mv ./l_openvino_toolkit_dev_ubuntu18_p_2021.4.752 openvino_2021
    elif [ "${os_version}" = "20.04" ]
    then
        wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4.2/l_openvino_toolkit_dev_ubuntu20_p_2021.4.752.tgz
        tar xzf l_openvino_toolkit_dev_ubuntu20_p_2021.4.752.tgz
        mv ./l_openvino_toolkit_dev_ubuntu20_p_2021.4.752 openvino_2021
    fi

elif [ "${os_release_id}" = "rhel" ]
then
    wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2021.4.2/l_openvino_toolkit_dev_rhel8_p_2021.4.752.tgz
    tar xzf l_openvino_toolkit_dev_rhel8_p_2021.4.752.tgz
    mv ./l_openvino_toolkit_dev_rhel8_p_2021.4.752 openvino_2021
fi