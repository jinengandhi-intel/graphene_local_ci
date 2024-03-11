import pytest
import os
from libs import utils
from libs import gramine_libs
from common.config.constants import *

@pytest.fixture(scope="session", autouse=True)
def gramine_setup():
    print_env_variables()

    # Delete old logs if any and create new logs directory.
    if os.path.exists(LOGS_DIR):
        del_logs_cmd = 'rm -rf ' + LOGS_DIR
        os.system(del_logs_cmd)

    os.makedirs(LOGS_DIR, exist_ok=True)

    gramine_libs.install_gramine_binaries()
    
    utils.exec_shell_cmd(f"mkdir {BASH_LOGS_DIR}")
    utils.exec_shell_cmd(f"mkdir {LIBFUZZER_LOGS_DIR}")


def print_env_variables():
    if not (os.environ.get("gramine_repo",None) or os.environ.get("gramine_repo",None)):
        pytest.exit("\n***** Either gramine_repo or gramine_repo variable is not defined*****")
    os.environ["gramine_repo"] = os.environ.get("gramine_repo", "")
    os.environ["gramine_commit"]  = os.environ.get("gramine_commit", "")
    print("\n\n############################################################################")
    print("Printing the environment variables")
    print("Gramine Commit: ", os.environ["gramine_commit"])
    print("Gramine Repo:       ", os.environ["gramine_repo"])
    print("############################################################################\n\n")

@pytest.fixture(scope="function", autouse=True)
def setup_libfuzzer():
    print("\n----------------------------------setup_libfuzzer----------------------------------\n")
    os.chdir(BASH_DIR)
    utils.exec_shell_cmd('rm -rf cipher_corpus/* files/*')
    os.chdir(LIBFUZZER_DIR)
    utils.exec_shell_cmd('rm -rf corpus cipher_corpus libfuzz_gramine-sgx.log')
    utils.exec_shell_cmd('mkdir corpus')

