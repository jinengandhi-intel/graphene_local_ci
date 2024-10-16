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
    def test_bash_workload(self):
        bash_result_file = open("CI-Examples/bash/result.txt", "r")
        bash_contents = bash_result_file.read()
        assert("Success 1/7" in bash_contents)
        assert("Success 2/7" in bash_contents)
        assert("Success 3/7" in bash_contents)
        assert("Success 4/7" in bash_contents)
        assert("Success 5/7" in bash_contents)
        assert("Success 6/7" in bash_contents)
        assert("error: " not in bash_contents)
        if (os_release_id != "alpine"):
            assert("Success 7/7" in bash_contents)

    @pytest.mark.examples
    def test_python_workload(self):
        python_result_file = open("CI-Examples/python/TEST_STDOUT", "r")
        python_contents = python_result_file.read()
        assert("Success 1/4" in python_contents)
        assert("Success 2/4" in python_contents)
        assert("Success 3/4" in python_contents)
        assert("Success 4/4" in python_contents)
        assert("error: " not in python_contents)
        if ra_type == "dcap":
            assert("Success SGX report" in python_contents)
            assert("Success SGX quote" in python_contents)

    @pytest.mark.examples
    def test_memcached_workload(self):
        memcached_result_file = open("CI-Examples/memcached/OUTPUT.txt", "r")
        memcached_contents = memcached_result_file.read()
        expected_output = ["2", "18"]
        assert(any(n in memcached_contents for n in expected_output))
        assert("error: " not in memcached_contents)
        
    @pytest.mark.examples
    def test_lighttpd_workload(self):
        for filename in glob.glob("CI-Examples/lighttpd/result-*"):
            lightppd_result_file = open(filename,"r")
        lightppd_contents = lightppd_result_file.read()
        assert((re.search("Concurrency =(\s+)1: Per Thread Median Througput (.*)Latency(.*)", lightppd_contents)) \
            and (re.search("Concurrency =(\s+)32: Per Thread Median Througput (.*)Latency(.*)", lightppd_contents)))
        assert("error: " not in lightppd_contents)

    @pytest.mark.examples
    def test_nginx_workload(self):
        for filename in glob.glob("CI-Examples/nginx/result-*"):
            nginx_result_file = open(filename,"r")
        nginx_contents = nginx_result_file.read()
        assert((re.search("Concurrency =(\s+)1: Per Thread Median Througput (.*)Latency(.*)", nginx_contents)) \
            and (re.search("Concurrency =(\s+)32: Per Thread Median Througput (.*)Latency(.*)", nginx_contents)))
        assert("error: " not in nginx_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(os_release_id == "alpine", reason='Blender is not enabled for Alpine')
    def test_blender(self):
        blender_result_file = "CI-Examples/blender/data/images/simple_scene.blend0001.png"
        assert(path.exists(blender_result_file))

    @pytest.mark.examples
    def test_redis(self):
        redis_result_file = open("CI-Examples/redis/OUTPUT", "r")
        redis_contents = redis_result_file.read()
        assert(("PING_INLINE" in redis_contents) and ("MSET" in redis_contents))
        assert("error: " not in redis_contents)

    @pytest.mark.examples
    def test_sqlite_workload(self):
        sqlite_result_file = open("CI-Examples/sqlite/OUTPUT", "r")
        sqlite_contents = sqlite_result_file.read()
        assert(("row 4" in sqlite_contents) \
                and ("row 3" in sqlite_contents) \
                and ("row 2" in sqlite_contents) \
                and ("row 1" in sqlite_contents))
        assert("error: " not in sqlite_contents)
    
    @pytest.mark.examples
    def test_busybox_workload(self):
        busybox_result_file = open("CI-Examples/busybox/result.txt", "r")
        busybox_contents = busybox_result_file.read()
        assert("Success 1/1" in busybox_contents)
        assert("error: " not in busybox_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="Go_helloworld is enabled only on servers")
    def test_go_helloworld_workload(self):
        go_helloworld_result_file = open("CI-Examples/go-helloworld/OUTPUT", "r")
        go_helloworld_contents = go_helloworld_result_file.read()
        assert("Hello, world" in go_helloworld_contents)
        assert("error: " not in go_helloworld_contents)
    
    @pytest.mark.sdtest
    @pytest.mark.skipif((int(no_cores) < 16 or sgx_mode != '1'),
                    reason="Sandstone is enabled on servers with SGX")
    def test_sdtest_workload(self):
        sdtest_result_file = open("CI-Examples/sd-test/OUTPUT.txt", "r")
        sdtest_contents = sdtest_result_file.read()
        assert(("Loop iteration 1 finished" in sdtest_contents) and ("exit: pass" in sdtest_contents))
        if edmm_mode != '1':
            sdtest_result_file_32gb = open("CI-Examples/sd-test/OUTPUT_32GB.txt", "r")
            sdtest_contents_32gb = sdtest_result_file_32gb.read()
            assert(("Loop iteration 1 finished" in sdtest_contents_32gb) and ("exit: pass" in sdtest_contents_32gb))

    @pytest.mark.examples
    def test_rust_workload(self):
        data = open("CI-Examples/rust/RESULT", "r")
        result_file = data.read().split("Result file: ")[1].strip()
        rust_result_file = open("CI-Examples/rust/{}".format(result_file), "r")
        rust_contents = rust_result_file.read()
        assert((re.search("Concurrency =(\s+)1: Per Thread Median Througput (.*)Latency(.*)", rust_contents)) \
            and (re.search("Concurrency =(\s+)32: Per Thread Median Througput (.*)Latency(.*)", rust_contents)))
        assert("error: " not in rust_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="OpenJDK enabled only for Ubuntu Server Configurations.")
    def test_openjdk_workload(self):
        jdk_result_file = open("CI-Examples/openjdk/OUTPUT", "r")
        jdk_contents = jdk_result_file.read()
        assert("Final Count is:" in jdk_contents)
        assert("error: " not in jdk_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((base_os not in ["ubuntu20.04"]) \
                or (("dcap" in node_label) and sgx_mode == '1'), \
                    reason="Bazel Build fails for Ubuntu 21 and Gramine DCAP")
    def test_tensorflow_lite_workload(self):
        tensorflow_result_file = open("CI-Examples/tensorflow-lite/OUTPUT", "r")
        tensorflow_contents = tensorflow_result_file.read()
        assert((re.search("average time: \d+", tensorflow_contents)) \
            and (re.search("\d+: 653 military uniform", tensorflow_contents)) \
            and (re.search("\d+: 668 mortarboard", tensorflow_contents)) \
            and (re.search("\d+: 401 academic gown", tensorflow_contents)) \
            and (re.search("\d+: 835 suit", tensorflow_contents)) \
            and (re.search("\d+: 458 bow tie", tensorflow_contents)))
        assert("error: " not in tensorflow_contents)

    @pytest.mark.examples
    def test_curl_workload(self):
        curl_result_file = open("CI-Examples/curl/RESULT", "r")
        curl_contents = curl_result_file.read()
        assert("Success 1/1" in curl_contents)
        assert("error: " not in curl_contents)

    @pytest.mark.examples
    def test_nodejs_workload(self):
        nodejs_result_file = open("CI-Examples/nodejs/RESULT", "r")
        nodejs_contents = nodejs_result_file.read()
        assert("Success 1/1" in nodejs_contents)
        assert("error: " not in nodejs_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(((base_os in ["ubuntu24.04", "alpine3.18"]) or (node_label == "graphene_22.04_5.19")),
                    reason="Pytorch not compatible for musl.")
    def test_pytorch_workload(self):
        pytorch_result_file = open("CI-Examples/pytorch/result.txt", "r")
        pytorch_contents = pytorch_result_file.read()
        assert(("Labrador retriever" in pytorch_contents) \
            and ("golden retriever" in pytorch_contents) \
            and ("Saluki, gazelle hound" in pytorch_contents) \
            and ("whippet" in pytorch_contents) \
            and ("Ibizan hound, Ibizan Podenco" in pytorch_contents))
        assert("error: " not in pytorch_contents)

    @pytest.mark.examples
    def test_r_workload(self):
        r1_result_file = open("CI-Examples/r/RESULT_1", "r")
        r1_contents = r1_result_file.read()
        assert("success" in r1_contents)
        assert("error: " not in r1_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id not in ["ubuntu", "debian", "alpine"]),
                    reason="GCC not enabled for RPM configurations.")
    def test_gcc_workload(self):
        gcc_result_file = open("CI-Examples/gcc/OUTPUT", "r")
        gcc_contents = gcc_result_file.read()
        assert(("Hello world (./test_files/hello)!" in gcc_contents) \
            and ("diff -q test_files/bzip2 test_files/bzip2.copy" in gcc_contents) \
            and ("diff -q test_files/gzip test_files/gzip.copy" in gcc_contents))
        assert("error: " not in gcc_contents)

    @pytest.mark.examples
    @pytest.mark.skipif(not(base_os in ["ubuntu20.04"])
                     or ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="Openvino enabled only for Ubuntu 20 Server Configurations")
    def test_openvino_workload(self):
        openvino_result_file = open("CI-Examples/openvino/OUTPUT", "r")
        openvino_contents = openvino_result_file.read()
        assert((re.search("Dumping statistics report", openvino_contents)) \
            and (re.search("Count:", openvino_contents)) \
            and (re.search("Duration:", openvino_contents)) \
            and (re.search("Latency:", openvino_contents)) \
            and (re.search("Throughput:", openvino_contents)))
        assert("error: " not in openvino_contents)

    @pytest.mark.examples
    @pytest.mark.sanity
    @pytest.mark.skipif(not((ra_type == "dcap") and sgx_mode == "1"), reason="Enabled only for Gramine SGX Dcap")
    def test_ra_tls_mbedtls_workload(self):
        mbedtls_result_file = open("CI-Examples/ra-tls-mbedtls/mbedtls_result.txt", "r")
        mbedtls_contents = mbedtls_result_file.read()
        assert("Success 1/4" in mbedtls_contents)
        assert("Success 2/4" in mbedtls_contents)
        assert("Success 3/4" in mbedtls_contents)
        assert("Success 4/4" in mbedtls_contents)
        assert("error: " not in mbedtls_contents)

    @pytest.mark.examples
    @pytest.mark.sanity
    @pytest.mark.skipif(not((ra_type == "dcap") and sgx_mode == "1"), reason="Enabled only for Gramine SGX Dcap")
    def test_ra_tls_secret_prov_workload(self):
        secret_prov_result_file = open("CI-Examples/ra-tls-secret-prov/secret_prov_result.txt", "r")
        secret_prov_contents = secret_prov_result_file.read()
        assert("Success 1/4" in secret_prov_contents)
        assert("Success 2/4" in secret_prov_contents)
        assert("Success 3/4" in secret_prov_contents)
        assert("Success 4/4" in secret_prov_contents)
        assert("error: " not in secret_prov_contents)

    @pytest.mark.examples
    @pytest.mark.sanity
    @pytest.mark.skipif(not((ra_type == "dcap") and sgx_mode == "1"), reason="Enabled only for Gramine SGX Dcap")
    def test_ra_tls_nginx_workload(self):
        nginx_result_file = open("CI-Examples/ra-tls-nginx/nginx_result.txt", "r")
        nginx_contents = nginx_result_file.read()
        assert("OK" in nginx_contents)
        assert("error: " not in nginx_contents)

    @pytest.mark.sanity
    def test_helloworld_workload(self):
        helloworld_result_file = open("CI-Examples/helloworld/helloworld_result.txt", "r")
        helloworld_contents = helloworld_result_file.read()
        assert("Hello, world" in helloworld_contents)
        assert("error: " not in helloworld_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((base_os not in ["ubuntu20.04", "ubuntu22.04"])
            or ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="Scikit-learn enabled for Ubuntu & Debian 11 Server Configurations.")
    def test_scikit_learn_intelex_workload(self):
        sklearn_result_file = open("CI-Examples/scikit-learn-intelex/RESULT", "r")
        sklearn_contents = sklearn_result_file.read()
        assert(("Success 1/2" in sklearn_contents) \
            and ("Success 2/2" in sklearn_contents))
        assert("error: " not in sklearn_contents)

    @pytest.mark.examples
    @pytest.mark.skipif((os_release_id not in ["ubuntu", "debian"]) or
                    ((int(no_cores) < 16) and sgx_mode == '1'),
                    reason="TFServing enabled only for above Ubuntu and debian Configurations.")
    def test_tfserving_workload(self):
        tfserving_result = open("CI-Examples/tfserving/RESULT", "r")
        tfserving_contents = tfserving_result.read()
        assert("Success" in tfserving_contents)
        assert("error: " not in tfserving_contents)

    @pytest.mark.gsc
    def test_gsc_bash_workload(self):
        gsc_bash_result = open("bash_result", "r")
        gsc_bash_log = gsc_bash_result.read()
        if (os_release_id == "debian") or ("redhat" in os_release_id) or (os_release_id == "quay.io/centos/centos"):
            assert(re.search('boot(.*)home(.*)proc', gsc_bash_log, re.DOTALL))
        else:
            assert(re.search('Mem:(.*)Swap:', gsc_bash_log, re.DOTALL))
        assert("error: " not in gsc_bash_log)

    @pytest.mark.gsc
    def test_gsc_python_workload(self):
        gsc_python_result = open("python_result", "r")
        gsc_python_log = gsc_python_result.read()
        assert("HelloWorld!" in gsc_python_log)
        assert("error: " not in gsc_python_log)

    @pytest.mark.gsc
    def test_gsc_helloworld_workload(self):
        gsc_helloworld_result = open("helloworld_result", "r")
        gsc_helloworld_log = gsc_helloworld_result.read()
        assert('"Hello World! Let\'s check escaped symbols: < & > "' in gsc_helloworld_log)
        assert("error: " not in gsc_helloworld_log)

    @pytest.mark.gsc
    @pytest.mark.skipif(distro_ver != "debian:11", reason='java-simple is enabled only on debian11 currently')
    def test_gsc_java_simple_workload(self):
        gsc_java_simple_result = open("openjdk-simple_result", "r")
        gsc_java_simple_log = gsc_java_simple_result.read()
        assert("Hello from Graminized Java application!" in gsc_java_simple_log)
        assert("error: " not in gsc_java_simple_log)
    
    @pytest.mark.gsc
    @pytest.mark.skipif(distro_ver != "debian:11", reason='java-spring-boot is enabled only on debian11 currently')
    def test_gsc_java_spring_boot_workload(self):
        gsc_java_springboot_result = open("openjdk-spring-boot_result", "r")
        gsc_java_springboot_log = gsc_java_springboot_result.read()
        assert("Hello from Graminized Spring Boot Application." in gsc_java_springboot_log)
        assert("error: " not in gsc_java_springboot_log)

    @pytest.mark.examples
    @pytest.mark.skipif(((base_os in ["ubuntu24.04", "alpine3.18"]) or ((int(no_cores) < 16) and sgx_mode == '1')),
                    reason="MongoDB not enabled for alpine distribution")
    def test_mongodb_workload(self):
        mongodb_result = open("CI-Examples/mongodb/OUTPUT", "r")
        mongodb_contents = mongodb_result.read()
        assert(("item: 'card'" in mongodb_contents) and \
               ("item: 'pen'" in mongodb_contents) and \
               ("item: 'lamp'" in mongodb_contents))
        assert("error: " not in mongodb_contents)

    @pytest.mark.gsc
    def test_gsc_gramine_build_bash_workload(self):
        gsc_bash_result = open("gramine_build_bash_result", "r")
        gsc_bash_log = gsc_bash_result.read()
        if (os_release_id == "debian") or ("redhat" in os_release_id) or (os_release_id == "quay.io/centos/centos"):
            assert(re.search('boot(.*)home(.*)proc', gsc_bash_log, re.DOTALL))
        else:
            assert(re.search('Mem:(.*)Swap:', gsc_bash_log, re.DOTALL))
        assert("error: " not in gsc_bash_log)

    @pytest.mark.examples
    def test_iperf_workload(self):
        iperf_result = open("CI-Examples/iperf/OUTPUT", "r")
        iperf_contents = iperf_result.read()
        assert(re.search("connected to (.*) port 5201", iperf_contents) and \
               ("iperf Done" in iperf_contents))
        assert("error: " not in iperf_contents)
