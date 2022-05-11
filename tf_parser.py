import glob
import os
import pytest
import re
path_bert = os.environ.get('bert_dir')
path_resnet = os.environ.get('resnet_dir')
path = [path_bert , path_resnet]
print ("Path : ", path)

def result_aggregation(input_path):
    all_files = glob.glob(input_path + "/*.txt")
    native_result = []
    direct_result = []
    sgx_result = []
    for filename in all_files:
        with open(filename, "r") as f:
            for row in f.readlines():
                if row:
                    if "Throughput" in row or "Total throughput" in row:
                        throughput = re.findall('\d+\.\d+', row)
                        throughput = round(float(throughput[0]),2)
                    else:
                        continue
                    if "native" in filename:
                        native_result.append(float(throughput))
                    elif "gramine-direct" in filename:
                        direct_result.append(float(throughput))
                    elif "gramine-sgx" in filename:
                        sgx_result.append(float(throughput))
                    else:
                        print("Output file from config list not found.")
    
    print("\nNumber of iterations : ",len(sgx_result))
    if len(native_result) > 0:
        print("Throughput values in native run : ", native_result, 
            " and Average : ",round(sum(native_result)/len(native_result),2))
    if len(direct_result) > 0: 
        print("Throughput values in Gramine direct run : ", direct_result,
            " and Average : ", round(sum(direct_result)/len(direct_result),2))   
    if len(sgx_result) > 0:    
        print("Throughput values in Gramine SGX run : ", sgx_result,
            " and Average : ", round(sum(sgx_result)/len(sgx_result),2)) 
    if len(sgx_result) > 0 and len(native_result) > 0 and len(direct_result) > 0:
        avg_sgx_throughput = sum(sgx_result)/len(sgx_result)
        avg_native_throughput = sum(native_result)/len(native_result)
        avg_direct_throughput = sum(direct_result)/len(direct_result)
        print("Degradation Native/SGX : ", (avg_native_throughput/avg_sgx_throughput))
        print("Degradation Native/Direct : ", (avg_native_throughput/avg_direct_throughput))
        print("Degradation Direct/SGX : ", (avg_direct_throughput/avg_sgx_throughput)) 

    return native_result, direct_result, sgx_result

class Test_TF_Results():
    @pytest.mark.skipif(path_bert is None,
                    reason="BERT example not executed")    
    def test_bert_workload(self):
        native_result, direct_result, sgx_result = result_aggregation(path_bert)            
        assert(len(native_result) is not None or len(sgx_result) is not None)

    @pytest.mark.skipif(path_resnet is None,
                    reason="RESNET example not executed")    
    def test_resnet_workload(self):
        native_result, direct_result, sgx_result = result_aggregation(path_resnet)
        assert(len(native_result) is not None or len(sgx_result) is not None)
    