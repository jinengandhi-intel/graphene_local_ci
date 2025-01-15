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
    @pytest.mark.skipif((os_release_id not in ["ubuntu", "debian"]),
                    reason="MySQL enabled only for above Ubuntu and debian Configurations.")
    def test_mysql_workload(self):
        mysql_result = open("CI-Examples/mysql/OUTPUT", "r")
        mysql_contents = mysql_result.read()
        assert("root@localhost is created with an empty password !" in mysql_contents)
        assert("error: " not in mysql_contents)
        mysql_result = open("CI-Examples/mysql/CREATE_RESULT", "r")
        mysql_contents = mysql_result.read()
        assert("Creating table 'sbtest2'..." in mysql_contents)
        assert("Creating table 'sbtest1'..." in mysql_contents)
        assert("Inserting 100000 records into 'sbtest2'" in mysql_contents)
        assert("Inserting 100000 records into 'sbtest1'" in mysql_contents)
        assert("error: " not in mysql_contents)
        mysql_result = open("CI-Examples/mysql/RUN_RESULT", "r")
        mysql_contents = mysql_result.read()
        assert("Threads fairness: " in mysql_contents)
        assert("error: " not in mysql_contents)
        mysql_result = open("CI-Examples/mysql/DELETE_RESULT", "r")
        mysql_contents = mysql_result.read()
        assert("Dropping table 'sbtest1'..." in mysql_contents)
        assert("Dropping table 'sbtest2'..." in mysql_contents)
        assert("error: " not in mysql_contents)
