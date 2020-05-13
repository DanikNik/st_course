# !/usr/bin/python


# import serial.tools.list_ports
import threading
import time

import serial as pyserial


class PhyConn:
    def __init__(
            self,
            should_stop: threading.Event,
            serial: pyserial.Serial = None,
            serial_name: str = None,
    ):
        self.should_stop = should_stop
        if serial:
            self.serial = serial
        elif serial_name:
            try:
                self.serial = pyserial.Serial(
                    serial_name, 115200, timeout=0.5, write_timeout=0.5
                )
            except:
                raise ValueError("no such serial in system")
        else:
            raise ValueError("no serial provided")

    def open(self):
        self.serial.open()

    def close(self):
        self.serial.close()

    def is_open(self):
        return self.serial.is_open

    def write(self, bytestr: bytes):
        # self.serial.flushInput()
        # self.serial.flushOutput()
        # print(f'[{threading.get_ident()}] PHYCONN.WRITE CALLED')
        n = self.serial.write(bytestr)
        # print(f'[{threading.get_ident()}] PHYCONN.WRITE ENDED')
        return n

    def recv(self, size: int):
        """Function should block returning data until there is smth in buffer"""
        # print(f'[{threading.get_ident()}] PHYCONN.RECV CALLED')
        while True:
            # handle OsError (IOError) if connection breaks

            # Traceback (most recent call last):
            # File "/usr/lib/python3.7/threading.py", line 870, in start
            #   self._target(*self._args, **self._kwargs)
            # File "/home/dnikolskiy/PycharmProjects/st_course/client/client.py", line 56, in recv_func
            #   frame = conn.recv()
            # File "/home/dnikolskiy/PycharmProjects/st_course/channel/connection.py", line 49, in recv
            #   byte = int.from_bytes(self._recv(), "big")
            # File "/home/dnikolskiy/PycharmProjects/st_course/channel/connection.py", line 142, in _recv
            #   return self.conn.recv(n)
            # File "/home/dnikolskiy/PycharmProjects/st_course/physical/phyconn.py", line 45, in recv
            #   if self.serial.in_waiting > 0:
            # File "/home/dnikolskiy/PycharmProjects/st_course/venv/lib/python3.7/site-packages/serial/serialposix.py", line 467, in in_waiting # noqa
            #   s = fcntl.ioctl(self.fd, TIOCINQ, TIOCM_zero_str)
            # OSError: [Errno 5] Input/output error
            if not self.should_stop.is_set():
                if self.serial.in_waiting > 0:
                    # print(f'[{threading.get_ident()}] PHYCONN.RECV NEW DATA')
                    data = self.serial.read(size)
                    # print(f'[{threading.get_ident()}] PHYCONN.RECV ENDED')
                    return data
                time.sleep(0.1)
            else:
                raise StopIteration
        # data = self.serial.read(size)
        # return data
