import socket
import time
import threading
from queue import Queue
import json
import pickle

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
    HEADERSIZE = 10
    while True:
        full_msg = b''
        new_msg = True
        for i, conn in enumerate(all_connections):
            while True:

                     msg = conn.recv(16)
                     if new_msg:
                         print("new msg len:", msg[:HEADERSIZE])
                         msglen = int(msg[:HEADERSIZE])
                         new_msg = False

                     print(f"full message length: {msglen}")

                     full_msg += msg

                     print(len(full_msg))

                     if len(full_msg) - HEADERSIZE == msglen:
                         print("full msg recvd")
                         print(full_msg[HEADERSIZE:])
                         print(pickle.loads(full_msg[HEADERSIZE:]))
                         new_msg = True
                         full_msg = b""


# Display current connections





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
