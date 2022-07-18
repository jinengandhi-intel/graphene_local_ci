import glob

path = r'/home/intel/redis-6.0.6/log/set/25/'

all_files = glob.glob(path + "/*.csv")

avg_latency=0
avg_kbps=0
avg_latency_native = []
avg_kbps_native = []

avg_latency_graphene_direct = []
avg_kbps_graphene_direct = []

avg_latency_graphene_sgx = []
avg_kbps_graphene_sgx = []

for filename in all_files:
    with open(filename, "r") as f:
        print(filename)
        for row in f.readlines():
            row = row.split()
            if row:
                if "Totals" in row[0]:
                    avg_latency=row[5]
                    avg_kbps=row[-1]
        if "native" in filename:
            avg_latency_native.append(float(avg_latency))
            avg_kbps_native.append(float(avg_kbps))
        elif "graphene_sgx" in filename:
            avg_latency_graphene_sgx.append(float(avg_latency))
            avg_kbps_graphene_sgx.append(float(avg_kbps))
        else:
            avg_latency_graphene_direct.append(float(avg_latency))
            avg_kbps_graphene_direct.append(float(avg_kbps))


print("Average Latency Native: ",sum(avg_latency_native)/len(avg_latency_native))
print("Average Latency Graphene Direct: ",sum(avg_latency_graphene_direct)/len(avg_latency_graphene_direct))

print("Average Throughput Native: ",sum(avg_kbps_native)/len(avg_kbps_native))
print("Average Throughput Graphene Direct: ",sum(avg_kbps_graphene_direct)/len(avg_kbps_graphene_direct))

            


