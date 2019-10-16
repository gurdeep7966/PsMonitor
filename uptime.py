import wmi
import datetime,time
c = wmi.WMI()
system_data = {"UpTime": "null"}
for os in c.Win32_OperatingSystem():
    time = os.LastBootUpTime.split('.')[0]
    last_boot_time = datetime.datetime.strptime(time, '%Y%m%d%I%M%S')
    now = datetime.datetime.now()

    uptime = now - last_boot_time
    system_data["UpTime"] = str(uptime).split('.')[0]
print("System booted since ", system_data)
print("last boot time is : ", last_boot_time)