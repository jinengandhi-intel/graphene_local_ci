import glob
import os
import pytest
path_bert = os.environ.get('bert_dir')
path_resnet = os.environ.get('resnet_dir')
path = [path_bert , path_resnet]
print ("Path : ", path)

def result_aggregation(input_path):
    all_files = glob.glob(input_path + "/*.txt")
    avg_throughput_native = []
    avg_throughput_gramine_direct = []
    avg_throughput_gramine_sgx = []
    for filename in all_files:
        with open(filename, "r") as f:
            for row in f.readlines():
                row = row.split()
                if row:
                    if "Throughput" in row[0]:
                        throughput = row[1]
                    else:
                        continue
                    if "native" in filename:
                        avg_throughput_native.append(float(throughput))
                    elif "gramine-direct" in filename:
                        avg_throughput_gramine_direct.append(float(throughput))
                    elif "gramine-sgx" in filename:
                        avg_throughput_gramine_sgx.append(float(throughput))
                    else:
                        print("Output file from config list not found.")
    
    return avg_throughput_native, avg_throughput_gramine_direct, avg_throughput_gramine_sgx

class Test_TF_Results():
    @pytest.mark.skipif(path_bert is None,
                    reason="BERT example not executed")    
    def test_bert_workload(self):
        native_result, direct_result, sgx_result = result_aggregation(path_bert)
        print("\nNumber of iterations for BERT workload : ",len(sgx_result))
        if len(native_result) > 0:
            print("Throughput values in native run : ", native_result)
            print("Average Throughput Native: ",sum(native_result)/len(native_result))
        if len(direct_result) > 0: 
            print("Throughput values in Gramine direct run : ", direct_result)   
            print("Average Throughput Gramine direct: ",sum(direct_result)/len(direct_result))
        if len(sgx_result) > 0:    
            print("Throughput values in Gramine SGX run : ", sgx_result) 
            print("Average Throughput Gramine SGX: ",sum(sgx_result)/len(sgx_result))
        if len(sgx_result) > 0 and len(native_result) > 0 and len(direct_result) > 0:
            avg_sgx_throughput = sum(sgx_result)/len(sgx_result)
            avg_native_throughput = sum(native_result)/len(native_result)
            avg_direct_throughput = sum(direct_result)/len(direct_result)
            print("Degradation Native/SGX : ", (avg_native_throughput/avg_sgx_throughput))
            print("Degradation Native/Direct : ", (avg_native_throughput/avg_direct_throughput))
            print("Degradation Direct/SGX : ", (avg_direct_throughput/avg_sgx_throughput))        
        assert(len(native_result) is not None or len(sgx_result) is not None)

    @pytest.mark.skipif(path_resnet is None,
                    reason="RESNET example not executed")    
    def test_resnet_workload(self):
        native_result, direct_result, sgx_result = result_aggregation(path_resnet)
        print("\nNumber of iterations for RESNET workload : ",len(sgx_result))
        if len(native_result) > 0:
            print("Throughput values in native run : ", native_result)
            print("Average Throughput Native: ",sum(native_result)/len(native_result))
        if len(direct_result) > 0: 
            print("Throughput values in Gramine direct run : ", direct_result)   
            print("Average Throughput Gramine direct: ",sum(direct_result)/len(direct_result))
        if len(sgx_result) > 0:    
            print("Throughput values in Gramine SGX run : ", sgx_result) 
            print("Average Throughput Gramine SGX: ",sum(sgx_result)/len(sgx_result))
        if len(sgx_result) > 0 and len(native_result) > 0 and len(direct_result) > 0:
            avg_sgx_throughput = sum(sgx_result)/len(sgx_result)
            avg_native_throughput = sum(native_result)/len(native_result)
            avg_direct_throughput = sum(direct_result)/len(direct_result)
            print("Degradation Native/SGX : ", (avg_native_throughput/avg_sgx_throughput))
            print("Degradation Native/Direct : ", (avg_native_throughput/avg_direct_throughput))
            print("Degradation Direct/SGX : ", (avg_direct_throughput/avg_sgx_throughput))
        assert(len(native_result) is not None or len(sgx_result) is not None)
    