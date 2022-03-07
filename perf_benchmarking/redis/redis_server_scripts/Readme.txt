Please redis_server_scripts.zip in your ICX server system and unzip it.

*** Few prerequisites ***
# SGX must be enabled in the server system
# Gramine must be built and working
# numactl must be installed
# 10G P2P connection must be established between ICX server and ICL client system

# Please modify REDIS_PATH and SCRIPTS_PATH variables in redis_launch.py file based on your system paths.


*** Command to start the redis server:
python3 ./redis_launch.py -f run_redis -c native

*** Command to kill the redis server:
python3 ./redis_launch.py -f kill_redis -c native

## Main file: redis_launch.py

## Once the redis-server is ready to accept the connections, user can start the client scripts from the client system.

## Please modify the core values (-C 1,77) in the line 
cmd=f" numactl -C 1,77 gramine-sgx " + redis_cmd  , inside redis_launch.py file,
based on your server likwid-topology if user wish to run graphene_sgx_same_core configuration.



