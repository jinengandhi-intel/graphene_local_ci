import os
from libs import utils
from common.config.constants import *
import subprocess


def build_libfuzzer(filesize):
    with open(os.path.join(LIBFUZZER_CORPUS_DIR, str(filesize)), 'wb') as file:
        file.write(os.urandom(filesize))
    print(utils.exec_shell_cmd('clang -g -fsanitize=fuzzer example.c -o example_fuzzer'))
    print(utils.exec_shell_cmd('gramine-sgx-pf-crypt encrypt -w files/wrap_key -i corpus -o cipher_corpus'))
    print(utils.exec_shell_cmd('make clean'))
    print(utils.exec_shell_cmd('make SGX=1'))

def run_libfuzzer(testname):
    for i in range(5):
        output = utils.exec_shell_popen('gramine-sgx libfuzz cipher_corpus', testname, 120)
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

    print(utils.exec_shell_cmd('make clean'))
    print(utils.exec_shell_cmd('make SGX=1'))
    print("verification process started.....")
    run_libfuzzer_verifier(log_file)


def run_libfuzzer_corrupt():
    with open(os.path.join(LIBFUZZER_CORPUS_DIR, str(filesize)), 'wb') as file:
        file.write(os.urandom(filesize))
    print(utils.exec_shell_cmd('clang -g -fsanitize=fuzzer example.c -o example_fuzzer'))
    print(utils.exec_shell_cmd('gramine-sgx-pf-crypt encrypt -w files/wrap_key -i corpus -o cipher_corpus'))
    print(utils.exec_shell_cmd('gramine-sgx-pf-tamper -w files/wrap_key -i cipher_corpus -o corrupt_file'))
    print(utils.exec_shell_cmd('make clean'))
    print(utils.exec_shell_cmd('make SGX=1'))
    output = utils.exec_shell_popen('gramine-sgx libfuzz corrupt_file')
    if output == 0:
        return True
    else:
        return False