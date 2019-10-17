
from socket import *
import asyncio
import time
import pickle
import psutil
import pythoncom
import wmi
from datetime import datetime, timedelta


async def echo_client(address,loop):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.setblocking(False)
    except ConnectionRefusedError:
        print('retryinig to connect')
        connected = False
        while not connected:
            try:
                sock.connect(address)
                sock.setblocking(False)
                connected=True

            except ConnectionRefusedError:
                time.sleep(2)



    while True:

        system_data=get_data()
        data=pickle.dumps(system_data)
        #data=pickle.dumps(system_data)
        try:

            await loop.sock_sendall(sock,data)
            #data = await loop.sock_recv(sock, 1024)
        except ConnectionResetError:
            connected=False
            sock = socket(AF_INET, SOCK_STREAM)
            while not connected:
                try:
                    print('connection lost Retrying to send data')
                    sock.connect(address)
                    sock.setblocking(False)
                    await loop.sock_sendall(sock, data)
                    #data = await loop.sock_recv(sock, 1024)
                    connected=True
                except ConnectionRefusedError:
                    time.sleep(5)


        #data=data.decode()
        #if not data:
        #    break
        # client.sendall(b'Got :'+data)
        #print('recived data is ' + data)
    sock.close()

def get_data():
    system_data = {"HostName": "null", "UpTime": "null", "CPU": "null"}
    host_name = gethostname()
    system_data["HostName"] = host_name
    cpu_utilization = psutil.cpu_percent(interval=5)
    system_data["CPU"] = cpu_utilization
    pythoncom.CoInitialize()
    c = wmi.WMI()
    for os in c.Win32_OperatingSystem():
        time = os.LastBootUpTime.split('.')[0]
        last_boot_time = datetime.strptime(time, '%Y%m%d%I%M%S')
        # now = datetime.now()
        # uptime = now - last_boot_time
        system_data["UpTime"] = str(last_boot_time)

    return system_data

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(echo_client(('10.42.62.156', 25000),loop))

