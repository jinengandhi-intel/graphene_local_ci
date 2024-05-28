import os
import time
import shutil
import pytest
from common.config.constants import *
from libs import utils


def fresh_gramine_checkout():
    """
    Function to perform a fresh checkout of gramine repo.
    :return:
    """
    print("\n###### In fresh_gramine_checkout #####\n")
    # Check if gramine folder exists. Delete it if exists, change directory to
    # user's home directory and git clone gramine within user's home dir.
    # Note: No need to create 'gramine' dir explicitly, as git clone will
    # automatically create one.
    # Also, note that we are checking out gramine everytime we execute the
    # performance framework, so that we execute it on the latest source.
    if os.path.exists(GRAMINE_HOME_DIR):
        shutil.rmtree(GRAMINE_HOME_DIR)
    
    gramine_repo = os.environ['gramine_repo']
    print(f"\n-- Cloning Gramine git repo: {gramine_repo}\n")
    if gramine_repo != '':
        utils.exec_shell_cmd(f"git clone {gramine_repo}", None)
    else:
        utils.exec_shell_cmd(GRAMINE_CLONE_CMD, None)
        
    # Git clone the examples repo too for workloads download.
    os.chdir(GRAMINE_HOME_DIR)
    gramine_commit = os.environ["gramine_commit"] or 'master'
    if gramine_commit == 'master':
        gramine_commit = utils.exec_shell_cmd("git rev-parse HEAD")
        os.environ["gramine_commit"] = gramine_commit        
    else:
        utils.exec_shell_cmd(f"git checkout {gramine_commit}", None)

    os.chdir(FRAMEWORK_HOME_DIR)


def setup_gramine_environment():
    # Update the following environment variables as the gramine binaries can be
    # installed at some other place other than '/usr/local'
    # PATH, PYTHONPATH and PKG_CONFIG_PATH
    # Need to update these variables only after building gramine as there would be some
    # dereferences of few path values which are created only after successful build.

    utils.update_env_variables(BUILD_PREFIX)

    print("\n-- Generating gramine-sgx private key..\n", GRAMINE_SGX_GEN_PRIVATE_KEY_CMD)
    utils.exec_shell_cmd(GRAMINE_SGX_GEN_PRIVATE_KEY_CMD)


def install_gramine_dependencies():
    print("\n###### In install_gramine_dependencies #####\n")

    # Read the system packages yaml file and update the actual system_packages string
    system_packages_path = os.path.join(FRAMEWORK_HOME_DIR, 'common/config', SYSTEM_PACKAGES_FILE)
    system_packages = utils.read_config_yaml(system_packages_path)
    system_packages_str = system_packages['Default']

    # Read the python packages yaml file and update the actual python_packages string
    python_packages_path = os.path.join(FRAMEWORK_HOME_DIR, 'common/config', PYTHON_PACKAGES_FILE)
    python_packages = utils.read_config_yaml(python_packages_path)
    python_packages_str = python_packages['Default']


    print("\n-- Executing below mentioned system update cmd..\n", APT_UPDATE_CMD)
    utils.exec_shell_cmd(APT_UPDATE_CMD)
    time.sleep(PKG_INSTALL_WAIT_TIME)

    print("\n-- Executing below mentioned apt --fix-broken cmd..\n", APT_FIX_BROKEN_CMD)
    utils.exec_shell_cmd(APT_FIX_BROKEN_CMD)
    time.sleep(PKG_INSTALL_WAIT_TIME)

    system_packages_cmd = SYS_PACKAGES_CMD + system_packages_str
    print("\n-- Executing below mentioned system packages installation cmd..\n", system_packages_cmd)
    utils.exec_shell_cmd(system_packages_cmd)
    time.sleep(PKG_INSTALL_WAIT_TIME)

    python_packages_cmd = PYTHON_PACKAGES_CMD + python_packages_str
    print("\n-- Executing below mentioned Python packages installation cmd..\n", python_packages_cmd)
    utils.exec_shell_cmd(python_packages_cmd)
    

def build_and_install_gramine():
    print("\n###### In build_and_install_gramine #####\n")
    
    # Change dir to above checked out gramine folder and
    # start building the same.
    os.chdir(GRAMINE_HOME_DIR)

    # Create prefix dir
    print(f"\n-- Creating build prefix directory '{BUILD_PREFIX}'..\n")
    # In the below makedirs call, if the target directory already exists an OSError is raised
    # if 'exist_ok' value is False. Otherwise, True value leaves the directory unaltered. 
    os.makedirs(BUILD_PREFIX, exist_ok=True)

    print("\n-- Executing below mentioned gramine-sgx sed cmd..\n", GRAMINE_SGX_SED_CMD)
    utils.exec_shell_cmd(GRAMINE_SGX_SED_CMD)
        
    print("\n-- Executing below mentioned gramine build meson build cmd..\n", GRAMINE_BUILD_MESON_CMD)
    utils.exec_shell_cmd(GRAMINE_BUILD_MESON_CMD)
    
    print("\n-- Executing below mentioned gramine ninja build cmd..\n", GRAMINE_NINJA_BUILD_CMD)
    utils.exec_shell_cmd(GRAMINE_NINJA_BUILD_CMD)

    print("\n-- Executing below mentioned gramine ninja build install cmd..\n", GRAMINE_NINJA_INSTALL_CMD)
    utils.exec_shell_cmd(GRAMINE_NINJA_INSTALL_CMD)
     
    os.chdir(FRAMEWORK_HOME_DIR)

def install_gramine_binaries():
    fresh_gramine_checkout()    
    install_gramine_dependencies()
    build_and_install_gramine()   
    setup_gramine_environment()