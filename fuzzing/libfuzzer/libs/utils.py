import sys
import yaml
import time
import shutil
import socket
import psutil
import subprocess
import lsb_release
import csv
from datetime import datetime as dt
import collections
import pkg_resources
import socket
import netifaces as ni
import re
from common.config.constants import *
from threading import Timer
import shlex


def exec_shell_cmd(cmd, stdout_val=subprocess.PIPE):
    try:
        cmd_stdout = subprocess.run([cmd], shell=True, check=True, stdout=stdout_val, stderr=subprocess.STDOUT, universal_newlines=True)

        if stdout_val is not None and cmd_stdout.stdout is not None:
            return cmd_stdout.stdout.strip()

        return cmd_stdout

    except subprocess.CalledProcessError as e:
        print(e.output)


def write_log(content, log_file):
    log = f"{LIBFUZZER_LOGS_DIR}/{log_file}.log"
    fd = open(log, "a+")
    fd.write(content)
    fd.write("\n")
    fd.close()
    print("logs contents are copied " + log)


def exec_shell_popen(cmd, log_file, timeout=0):
    print(f"Process started by running this command : {cmd}")
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, encoding="utf-8")
    process_output = ''
    try:
        if timeout!=0:
            timer = Timer(timeout, process.kill)
            timer.start()
        while True:
            output = process.stdout.readline()
            print(output)
            process_output += output
            if process.poll() is not None and output == '':
                break
    finally:
        if timeout!=0:
            timer.cancel()
        process.stdout.close()
        write_log(process_output, log_file)
    return process.returncode


def read_config_yaml(config_file_path):
    with open(config_file_path, "r") as config_fd:
        try:
            config_dict = yaml.safe_load(config_fd)
        except yaml.YAMLError as exc:
            raise Exception(exc)
    return config_dict


def get_distro_and_version():
    distro = lsb_release.get_distro_information().get('ID').lower()
    distro_version = lsb_release.get_distro_information().get('RELEASE')
    return distro, distro_version


def clear_system_cache():
    """
    Function to clear pagecache, dentries, and inodes. We need to clear system cache to get
    consistent results.
    :return:
    """
    echo_cmd_path = exec_shell_cmd('which echo')
    clear_cache_cmd = "sudo sh -c \"" + echo_cmd_path + " 3 > /proc/sys/vm/drop_caches\""
    print("\n-- Executing clear cache command..", clear_cache_cmd)
    exec_shell_cmd(clear_cache_cmd, None)


def clean_up_system():
    """
    Function to cleanup to remove unwanted packages and their dependencies, pagecache,
    dentries, inodes and apt cache.
    :return:
    """
    # Cleanup existing gramine binaries (if any) before starting a fresh build.
    # Passing prefix path as argument, so that user installed (if any) gramine
    # binaries are also removed.
    cleanup_gramine_binaries(BUILD_PREFIX)

    try:
        print("\n-- Removing unnecessary packages and dependencies..")
        exec_shell_cmd("sudo apt-get -y autoremove", None)
    except:
        print("\n-- Executing apt --fix-broken cmd..\n", APT_FIX_BROKEN_CMD)
        exec_shell_cmd(APT_FIX_BROKEN_CMD, None)
    print("\n-- Clearing thumbnail cache..")
    exec_shell_cmd("sudo rm -rf ~/.cache/thumbnails/*", None)
    print("\n-- Clearing apt cache..")
    exec_shell_cmd("sudo apt-get -y clean", None)

    clear_system_cache()

    print("\n-- Clearing swap memory..")
    exec_shell_cmd("sudo sh -c 'swapoff -a && swapon -a'", None)


def set_permissions():
    """
    Funciton to set appropriate permissions before triggering the perf runs.
    :return:
    """
    print("\n-- Setting required device persmissions :")
    if os.path.exists("/dev/sgx_enclave") and os.path.exists("/dev/sgx_provision"):
        exec_shell_cmd("sudo chmod 777 /dev/sgx_enclave /dev/sgx_provision")
    else:
        print("\n-- Warning - Unable to find SGX dev files. May not be able to execute workload with SGX..")
    
    logged_in_user = os.getlogin()
    if os.path.exists("/dev/cpu_dma_latency"):
        exec_shell_cmd(f"sudo chown {logged_in_user} /dev/cpu_dma_latency")
        exec_shell_cmd("sudo chmod 0666 /dev/cpu_dma_latency")
    
    exec_shell_cmd("sudo mount -o remount,exec /dev")


