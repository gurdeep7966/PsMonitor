
import sys
import socket
import selectors
import types
import psutil

sel = selectors.DefaultSelector()



def cpu_utilization():
    cpu_utilization = psutil.cpu_percent(interval=5)
    return cpu_utilization

def start_connections(host, port):
    server_addr = (host, port)

    print("starting connection to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    #data = types.SimpleNamespace(
    #    connid=connid,
    #    msg_total=sum(len(m) for m in messages),
    #    recv_total=0,
    #    messages=list(messages),
    #    outb=b"",
    #)
    data=cpu_utilization()
    sel.register(sock, events, data=data)



def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    #if mask & selectors.EVENT_READ:
    #    recv_data = sock.recv(1024)  # Should be ready to read
    #    if recv_data:
    #        print("received", repr(recv_data), "from connection")
    #        data.recv_total += len(recv_data)
    #    if not recv_data or data.recv_total == data.msg_total:
    #        print("closing connection", data.connid)
    #        sel.unregister(sock)
    #        sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
        if data:
            print("sending", repr(data))
            data=str(data).encode()
            sock.send(data)  # Should be ready to write
            #data.outb = data[sent:]




host='10.42.62.156'
port=9999
start_connections(host, int(port))

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                start_connections(host, port)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()