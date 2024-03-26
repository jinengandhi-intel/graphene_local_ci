import os

FRAMEWORK_HOME_DIR = os.getcwd()
GRAMINE_HOME_DIR = FRAMEWORK_HOME_DIR + "/gramine"
LIBFUZZER_DIR = FRAMEWORK_HOME_DIR + "/src"
BASH_DIR = FRAMEWORK_HOME_DIR + "/src/bash"
LIBFUZZER_CORPUS_DIR = os.path.join(LIBFUZZER_DIR, 'corpus')
LOGS_DIR = FRAMEWORK_HOME_DIR + "/logs"
LIBFUZZER_LOGS_DIR = os.path.join(LOGS_DIR, 'libfuzzer')
BASH_LOGS_DIR = os.path.join(LOGS_DIR, 'bash')
PYTORCH_DIR = FRAMEWORK_HOME_DIR + "/examples/pytorch"
HTTP_PROXY = "http://proxy-dmz.intel.com:911/"
HTTPS_PROXY = "http://proxy-dmz.intel.com:912/"
NO_PROXY = "intel.com,.intel.com,127.0.0.1,10.0.0.0/8,192.168.0.0./16,localhost,127.0.0.0/8,134.134.0.0/16"
SYSTEM_PACKAGES_FILE = "system_packages.yaml"
PYTHON_PACKAGES_FILE = "python_packages.yaml"
PKG_INSTALL_WAIT_TIME = 25
TEST_SLEEP_TIME_BW_ITERATIONS = 15
BUILD_TYPE = "release"
BUILD_PREFIX = FRAMEWORK_HOME_DIR + "/gramine_install/usr"
ITERATIONS = int(os.environ.get('iterations', '5'))
TIMEOUT = int(os.environ.get('timeout', '120'))

# Commands constants
GRAMINE_CLONE_CMD = "git clone https://github.com/gramineproject/gramine.git"
EXAMPLES_REPO_CLONE_CMD = "git clone https://github.com/gramineproject/examples.git"

BUILD_TYPE_PREFIX_STRING = "--prefix=" + BUILD_PREFIX + " --buildtype=" + BUILD_TYPE

GRAMINE_SGX_SED_CMD = "sed -i \"/uname/ a '/usr/src/linux-headers-@0@/arch/x86/include/uapi'.format(run_command('uname', '-r').stdout().split('-generic')[0].strip()),\" meson.build"

GRAMINE_BUILD_MESON_CMD = "meson setup build/ --werror " + \
                        BUILD_TYPE_PREFIX_STRING + \
                        " -Ddirect=enabled -Dsgx=enabled > " + \
                        LOGS_DIR + "/gramine_build_meson_cmd_output.txt"

GRAMINE_NINJA_BUILD_CMD = "ninja -vC build > " + LOGS_DIR + "/gramine_ninja_build_cmd_output.txt"

GRAMINE_NINJA_INSTALL_CMD = "ninja -vC build install > " + LOGS_DIR + "/gramine_ninja_install_cmd_output.txt"

PYTHONPATH_CMD = "gramine/scripts/get-python-platlib.py " + BUILD_PREFIX

GRAMINE_SGX_GEN_PRIVATE_KEY_CMD = "gramine-sgx-gen-private-key -f"

APT_UPDATE_CMD = "sudo apt-get update"

APT_FIX_BROKEN_CMD = "sudo apt --fix-broken install -y"

SYS_PACKAGES_CMD = "sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y "

# -U option is to install the latest package (if upgrade is available).
PYTHON_PACKAGES_CMD = "python3 -m pip install -U "

PIP_UPGRADE_CMD = "python3 -m pip install --upgrade pip"

LOG_LEVEL = "error"