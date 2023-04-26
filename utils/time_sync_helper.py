import requests
import json
import time
import subprocess
import re
import os
import base64

class ConnectionDetails:
    '''This is class contains parameter/data for setting time'''

    def read_timezone():
        out = subprocess.Popen(['timedatectl'], \
                stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT)
        stout, sterr = out.communicate()
        machine_time_zone = re.findall(r'Time zone:\s(\w+\/\w+)', stout.decode())
        if len(machine_time_zone) > 0:
            return machine_time_zone[0]   
        return 'Asia/Kolkata'
    
    def string_maker(word):
        byt = word.encode("ascii")
        ssb = base64.b64decode(byt)
        return ssb.decode("ascii")

    
    intel_proxy = {
        'http': 'http://proxy-dmz.intel.com:911',
        "https": "http://proxy-dmz.intel.com:912"
    }

    os_release_id = os.environ.get('os_release_id')

    passphrase = string_maker('aW50ZWxAMTIz')
    if os_release_id in ['rockylinux']:
        passphrase = 'aW50ZWw='
    
    timezone = read_timezone()
    base_url = 'https://timeapi.io/api/TimeZone/zone?timeZone=' 
    target_url = base_url + timezone


class TimeSyncCMD:
    def get_supported_time_format(self, response):
        json_object = json.loads(response.text)
        unformatted_time = json_object["currentLocalTime"]
        splitted_time = unformatted_time.split('.')
        splitted_time = splitted_time[0].replace('T', ' ')
        time_object = time.strptime(splitted_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = time.strftime("%d %b %Y %H:%M:%S", time_object)
        return time_stamp
    
    def execute_time_cmd(self, time_stamp, passphrase):
        cmd = 'sudo date --set "'+ str(time_stamp) + '"'
        subprocess.call('echo {} | sudo -S {}'.format(passphrase, cmd), shell=True)

    def sync_hw_clock(self, passphase):
        cmd = 'sudo hwclock --systohc'
        subprocess.call('echo {} | sudo -S {}'.format(passphase, cmd), shell=True)
    

if __name__=='__main__':
    try:
        obj_conn = ConnectionDetails()
        response = requests.get(obj_conn.target_url, proxies=obj_conn.intel_proxy)

        obj_tsc = TimeSyncCMD()

        time_stamp = obj_tsc.get_supported_time_format(response)
        obj_tsc.execute_time_cmd(time_stamp, obj_conn.passphrase)
        obj_tsc.sync_hw_clock(obj_conn.passphrase)
        print('Successfully updated system time!')
    except Exception as e:
        print('Failed to update system time!' + e)
