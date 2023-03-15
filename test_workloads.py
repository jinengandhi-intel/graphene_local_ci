#!/usr/bin/env python3
import sys
import logging
import glob
from os import path
import os
import pytest
import re

sgx_mode = os.environ.get('SGX')
no_cores = os.environ.get('no_cpu')
os_version = os.environ.get('os_version')
os_release_id = os.environ.get('os_release_id')
node_label = os.environ.get('node_label')

class Test_Workload_Results():
    @pytest.mark.examples
    def test_bash_workload(self):
        bash_result_file = open("CI-Examples/bash/result.txt", "r")
        bash_contents = bash_result_file.read()
        assert("Success 1/7" in bash_contents)
        assert("Success 2/7" in bash_contents)
        assert("Success 3/7" in bash_contents)
        assert("Success 4/7" in bash_contents)
        assert("Success 5/7" in bash_contents)
        assert("Success 6/7" in bash_contents)
        assert("Success 7/7" in bash_contents)

    @pytest.mark.examples
    def test_python_workload(self):
        python_result_file = open("CI-Examples/python/TEST_STDOUT", "r")
        python_contents = python_result_file.read()
        assert("Success 1/4" in python_contents)
        assert("Success 2/4" in python_contents)
        assert("Success 3/4" in python_contents)
        assert("Success 4/4" in python_contents)
        if os.environ.get("RA_TYPE") == "dcap":
            assert("Success SGX report" in python_contents)
            assert("Success SGX quote" in python_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id != "ubuntu" or
                    float(os_version) >= 21),
                    reason="Memcached libraries not available for CENT/RHEL")
    def test_memcached_workload(self):
        memcached_result_file = open("CI-Examples/memcached/OUTPUT.txt", "r")
        memcached_contents = memcached_result_file.read()
        assert("2" in memcached_contents)
        
    @pytest.mark.examples
    def test_lightppd_workload(self):
        for filename in glob.glob("CI-Examples/lighttpd/result-*"):
            lightppd_result_file = open(filename,"r")
        lightppd_contents = lightppd_result_file.read()
        assert((re.search("Concurrency =(\s+)1: Per Thread Median Througput (.*)Latency(.*)", lightppd_contents)) \
            and (re.search("Concurrency =(\s+)32: Per Thread Median Througput (.*)Latency(.*)", lightppd_contents)))

    @pytest.mark.examples
    def test_nginx_workload(self):
        for filename in glob.glob("CI-Examples/nginx/result-*"):
            nginx_result_file = open(filename,"r")
        nginx_contents = nginx_result_file.read()
        assert((re.search("Concurrency =(\s+)1: Per Thread Median Througput (.*)Latency(.*)", nginx_contents)) \
            and (re.search("Concurrency =(\s+)32: Per Thread Median Througput (.*)Latency(.*)", nginx_contents)))

    @pytest.mark.examples
    def test_blender(self):
        blender_result_file = "CI-Examples/blender/data/images/simple_scene.blend0001.png"
        assert(path.exists(blender_result_file))

    @pytest.mark.examples
    def test_redis(self):
        redis_result_file = open("CI-Examples/redis/OUTPUT", "r")
        redis_contents = redis_result_file.read()
        assert(("PING_INLINE" in redis_contents) and ("MSET" in redis_contents))

    @pytest.mark.examples
    def test_sqlite_workload(self):
        sqlite_result_file = open("CI-Examples/sqlite/OUTPUT", "r")
        sqlite_contents = sqlite_result_file.read()
        assert(("row 4" in sqlite_contents) \
                and ("row 3" in sqlite_contents) \
                and ("row 2" in sqlite_contents) \
                and ("row 1" in sqlite_contents))
    
    @pytest.mark.examples
    def test_busybox_workload(self):
        busybox_result_file = open("CI-Examples/busybox/result.txt", "r")
        busybox_contents = busybox_result_file.read()
        assert("Success 1/1" in busybox_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((int(no_cores) < 16),
                    reason="Go_helloworld is enabled only on servers")
    def test_go_helloworld_workload(self):
        go_helloworld_result_file = open("CI-Examples/go_helloworld/OUTPUT", "r")
        go_helloworld_contents = go_helloworld_result_file.read()
        assert("Hello, world" in go_helloworld_contents)                
    
    @pytest.mark.sandstone
    @pytest.mark.skipif((int(no_cores) < 16 or sgx_mode != '1'),
                    reason="Sandstone is enabled on servers with SGX")
    def test_sandstone_workload(self):
        sandstone_result_file = open("CI-Examples/sandstone-50-bin/OUTPUT.txt", "r")
        sandstone_contents = sandstone_result_file.read()
        assert(("Loop iteration 1 finished" in sandstone_contents) and ("exit: pass" in sandstone_contents))

    @pytest.mark.examples
    def test_rust_workload(self):
        data = open("CI-Examples/rust/RESULT", "r")
        result_file = data.read().split("Result file: ")[1].strip()
        rust_result_file = open("CI-Examples/rust/{}".format(result_file), "r")
        rust_contents = rust_result_file.read()
        assert((re.search("Concurrency =(\s+)1: Per Thread Median Througput (.*)Latency(.*)", rust_contents)) \
            and (re.search("Concurrency =(\s+)32: Per Thread Median Througput (.*)Latency(.*)", rust_contents)))

    @pytest.mark.examples
    @pytest.mark.skipif(((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="OpenJDK enabled only for Ubuntu Server Configurations.")
    def test_openjdk_workload(self):
        jdk_result_file = open("CI-Examples/openjdk/OUTPUT", "r")
        jdk_contents = jdk_result_file.read()
        assert("Final Count is:" in jdk_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(float(os_version) >= 21 or
                ((node_label == 'graphene_18.04_5.19') and sgx_mode == '1') or
                (("dcap" in node_label) and sgx_mode == '1'),
                    reason="Bazel Build fails for Ubuntu 21 and Gramine DCAP")
    def test_tensorflow_workload(self):
        tensorflow_result_file = open("CI-Examples/tensorflow-lite/OUTPUT", "r")
        tensorflow_contents = tensorflow_result_file.read()
        assert((re.search("average time: \d+", tensorflow_contents)) \
            and (re.search("\d+: 653 military uniform", tensorflow_contents)) \
            and (re.search("\d+: 668 mortarboard", tensorflow_contents)) \
            and (re.search("\d+: 401 academic gown", tensorflow_contents)) \
            and (re.search("\d+: 835 suit", tensorflow_contents)) \
            and (re.search("\d+: 458 bow tie", tensorflow_contents)))

    @pytest.mark.examples
    def test_curl_workload(self):
        curl_result_file = open("CI-Examples/curl/RESULT", "r")
        curl_contents = curl_result_file.read()
        assert("Success 1/1" in curl_contents)

    @pytest.mark.examples
    def test_nodejs_workload(self):
        nodejs_result_file = open("CI-Examples/nodejs/RESULT", "r")
        nodejs_contents = nodejs_result_file.read()
        assert("Success 1/1" in nodejs_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(((node_label == 'graphene_18.04_5.19') and (sgx_mode == '1')),
                    reason="Pytorch fails for graphene_18.04_5.19")
    def test_pytorch_workload(self):
        pytorch_result_file = open("CI-Examples/pytorch/result.txt", "r")
        pytorch_contents = pytorch_result_file.read()
        assert(("Labrador retriever" in pytorch_contents) \
            and ("golden retriever" in pytorch_contents) \
            and ("Saluki, gazelle hound" in pytorch_contents) \
            and ("whippet" in pytorch_contents) \
            and ("Ibizan hound, Ibizan Podenco" in pytorch_contents))

    @pytest.mark.examples
    @pytest.mark.skipif(((node_label == 'graphene_18.04_5.19') and (sgx_mode == '1')),
                    reason="R fails for graphene_18.04_5.19")
    def test_r_workload(self):
        r1_result_file = open("CI-Examples/r/RESULT_1", "r")
        r1_contents = r1_result_file.read()
        assert("success" in r1_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id != "ubuntu") or
                    ((node_label == 'graphene_18.04_5.19') and (sgx_mode == '1')),
                    reason="GCC enabled only for Ubuntu configurations.")
    def test_gcc_workload(self):
        gcc_result_file = open("CI-Examples/gcc/OUTPUT", "r")
        gcc_contents = gcc_result_file.read()
        assert(("Hello world (./test_files/hello)!" in gcc_contents) \
            and ("diff -q test_files/bzip2 test_files/bzip2.copy" in gcc_contents) \
            and ("diff -q test_files/gzip test_files/gzip.copy" in gcc_contents))

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id == 'centos') or
                    (float(os_version) >= 21) or ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="Openvino enabled only for Ubuntu 18 & 20 Server Configurations")
    def test_openvino_workload(self):
        openvino_result_file = open("CI-Examples/openvino/OUTPUT", "r")
        openvino_contents = openvino_result_file.read()
        assert((re.search("Dumping statistics report", openvino_contents)) \
            and (re.search("Count:", openvino_contents)) \
            and (re.search("Duration:", openvino_contents)) \
            and (re.search("Latency:", openvino_contents)) \
            and (re.search("Throughput:", openvino_contents)))

    @pytest.mark.examples
    @pytest.mark.sanity
    @pytest.mark.skipif(not(("dcap" in node_label) and sgx_mode == "1"), reason="Enabled only for Gramine SGX Dcap")
    def test_ra_tls_mbedtls_workload(self):
        mbedtls_result_file = open("CI-Examples/ra-tls-mbedtls/mbedtls_result.txt", "r")
        mbedtls_contents = mbedtls_result_file.read()
        assert("Success 1/4" in mbedtls_contents)
        assert("Success 2/4" in mbedtls_contents)
        assert("Success 3/4" in mbedtls_contents)
        assert("Success 4/4" in mbedtls_contents)

    @pytest.mark.examples
    @pytest.mark.sanity
    @pytest.mark.skipif(not(("dcap" in node_label) and sgx_mode == "1"), reason="Enabled only for Gramine SGX Dcap")
    def test_ra_tls_secret_prov_workload(self):
        secret_prov_result_file = open("CI-Examples/ra-tls-secret-prov/secret_prov_result.txt", "r")
        secret_prov_contents = secret_prov_result_file.read()
        assert("Success 1/4" in secret_prov_contents)
        assert("Success 2/4" in secret_prov_contents)
        assert("Success 3/4" in secret_prov_contents)
        assert("Success 4/4" in secret_prov_contents)

    @pytest.mark.sanity
    def test_helloworld_workload(self):
        helloworld_result_file = open("CI-Examples/helloworld/helloworld_result.txt", "r")
        helloworld_contents = helloworld_result_file.read()
        assert("Hello, world" in helloworld_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id != 'ubuntu') or (float(os_version) <= 20) or ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="Scikit-learn enabled for Ubuntu Server Configurations.")
    def test_scikit_workload(self):
        sklearn_result_file = open("CI-Examples/scikit-learn-intelex/RESULT", "r")
        sklearn_contents = sklearn_result_file.read()
        assert(("Success 1/2" in sklearn_contents) \
            and ("Success 2/2" in sklearn_contents))

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id != 'ubuntu') or (float(os_version) <= 20) or
                    ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="TFServing enabled only for above Ubuntu 18.04 Configurations.")
    def test_tfserving_workload(self):
        tfserving_result = open("CI-Examples/tfserving/RESULT", "r")
        tfserving_contents = tfserving_result.read()
        assert("Success" in tfserving_contents)