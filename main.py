#!/usr/bin/env python

import sys
import threading

from client.client import Client


def reading_func(c: Client):
    while True:
        frame = c.read()
        if frame.frametype == frame.TYPE_DATA:
            print(f'[{threading.get_ident()}] CAPTURED: {frame.data}')


if __name__ == '__main__':
    com1 = sys.argv[1]
    com2 = sys.argv[2]
    address = int(sys.argv[3])
    print(f'COM PORTS ARE {com1} and {com2}')
    print(f'ADDRESS IS {address}')
    client = Client(address, com1, com2)
    client.run()
    input()
    client.register()
    print('SUCCESSFULLY REGISTERED')
    reader = threading.Thread(target=reading_func, args=[client])
    try:
        reader.start()
        while True:
            dst, data = str(input()).split(' ')
            print("GOT DATA AND ADDR")
            client.send(data, dst)
    except:
        client.stop()
        reader.join()
