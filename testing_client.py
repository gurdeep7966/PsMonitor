import socket
import json
import os
import subprocess
import psutil
import time
import threading
from queue import Queue
import wmi
from datetime import datetime, timedelta
import pythoncom
import pickle

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
HEADERSIZE = 10

system_data = {"HostName": "null", "UpTime": "null", "CPU": "null"}


def host_name():
    #pythoncom.CoInitialize()
    while True:
        host_name = socket.gethostname()
        system_data["HostName"] = host_name
        cpu_utilization = psutil.cpu_percent(interval=5)
        system_data["CPU"] = cpu_utilization
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for os in c.Win32_OperatingSystem():
            time = os.LastBootUpTime.split('.')[0]
            last_boot_time = datetime.strptime(time, '%Y%m%d%I%M%S')
            #now = datetime.now()
            #uptime = now - last_boot_time
            system_data["UpTime"] = str(last_boot_time)


def run_command():
    s = socket.socket();
    host = '10.42.62.156'
    port = 9999
    s.connect((host, port))
    while True:
        time.sleep(5)
        data=pickle.dumps(system_data)
        data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8')+data
        print(data)
        s.send(data)
    s.close()

def create_worker():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next Job in Queue (1 to handle connection 2 to send commands)

def work():
    while True:
        x = queue.get()
        if x == 1:
            host_name()
            time.sleep(5)

        if x == 2:
            run_command()
        queue.task_done()


# Each list item is a new JOB

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_worker()
create_jobs()


