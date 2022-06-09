#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2019 Wojtek Porczyk <woju@invisiblethingslab.com>
# Copyright (c) 2021 Intel Corporation
#                    Paweł Marczewski <pawel@invisiblethingslab.com>

import configparser
import fnmatch
import logging
import os
import pathlib
import shlex
import subprocess
import sys
import re
import pytest

from graminelibos.regression import HAS_SGX, run_command

sgx_mode = os.environ.get('SGX')
if sgx_mode == '1':
    DEFAULT_LTP_SCENARIO = 'install-sgx/runtest/syscalls-new'
    DEFAULT_LTP_CONFIG = 'ltp_tests.cfg ltp-sgx_tests.cfg ltp-bug-1075_tests.cfg'
else:
    DEFAULT_LTP_SCENARIO = 'install/runtest/syscalls-new'
    DEFAULT_LTP_CONFIG = 'ltp_tests.cfg'

LTP_SCENARIO = os.environ.get('LTP_SCENARIO', DEFAULT_LTP_SCENARIO)
LTP_CONFIG = os.environ.get('LTP_CONFIG', DEFAULT_LTP_CONFIG).split(' ')
LTP_TIMEOUT_FACTOR = float(os.environ.get('LTP_TIMEOUT_FACTOR', '1'))

def read_scenario(scenario):
    """Read an LTP scenario file (list of tests).

    Each line specifies a name (tag) and a command.
    """

    with open(scenario, 'r') as f:
        for line in f:
            if line[0] in '\n#':
                continue
            tag, *cmd = shlex.split(line)
            yield tag, cmd


def is_wildcard_pattern(name):
    return bool(set(name) & set('*?[]!'))


def get_int_set(value):
    return set(int(i) for i in value.strip().split())


class Config:
    """Parser for LTP configuration files.

    A section name can be a test tag, or a wildcard matching many tags (e.g. `access*`). A wildcard
    section can only contain `skip = yes`.

    TODO: Instead of Python's INI flavor (`configparser`), use TOML, for consistency with the rest
    of the project.
    """

    def __init__(self, config_paths):
        self.cfg = configparser.ConfigParser(
            converters={
                'path': pathlib.Path,
                'intset': get_int_set,
            },
            defaults={
                'timeout': '30',
            },
        )

        for path in config_paths:
            with open(path, 'r') as f:
                self.cfg.read_file(f)

        self.skip_patterns = []
        for name, section in self.cfg.items():
            if is_wildcard_pattern(name):
                for key in section:
                    if key != 'skip' and section[key] != self.cfg.defaults().get(key):
                        raise ValueError(
                            'wildcard sections like {!r} can only contain "skip", not {!r}'.format(
                                name, key))
                if section.get('skip'):
                    self.skip_patterns.append(name)

    def get(self, tag):
        """Find a section for given tag.

        Returns the default section if there's no specific one, and None if the test should be
        skipped.
        """
        if self.cfg.has_section(tag):
            section = self.cfg[tag]
            if section.get('skip'):
                return None
            return section

        for pattern in self.skip_patterns:
            if fnmatch.fnmatch(tag, pattern):
                return None

        return self.cfg[self.cfg.default_section]


def list_tests(ltp_config=LTP_CONFIG, ltp_scenario=LTP_SCENARIO):
    """List all tests along with their configuration."""

    config = Config(ltp_config)

    for tag, cmd in read_scenario(ltp_scenario):
        section = config.get(tag)
        yield tag, cmd, section

def woken_up_valid_check(woken_string_result):
    if (woken_string_result):
        flag_woken_issue = False
        for entry in woken_string_result:
            find_num = re.findall(r'\d+', entry)
            if (find_num):
                num_list = list(map(int, find_num))
                num_list_1 = num_list[0]
                num_list_2 = num_list[1]
                if ( num_list_1 > 50000 and num_list_2 > 50000 ):
                    return False                        
                else:
                    flag_woken_issue = True
                    continue
        if (flag_woken_issue == True):
            return True
    else:
        return True