def cleanup_gramine_binaries(build_prefix):
    """
    Function to clean up gramine binaries from standard system paths
    and user defined installed paths (installed via "--build_prefix" option)
    :param build_prefix:
    :return:
    """
    if os.path.exists(build_prefix): shutil.rmtree(build_prefix)

    gramine_uninstall_cmd = "sudo apt-get remove -y gramine"
    python_version_str = "python" + str(sys.version_info.major) + "." + str(sys.version_info.minor)
    # The substring "x86_64-linux-gnu" within below path is for Ubuntu. It would be different
    # for other distros like CentOS or RHEL. Currently, hardcoding it for Ubuntu but needs to
    # be updated for other distros in future.
    gramine_user_installed_bin_rm_cmd = "sudo rm -rf /usr/local/bin/gramine* /usr/local/lib/" + \
                                        python_version_str + \
                                        "/dist-packages/graminelibos /usr/local/lib/x86_64-linux-gnu/*gramine*"

    print("\n-- Uninstalling gramine..\n", gramine_uninstall_cmd)
    os.system(gramine_uninstall_cmd)

    print("\n-- Removing user installed gramine binaries..\n", gramine_user_installed_bin_rm_cmd)
    os.system(gramine_user_installed_bin_rm_cmd)

def update_env_variables(build_prefix):
    """
    Function to update the following environment variables to below respective locations,
    as the gramine binaries can be installed at some other place other than '/usr/local'.
    $PATH => <build_prefix>/bin
    $PYTHONPATH => <prefix>/lib/python<version>/site-packages
    $PKG_CONFIG_PATH => <prefix>/<libdir>/pkgconfig
    :param build_prefix:
    :return:
    """
    
    os.environ["PATH"] = build_prefix + "/bin" + os.pathsep + os.environ["PATH"]
    print(f"\n-- Updated environment PATH variable to the following..\n", os.environ["PATH"])

    # Update environment 'PKG_CONFIG_PATH' variable to <prefix>/<libdir>/pkgconfig.
    libdir_path_cmd = "meson introspect " + GRAMINE_HOME_DIR + \
                    "/build/ --buildoptions | jq -r '(map(select(.name == \"libdir\"))) | map(.value) | join(\"/\")'"
    libdir_path = exec_shell_cmd(libdir_path_cmd)

    os.environ["PKG_CONFIG_PATH"] = build_prefix + "/" + libdir_path + "/pkgconfig" + os.pathsep + os.environ.get(
        'PKG_CONFIG_PATH', '')
    print(f"\n-- Updated environment PKG_CONFIG_PATH variable to the following..\n", os.environ["PKG_CONFIG_PATH"])

    print(f"\n-- PYTHONPATH command\n", PYTHONPATH_CMD)
    os.environ["PYTHONPATH"] = subprocess.check_output(PYTHONPATH_CMD, encoding='utf-8', shell=True)
    print(f"\n-- Updated environment PYTHONPATH variable to the following..\n", os.environ["PYTHONPATH"])
    print(f"\n-- Updating 'LC_ALL' env-var\n")
    os.environ['LC_ALL'] = "C.UTF-8"

    print(f"\n-- Updating 'LANG' env-var\n")
    os.environ['LANG'] = "C.UTF-8"

    print(f"\n-- Updating 'SSHPASS' env-var\n")
    os.environ['SSHPASS'] = "intel@123"

    print(f"\n-- Updating 'ARCH_LIBDIR' env-var\n")
    cmd_out = exec_shell_cmd('cc -dumpmachine')
    os.environ['ARCH_LIBDIR'] = "/lib/" + cmd_out

    print(f"\n-- Updating 'LC_ALL' env-var\n")
    os.environ['LC_ALL'] = "C.UTF-8"

    print(f"\n-- Updating 'LANG' env-var\n")
    os.environ['LANG'] = "C.UTF-8"
	
    os.environ['ENV_USER_UID'] = exec_shell_cmd('id -u')
    os.environ['ENV_USER_GID'] = exec_shell_cmd('id -g')


def set_http_proxies():
    """
    Function to set environment http and https proxies.
    :return:
    """
    os.environ['http_proxy'] = HTTP_PROXY
    os.environ['HTTP_PROXY'] = HTTP_PROXY
    os.environ['https_proxy'] = HTTPS_PROXY
    os.environ['HTTPS_PROXY'] = HTTPS_PROXY
    print("\n-- Setting http_proxy : \n", os.environ['http_proxy'])
    print("\n-- Setting https_proxy : \n", os.environ['https_proxy'])


def set_no_proxy():
    os.environ['no_proxy'] = NO_PROXY
    os.environ['NO_PROXY'] = NO_PROXY
    print("\n-- Setting no_proxy : \n", os.environ['no_proxy'])
