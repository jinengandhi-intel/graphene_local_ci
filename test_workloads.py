#!/usr/bin/env python3
import sys
import logging
import glob
from os import path
import os


class Test_Workload_Results():
    def test_bash_workload(self):
        bash_result_file = open("CI-Examples/bash/OUTPUT", "r")
        bash_contents = bash_result_file.read()
        assert("readlink" in bash_contents)

    def test_python_workload(self):
        python_result_file = open("CI-Examples/python/TEST_STDOUT", "r")
        python_contents = python_result_file.read()
        assert("Success 1/4" in python_contents)
        assert("Success 2/4" in python_contents)
        assert("Success 3/4" in python_contents)
        assert("Success 4/4" in python_contents)

    def test_lightppd_workload(self):
        for filename in glob.glob("CI-Examples/lighttpd/result-*"):
            lightppd_result_file = open(filename,"r")
        lightppd_contents = lightppd_result_file.read()
        assert("0,0" in lightppd_contents)

    def test_nginx_workload(self):
        for filename in glob.glob("CI-Examples/nginx/result-*"):
            nginx_result_file = open(filename,"r")
        nginx_contents = nginx_result_file.read()
        assert("0,0" in nginx_contents)

    def test_blender(self):
        blender_result_file = "CI-Examples/blender/data/images/simple_scene.blend0001.png"
        assert(path.exists(blender_result_file))

    def test_redis(self):
        redis_result_file = open("CI-Examples/redis/OUTPUT", "r")
        redis_contents = redis_result_file.read()
        assert(("PING_INLINE" in redis_contents) and ("MSET" in redis_contents))

    def test_sqlite_workload(self):
        sqlite_result_file = open("CI-Examples/sqlite/OUTPUT", "r")
        sqlite_contents = sqlite_result_file.read()
        assert(("row 4" in sqlite_contents) \
                and ("row 3" in sqlite_contents) \
                and ("row 2" in sqlite_contents) \
                and ("row 1" in sqlite_contents))