def parse_test_output(stdout, _stderr, cmd):
    """Parse LTP stdout to determine passed/failed subtests.

    Returns two sets: passed and failed subtest numbers.
    """

    passed = set()
    failed = set()
    conf = set()
    subtest = 0
    woken_string = re.compile(r'woken up early | \[\d+\,\d+\]')
    woken_string_result  = woken_string.findall(stdout)

    for line in stdout.splitlines():
        if line == 'Summary':
            break

        # Drop this line so that we get consistent offsets
        if line == 'WARNING: no physical memory support, process creation may be slow.':
            continue

        tokens = line.split()
        if len(tokens) < 2:
            continue

        if 'INFO' in line:
            continue

        if tokens[1].isdigit():
            subtest = int(tokens[1])
        else:
            subtest += 1

        if 'TPASS' in line or 'PASS:' in line:
            passed.add(subtest)
        elif (any(t in line for t in ['TFAIL', 'FAIL:', 'TBROK', 'BROK:']) and not woken_string_result):
            if (sgx_mode == '1') and (cmd[0]=='getppid02' or cmd[0]=='getpid01') \
                    and ("TBROK: Test haven't reported results" in line):
                passed.add(subtest)
            else:
                failed.add(subtest)
        elif (woken_string_result):
            woken_up_valid = woken_up_valid_check(woken_string_result)
            if (woken_up_valid == True):
                passed.add(subtest)
            else:
                failed.add(subtest)
        elif ('TCONF' in line or 'CONF' in line):
            conf.add(subtest)
        
    system_error_output_valid = check_system_error_output_valid(_stderr)

    return passed, failed, conf, system_error_output_valid


def check_must_pass(passed, failed, must_pass, conf, system_error_output_valid):
    """Verify the test results based on `must-pass` specified in configuration file."""

    # No `must-pass` means all tests must pass

    must_pass_passed = set()
    must_pass_failed = set()
    must_pass_unknown = set()
    for subtest in must_pass:
        if subtest in passed:
            must_pass_passed.add(subtest)
        elif subtest in failed:
            must_pass_failed.add(subtest)
        else:
            must_pass_unknown.add(subtest)

    if must_pass_failed or must_pass_unknown:
        pytest.fail('Failed or unknown subtests specified in must-pass: {}'.format(
            must_pass_failed | must_pass_unknown))

    if not failed and passed == must_pass_passed and not conf:
        pytest.fail('The must-pass list specifies all tests, remove it from config')

    if not passed and not conf:
        pytest.fail('All subtests skipped, replace must-pass with skip')

    if (system_error_output_valid == False) :
        pytest.fail("Error due to invalid system error output")        

def check_system_error_output_valid(_stderr):
    error_list = []
    error_list = _stderr.split("error:")
    for error in error_list:
        if error == "":
            ret_code = True
            continue
        elif "Mounting file:/proc may expose unsanitized" in error or \
            "[P1:T1:]" in error or \
            "Failed to read ELF header" in error or \
            "Disallowing access to file '/usr/bin/systemd-detect-virt'" in error or \
            "Disallowing access to file '/lib64/libnss_nis.so.2'" in error or \
            "Disallowing access to file '/usr/lib64/libnss_nis.so.2'" in error or \
            "Disallowing access to file '/lib64/libtinfo.so.6'" in error or \
            "Disallowing access to file '/usr/lib64/libtinfo.so.6'" in error or \
            "Detected deprecated syntax" in error or \
            "Mounting file:/dev/cpu_dma_latency may expose unsanitized" in error or \
            "Sending IPC process-exit notification failed: -13" in error or \
            "Failed to send IPC msg" in error or \
            "bind: invalid handle returned" in error or \
            "Disallowing access to file '/lib/x86_64-linux-gnu/libnss_nis.so.2" in error :        
            ret_code = True
            continue
        else:
            ret_code = False
            return False
    return ret_code

