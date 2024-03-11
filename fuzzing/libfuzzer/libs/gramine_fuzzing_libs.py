import os
from libs import utils
from common.config.constants import *
import subprocess
import shlex


def build_libfuzzer(filesize):
    with open(os.path.join(LIBFUZZER_CORPUS_DIR, str(filesize)), 'wb') as file:
        file.write(os.urandom(filesize))
    print("\n----------------------------------build_libfuzzer----------------------------------\n")
    utils.exec_shell_cmd('clang -g -fsanitize=fuzzer example.c -o example_fuzzer')
    utils.exec_shell_cmd('gramine-sgx-pf-crypt encrypt -w files/wrap_key -i corpus -o cipher_corpus')

def initialize_gramine_sgx():
    print("\n----------------------------------initialize_gramine_sgx----------------------------------\n")
    utils.exec_shell_cmd('make clean')
    utils.exec_shell_cmd('make SGX=1')

def run_libfuzzer(filesize, testname, iterations=1, timeout=0):
    build_libfuzzer(filesize)
    initialize_gramine_sgx()
    for i in range(iterations):
        output = utils.exec_shell_popen('gramine-sgx libfuzz cipher_corpus', testname, timeout)
        print('output of the libfuzzer ' + str(output))
        if output not in (0, -9):
            print("gramine libfuzzer execution is failed....")
            return False
    return True

def get_insecure_key_value(manifest_file):
    result = ""
    with open(manifest_file) as manifest:
        for line in manifest:
            key, value = line.partition("=")[::2]
            if key.strip() == "fs.insecure__keys.wrap_key":
                result = value.rstrip()
                break
    return result

def run_libfuzzer_verifier(log_file):
    try:
        result = subprocess.check_output('gramine-sgx ./bash -c "./dir_loop.sh"', shell=True)
    except subprocess.CalledProcessError as exc:
        print("error code : ", grepexc.returncode, grepexc.output)
    finally:
        log = f"{BASH_LOGS_DIR}/{log_file}.log"
        file = open(log, "w+b")
        file.write(result)
        file.close()
        print("decrypted contents of cipher_corpus directory is copied : " + log)

def verify_libfuzzer(log_file):
    os.chdir(BASH_DIR)
    utils.exec_shell_cmd(f"cp -rf {LIBFUZZER_DIR}/cipher_corpus/*  cipher_corpus/")
    utils.exec_shell_cmd(f"cp -rf {LIBFUZZER_DIR}/files/*  files/")

    insecure_key_value = get_insecure_key_value(os.path.join(LIBFUZZER_DIR, 'libfuzz.manifest.template'))
    utils.exec_shell_cmd(f"sed -i 's/^fs.insecure__keys.wrap_key.*/fs.insecure__keys.wrap_key ={insecure_key_value}/' manifest.template")
    utils.exec_shell_cmd('chmod +x dir_loop.sh')

    initialize_gramine_sgx()
    print("verification process started.....")                                                                                                                                          
    run_libfuzzer_verifier(log_file)

def verify_process(process, expected_output, log_file):
    result = False
    process_output = ''
    try:
        while True:
            output = process.stdout.readline()
            print(output)
            process_output += output
            if expected_output in process_output:
                result = True
                break
            if process.poll() is not None and output == '':
                break
    finally:
        process.stdout.close()
        utils.kill(process.pid)
        utils.write_log(process_output, log_file)
    return result


def run_libfuzzer_corrupt(filesize, testname):
    build_libfuzzer(filesize)
    utils.exec_shell_cmd('mkdir corrupt_file')
    utils.exec_shell_cmd(f"gramine-sgx-pf-tamper -w files/wrap_key -i cipher_corpus/{filesize} -o corrupt_file")
    utils.exec_shell_cmd(f"sed -i 's/^loader.log_level.*/loader.log_level = \"debug\"/' libfuzz.manifest.template")
    utils.exec_shell_cmd('rm -rf cipher_corpus && mv corrupt_file cipher_corpus')
    initialize_gramine_sgx()
    process = subprocess.Popen(shlex.split("gramine-sgx libfuzz cipher_corpus"), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    return verify_process(process, "[P1:T1:example_fuzzer] warning: pf_open failed: Invalid header", testname)


def run_libfuzzer_wrong_insecure_key(filesize, testname, insecure_key_value):
    build_libfuzzer(filesize)
    utils.exec_shell_cmd(f"sed -i 's/^fs.insecure__keys.wrap_key.*/fs.insecure__keys.wrap_key ={insecure_key_value}/' libfuzz.manifest.template")
    initialize_gramine_sgx()
    process = subprocess.Popen(shlex.split("gramine-sgx libfuzz cipher_corpus"), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    return verify_process(process, "Cannot parse hex key: 'F558C'", testname)