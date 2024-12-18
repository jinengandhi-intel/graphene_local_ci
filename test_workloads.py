#!/usr/bin/env python3
import sys
import logging
import glob
from os import path
import os
import pytest
import re

sgx_mode = os.environ.get('SGX')
no_cores = os.environ.get('no_cpu', '8')
os_version = os.environ.get('os_version')
base_os = os.environ.get('base_os')
os_release_id = os.environ.get('os_release_id')
node_label = os.environ.get('node_label')
edmm_mode = os.environ.get('EDMM')
distro_ver = os.environ.get('distro_ver')
ra_type = os.environ.get("RA_TYPE", "none")

class Test_Workload_Results():
    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id not in ["ubuntu", "debian"]) or
                    ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="MySQL enabled only for above Ubuntu and debian Configurations.")
    def test_mysql_workload(self):
        mysql_result = open("CI-Examples/mysql/RESULT", "r")
        mysql_contents = mysql_result.read()
        assert("Success 1/2" in mysql_contents)
        assert("Success 2/2" in mysql_contents)
        assert("error: " not in mysql_contents)