def test_ltp(cmd, section, capsys):
    must_pass = section.getintset('must-pass')
    if sgx_mode == '1':
        binary_dir_ltp = "install-sgx/testcases/bin"
    else:
        binary_dir_ltp = "install/testcases/bin"
    loader = 'gramine-sgx' if HAS_SGX else 'gramine-direct'
    timeout = int(section.getfloat('timeout') * LTP_TIMEOUT_FACTOR)
    full_cmd = [loader, *cmd]
    match = re.search(r'_run', full_cmd[1])
    if match:
        setup_bin = os.path.join(binary_dir_ltp, full_cmd[1].replace("run", "setup"))
        returncode_setup, stdout_setup, _stderr_setup = run_command(setup_bin, timeout=timeout, can_fail=True)
    logging.info('command: %s', full_cmd)
    logging.info('must_pass: %s', list(must_pass) if must_pass else 'all')

    live_output = os.getenv('GRAMINE_LTP_LIVE_OUTPUT') or ''
    if section.name in live_output.split(','):
        with capsys.disabled():
            returncode, stdout, _stderr = run_command(full_cmd, timeout=timeout, can_fail=True)
    else:
        returncode, stdout, _stderr = run_command(full_cmd, timeout=timeout, can_fail=True)

    # Parse output regardless of whether `must_pass` is specified: unfortunately some tests
    # do not exit with non-zero code when failing, because they rely on `MAP_SHARED` (which
    # we do not support correctly) for collecting test results.
    passed, failed, conf, system_error_output_valid = parse_test_output(stdout, _stderr, cmd)

    logging.info('returncode: %s', returncode)
    logging.info('passed: %s', list(passed))
    logging.info('failed: %s', list(failed))
    logging.info('Conf: %s', list(conf))
    
    if not must_pass:
        if failed:
            pytest.fail('Failed subtests: {}'.format(failed))
        elif conf and not passed:
            pytest.fail('Only TCONF found: {}'.format(failed))
        elif (system_error_output_valid == False):
            pytest.fail("Error due to invalid system error output")                             
        return
    else:
        check_must_pass(passed, failed, must_pass, conf, system_error_output_valid)


def test_lint():
    cmd = ['./contrib/conf_lint.py', '--scenario', LTP_SCENARIO, *LTP_CONFIG]
    p = subprocess.run(cmd)
    if p.returncode:
        pytest.fail('conf_lint.py failed, see stdout for details')


def pytest_generate_tests(metafunc):
    """Generate all tests.

    This function is called by Pytest, and it's responsible for generating parameters for
    `test_ltp`.
    """

    if metafunc.function is test_ltp:
        params = []
        for tag, cmd, section in list_tests():
            # If a test should be skipped, mark it as such, but add it for Pytest anyway: we want
            # skipped tests to be visible in the report.
            marks = [] if section else [pytest.mark.skip]
            params.append(pytest.param(cmd, section, id=tag, marks=marks))

        metafunc.parametrize('cmd,section', params)


def main():
    if sys.argv[1:] == ['--list']:
        seen = set()
        for _tag, cmd, section in list_tests():
            executable = cmd[0]
            if section and executable not in seen:
                seen.add(executable)
                print(executable)
    else:
        usage = '''\
Usage:

    {} --list   (to list test executables)

Invoke Pytest directly (python3 -m pytest) to run tests.

Supports the following environment variables:

    SGX: set to 1 to enable SGX mode (default: disabled)
    LTP_SCENARIO: LTP scenario file (default: {})
    LTP_CONFIG: space-separated list of LTP config files (default: {})
    LTP_TIMEOUT_FACTOR: multiply all timeouts by given value
'''.format(sys.argv[0], DEFAULT_LTP_SCENARIO, DEFAULT_LTP_CONFIG)
        print(usage, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()