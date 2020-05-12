# !/usr/bin/python


# import serial.tools.list_ports
import time

import serial as pyserial


class PhyConn:
    def __init__(self, serial: pyserial.Serial = None, serial_name: str = None):
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
            if self.serial.in_waiting > 0:
                # print(f'[{threading.get_ident()}] PHYCONN.RECV NEW DATA')
                data = self.serial.read(size)
                # print(f'[{threading.get_ident()}] PHYCONN.RECV ENDED')
                return data
            time.sleep(0.1)
        # data = self.serial.read(size)
        # return data
