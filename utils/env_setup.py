import requests
import json
import time
import subprocess
import os
import base64

node_name = os.environ.get('NODE_NAME')

priviledge = "sudo -S"
if node_name == "graphene_icl_alpine":
    priviledge = "doas "

class ConnectionDetails:
    '''This is class contains parameter/data for setting time''' 

    intel_proxy = {
        'http': 'http://proxy-dmz.intel.com:911',
        "https": "http://proxy-dmz.intel.com:912"
    }
    
    timezone = 'Asia/Kolkata'
    base_url = 'https://timeapi.io/api/TimeZone/zone?timeZone=' 
    target_url = base_url + timezone


class TimeSyncCMD:
    '''This class has helper methods to set time/timezone'''
    def get_supported_time_format(self, response):
        json_object = json.loads(response.text)
        unformatted_time = json_object["currentLocalTime"]
        splitted_time = unformatted_time.split('.')
        splitted_time = splitted_time[0].replace('T', ' ')
        time_object = time.strptime(splitted_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = time.strftime("%d %b %Y %H:%M:%S", time_object)
        return time_stamp
    
    def execute_time_cmd(self, time_stamp):
        try:
            cmd = ' date --set "'+ str(time_stamp) + '"'
            subprocess.run(f"{priviledge} {cmd}", timeout=5, shell=True)
        except Exception as e:
            print('Failed to set the time' + e)


    def set_timezone_cmd(self, time_zone):
        if node_name == "graphene_icl_alpine":
            cmd = " setup-timezone -z "
        else:
            cmd = " timedatectl set-timezone "
        try:
            subprocess.run(f"{priviledge} {cmd} {time_zone}", timeout=5, shell=True)
        except Exception as e:
            print('Failed to set the timezone' + e)
   
    def sync_hw_clock(self):
        try:
            subprocess.run(f"{priviledge} hwclock --systohc", timeout=5, shell=True)
        except Exception as e:
            print('Failed to set hwclock' + e)

class HostSetup():
    def setup():
        try:
            subprocess.run(f"{priviledge} service docker restart", timeout=50, shell=True)
            subprocess.run("sleep 10s", shell=True)
            subprocess.run(f"{priviledge} chown $USER /var/run/docker.sock", timeout=5, shell=True)
            subprocess.run(f"{priviledge} chmod 777 /dev/cpu_dma_latency", timeout=5, shell=True)
            subprocess.run(f"{priviledge} chown $USER /dev/cpu_dma_latency", timeout=5, shell=True)
            subprocess.run(f"{priviledge} sysctl -w vm.max_map_count=1310720", timeout=10, shell=True)
            if (os.path.exists("/dev/sgx_enclave")):
                subprocess.run(f"{priviledge} chmod 777 /dev/sgx_enclave", timeout=5, shell=True)
                subprocess.run(f"{priviledge} chmod 777 /dev/sgx_provision", timeout=5, shell=True)
            print("System setup is done")
        except Exception as e:
            print('Failed to update host system setup' + e)


if __name__=='__main__':
    try:
        obj_conn = ConnectionDetails()
        response = requests.get(obj_conn.target_url, proxies=obj_conn.intel_proxy)
        obj_tsc = TimeSyncCMD()
        obj_tsc.set_timezone_cmd(obj_conn.timezone)
        time_stamp = obj_tsc.get_supported_time_format(response)
        obj_tsc.execute_time_cmd(time_stamp)
        obj_tsc.sync_hw_clock()
        print('Successfully updated system time!')
        HostSetup.setup()
    except Exception as e:
        print('Failed to update system time!' + e)
