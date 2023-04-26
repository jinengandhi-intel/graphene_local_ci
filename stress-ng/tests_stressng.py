import argparse
import os
import glob
import sys
from itertools import islice
from collections import defaultdict
import pytest

total_test_list={"hdd.log":15, "seek.log":7, "seek-hdd.log":4, "interrupt.log":6, \
            "filesystem.log":12, "filesystem_all.log":12, "scheduler.log":8, \
            "scheduler_all.log":9}

def parse_test_logs(log_file):
    test_results = defaultdict(list)
    fd = open(log_file)

    f_contents = fd.read()
    filename = os.path.basename(log_file)
    if "successful run completed" in f_contents and "error" not in f_contents:
        test_results["Pass"].append([i+1 for i in range(total_test_list.get(filename))])
    else:
        sub_tests = f_contents.split("starting stressors")
        sub_tests.pop(0) # Removing the content before the first test starts
        test_number = 0
        for tests in sub_tests:
            test_number += 1
            if "error" in tests:
                test_results["Fail"].append(test_number)
    
        for i in range(total_test_list.get(filename)):
            if (i+1) not in test_results["Fail"]:
                test_results["Pass"].append(i+1)
                       
    fd.close()
    print(test_results)
    return test_results

class Test_StressNG_Results():
    
    def test_stress_ng_hdd(self):
        test_results = parse_test_logs("hdd.log")
        assert(len(test_results["Fail"]) == 0)
    
    def test_stress_ng_seek(self):
        test_results = parse_test_logs("seek.log")
        assert(len(test_results["Fail"]) == 0)
    
    def test_stress_ng_seek_hdd(self):
        test_results = parse_test_logs("seek-hdd.log")
        assert(len(test_results["Fail"]) == 0)
    
    def test_stress_ng_interrupt(self):
        test_results = parse_test_logs("interrupt.log")
        assert(len(test_results["Fail"]) == 0)
    
    def test_stress_ng_filesystem(self):
        test_results = parse_test_logs("filesystem.log")
        assert(len(test_results["Fail"]) == 0)
    
    def test_stress_ng_filesystem_all(self):
        test_results = parse_test_logs("filesystem_all.log")
        assert(len(test_results["Fail"]) == 0)
    
    def test_stress_ng_scheduler(self):
        test_results = parse_test_logs("scheduler.log")
        assert(len(test_results["Fail"]) == 0)
