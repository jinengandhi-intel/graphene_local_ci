import os
import pytest
from libs import utils
from libs import gramine_fuzzing_libs
from common.config.constants import *

@pytest.mark.usefixtures("gramine_setup")
class TestClass:
    @pytest.mark.parametrize("filesize", [0, 1, 2, 15, 16, 17, 255, 256, 257, 1023, 1024, 1025, 65535, 65536, 65537,
                         1048575, 1048576, 1048577])
    def test_fuzzing_with_different_filesize(self, filesize):
        testname = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        iterations = int(os.environ.get('iterations', '5'))
        timeout = int(os.environ.get('timeout', '120'))
        output = gramine_fuzzing_libs.run_libfuzzer(filesize, testname, iterations, timeout)
        if not output:
            print("Libfuzzer execution failure!!!")
            assert False
            return
        gramine_fuzzing_libs.verify_libfuzzer(testname)
        
    def test_fuzzing_with_corrupt_file(self):
        filesize = 1024
        testname = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        output = gramine_fuzzing_libs.run_libfuzzer_corrupt(filesize, testname)
        print('output of the libfuzzer with corrupted file ' + str(output))
        assert output

    def test_fuzzing_with_wrong_insecure_key(self):
        filesize = 1024
        insecure_key_value = '"F558C"'
        testname = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        output = gramine_fuzzing_libs.run_libfuzzer_wrong_insecure_key(filesize, testname, insecure_key_value)
        print('output of the libfuzzer with wrong insecure key ' + str(output))
        assert output

