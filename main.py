#!/usr/bin/env python

import sys
import threading
from textwrap import wrap

from bitstring import BitArray

from channel.connection import Connection
from physical.phyconn import PhyConn


def reading_func(c: Connection):
    while True:
        frame = c.recv()
        if frame.frametype == frame.TYPE_DATA:
            framebits = BitArray(frame.bytes())
            print('CAPTURED', wrap(framebits.bin, 8))


if __name__ == '__main__':
    print('START')
    com = input('COM: ')
    conn = Connection(PhyConn(serial_name=com))
    reader = threading.Thread(target=reading_func, args=[conn])
    reader.start()
    try:
        while True:
            data = str(input())
            if data == 'OPEN':
                conn.open()
            elif data == 'CLOSE':
                conn.close()
            elif data == 'SYN':
                conn._send_syn()
            elif data == 'FIN':
                conn._send_ack()
            else:
                conn.send(data)
    except Exception:
        reader.join(0.1)
