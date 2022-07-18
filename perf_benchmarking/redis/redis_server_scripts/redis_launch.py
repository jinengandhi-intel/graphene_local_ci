import argparse
import os
import shutil
import subprocess
import sys
import time

WORKSPACE=os.getenv("WORKSPACE")
REDIS_PATH=WORKSPACE+"/CI-Examples/redis"
SCRIPTS_PATH=WORKSPACE+"/CI-Examples/redis/redis_server_scripts"
RSERVER_SIZE_GB=4
RSERVER_SIZE = RSERVER_SIZE_GB * 1024 * 1024 * 1024

def myparser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--function', '-f', 
        choices=['run_all', 'build_graphene_env', 'setup_server','run_redis', 'run_redis_benchmark', 'kill_redis'], 
        help='Function to execute', 
        required=True)

    parser.add_argument(
        '--config', '-c', 
        choices=[
            'native', 
            'graphene', 
            'graphene_sgx_exitless_no_pinning',
            'graphene_sgx_exitless_skt0_pinning',
            'graphene_sgx_same_core', 
            'graphene_sgx_diff_core', 
            'graphene_sgx_single_thread', 
            'graphene_sgx_single_thread_exitless',
            'native_w_strace'
            ], 
        help='redis configuration to launch', 
        required=False,
        default=None)

    parser.add_argument(
        '--port', '-p',
        help='redis port number', 
        required=False,
        default='9001')    

    args = parser.parse_args()
    return args


def setup_server():
    print("\nSetting up server OS parameters ...")		
    os.system("echo never > /sys/kernel/mm/transparent_hugepage/enabled")
    os.system("echo 1 > /proc/sys/vm/overcommit_memory")
    os.system("echo 3 > /proc/sys/vm/drop_caches")
    os.system("sysctl -w net.core.somaxconn=65535 > /dev/null")
    os.system("swapoff -a")
    
    time.sleep(1)
    
    print("\nChecking values ...\n")		
    os.system("echo 'Checking Server setup: '")
    os.system("echo -e '\tHuge pages - Never'")
    os.system("cat /sys/kernel/mm/transparent_hugepage/enabled")
    os.system("echo ''")
    os.system("echo -e '\tOvercommit_memory > 1'")
    os.system("cat /proc/sys/vm/overcommit_memory")
    os.system("echo ''")
    os.system("echo -e '\tClearing cache > 3'")
    # os.system("cat /proc/sys/vm/drop_caches")
    os.system("echo ''")
    os.system("echo -e '\tMax number of connections >65K'")
    os.system("cat /proc/sys/net/core/somaxconn")

    #os.system("service irqbalance stop")
    
    print("\nIf values are not as expected stop the test!!!\n")
    time.sleep(2)

def kill_redis(force=False):
    cmd = "ps -e | grep 'redis\|pal'"
    results = os.popen(cmd).read()
    print(results)
    if len(results.split()) > 1:
        pid = results.split()[0]

        if force:
            cmd = f'kill -9 {pid}'
        else:
            cmd = f'kill {pid}'

        os.system(cmd)

def run_redis_benchmark(port):
    CWD=os.getcwd()
    os.chdir(REDIS_PATH)

    cmd = f"src/src/redis-benchmark -p {port}"
    print(cmd)
    os.system(cmd)

    os.chdir(CWD)

def build_graphene_env(exitless=False):
    CWD=os.getcwd()

    os.chdir(REDIS_PATH)

    if exitless:
        print("\n exitless true")
        redis_graphene_manifest_template = SCRIPTS_PATH + os.sep + 'redis-server.manifest.template.exitless'
    else:
        redis_graphene_manifest_template = SCRIPTS_PATH + os.sep + 'redis-server.manifest.template'
    
    dst_file = REDIS_PATH + os.sep + 'redis-server.manifest.template'
    shutil.copy(redis_graphene_manifest_template, dst_file)

    cmd='make clean;make SGX=1'
    os.system(cmd)

    os.chdir(CWD)

def run_redis(config, port):
    # Store current directory
    CWD=os.getcwd()

    # Move to REDIS directory
    os.chdir(REDIS_PATH)

    # Based on config, format command
    redis_cmd = f"./redis-server --port {port} --maxmemory {RSERVER_SIZE} --maxmemory-policy allkeys-lru --appendonly no --protected-mode no --save '' &"

    if config == 'native':
        build_graphene_env()
        cmd=f"numactl -C 1 " + redis_cmd
        #cmd=f" " + redis_cmd
    elif config == 'native_w_strace':
        cmd=f"strace -o strace_output.txt numactl -C 1 " + redis_cmd
    elif config == 'graphene':
        build_graphene_env()
        cmd=f"numactl -C 1 gramine-direct " + redis_cmd
       # cmd=f" ./pal_loader " + redis_cmd
    elif config == 'graphene_sgx_single_thread':
        build_graphene_env()
        cmd=f" numactl -C 1 gramine-sgx " + redis_cmd
       # cmd=f"SGX=1 ./pal_loader " + redis_cmd
    elif config == 'graphene_sgx_exitless_no_pinning':
        build_graphene_env(exitless=True)
        cmd=f"SGX=1 ./pal_loader " + redis_cmd
    elif config == 'graphene_sgx_exitless_skt0_pinning':
        build_graphene_env(exitless=True)
        cmd=f"SGX=1 numactl -C1-39,81-119 ./pal_loader " + redis_cmd
    elif config == 'graphene_sgx_same_core':
        build_graphene_env(exitless=True)
        cmd=f" numactl -C 1,77 gramine-sgx " + redis_cmd
    elif config == 'graphene_sgx_diff_core':
        build_graphene_env(exitless=True)
        cmd=f" numactl -C 1,2 gramine-sgx " + redis_cmd
    elif config == 'graphene_sgx_single_thread_exitless':
        build_graphene_env(exitless=True)
        cmd=f" numactl -C 1 gramine-sgx " + redis_cmd
    else:
        print(f'ERROR: Invalid Config - {config}')
        return

    # Print/Execute command
    print(cmd)
    os.system(cmd)

    # Restore current directory
    os.chdir(CWD)

    # Add some buffer time to allow redis to start
    time.sleep(10)

def main(function, config=None, port='9001'):
    if function == 'run_redis':
        run_redis(config, port)
    elif function == 'run_redis_benchmark':
        run_redis_benchmark(port)
    elif function == 'kill_redis':
        kill_redis()
    elif function == 'run_all':
        setup_server()
        run_redis(config, port)
        run_redis_benchmark(port)
        kill_redis()
    elif function == 'setup_server':
        setup_server()
    elif function == 'build_graphene_env':
        if (config == 'graphene_sgx_same_core') | (config == 'graphene_sgx_diff_core'):
            build_graphene_env(exitless=True)
        else:
            build_graphene_env()
    else:
        print(f'ERROR: Unsupported function: {function}')

if __name__ == "__main__":
    myargs = myparser()
    # print(myargs)
    main(function=myargs.function, config=myargs.config, port=myargs.port)
