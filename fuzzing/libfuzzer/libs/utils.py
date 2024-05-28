import sys
import yaml
import time
import shutil
import socket
import psutil
import subprocess
import csv
from datetime import datetime
import collections
import pkg_resources
import socket
import netifaces as ni
import re
from common.config.constants import *
from threading import Timer
import shlex
import pandas  as pd
from pandas import ExcelWriter
import os


def kill(proc_pid):
    try:
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.terminate()
        process.terminate()
    except:
        pass


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


def exec_shell_popen(cmd, log_file, timeout):
    print(f"Process started by running this command : {cmd}")
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, encoding="utf-8")
    process_output = ''
    try:
        if timeout!=0:
            timer = Timer(timeout, process.kill)
            timer.start()
        while True:
            output = process.stdout.readline()
            current_time = datetime.now().strftime("%H:%M:%S")
            output = f"{current_time} : {output}"
            print(output.strip())
            process_output += output
            if process.poll() is not None:
                break
    finally:
        if timeout!=0:
            timer.cancel()
        process.stdout.close()
        current_time = datetime.now().strftime("%H:%M:%S")
        process_output +=  f"\n the process got terminated at {current_time}\n"
        write_log(process_output, log_file)
    return process.returncode


def read_config_yaml(config_file_path):
    with open(config_file_path, "r") as config_fd:
        try:
            config_dict = yaml.safe_load(config_fd)
        except yaml.YAMLError as exc:
            raise Exception(exc)
    return config_dict

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
    
def write_excel(data):
    df = pd.DataFrame([data])
    print(df)
    filename = 'libfuzzer.xlsx'
    path = f"{FRAMEWORK_HOME_DIR}/{filename}"
    if os.path.isfile(path):
        print('file exist')
        with pd.ExcelWriter(path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row, index=False, header=False)
    else:
        print('creating new file')
        df.to_excel(path,'Sheet1', index=False)        
    
    
def generate_report(testname, filesize, timeout, iterations):
    log_file = f"{LIBFUZZER_LOGS_DIR}/{testname}.log"
    content = open(log_file).read()
    initial_corpus = re.findall(r'INFO:\s*([\d]+)', content)[0]
    final_corpus = re.findall(r'INFO:\s*([\d]+)', content)[-1]
    mutation = re.findall(r'#([\d]+)', content)[-1]
    print('initial_corpus : ' + initial_corpus)
    print('final_corpus : ' + final_corpus)
    print('mutation : ' + mutation)
    
    data = {'filesize(Bytes)' : filesize,
        'initial_corpus' : initial_corpus,
        'final_corpus' : final_corpus,
        'mutation' : mutation,
        'iterations' : iterations,
        'timeout_per_iterations(sec)' : timeout,
      }
      
    write_excel(data)
    

def generate_pytorch_pre_trained_model():
    os.chdir(FRAMEWORK_HOME_DIR)
    print(f"\nexecuting {EXAMPLES_REPO_CLONE_CMD} ...")
    exec_shell_cmd(EXAMPLES_REPO_CLONE_CMD, None)
    os.chdir(PYTORCH_DIR)
    print("\nexecuting 'python3 download-pretrained-model.py' ...")
    exec_shell_cmd('python3 download-pretrained-model.py')
    exec_shell_cmd(f"cp alexnet-pretrained.pt {LIBFUZZER_CORPUS_DIR}/")
    os.chdir(LIBFUZZER_DIR)

