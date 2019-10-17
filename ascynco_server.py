
from socket import *
import asyncio
import pickle
all_connections = []
all_addresses = []

async def echo_server(address, loop):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    sock.setblocking(False)
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        # client,addr=sock.accept()
        client, addr = await loop.sock_accept(sock)
        all_connections.append(client)
        all_addresses.append(address)
        print('connection from', all_addresses[0])
        loop.create_task(get_data(client, loop))

    # t=threading.Thread(Target=echo_handler,args=(client,))
    # t.start()







async def get_data(client, loop):
    while True:
        # data=client.recv(1024)
        data = await loop.sock_recv(client, 1024)
        data=pickle.loads(data)
        if not data:
            break
        # client.sendall(b'Got :'+data)
        print('recived data is ',data)
        #print('sending back '+data)
        #await loop.sock_sendall(client, b'Got :' + data.encode())
    print('connection closing ')
    client.close()
    print('Connection Closed')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(echo_server(('', 25000), loop))

