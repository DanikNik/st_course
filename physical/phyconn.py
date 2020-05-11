# !/usr/bin/python


# import serial.tools.list_ports
import threading
import serial as pyserial


# initialization and open the port

# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call


class PhyConn:
    def __init__(self, serial: pyserial.Serial, serial_name: str):
        if serial:
            self.serial = serial
        elif serial_name:
            self.serial = pyserial.Serial(serial_name, 115200, timeout=1, write_timeout=3)
        else:
            raise ValueError('no serial provided')

    def open(self):
        self.serial.open()

    def close(self):
        self.serial.close()

    def is_open(self):
        return self.serial.is_open

    def write(self, bytestr: bytes):
        return self.serial.write(bytestr)

    def recv(self, size: int):
        return self.serial.read(size)


# ser_1 = serial.Serial()
#
#
# def portinit(com):
#     # ser.port = "/dev/ttyUSB0"
#     # ser.port = "/dev/ttyS2"
#     ser_1.baudrate = com[2]
#     ser_1.bytesize = serial.EIGHTBITS  # number of bits per bytes
#     ser_1.parity = serial.PARITY_NONE  # set parity check: no parity
#     ser_1.stopbits = serial.STOPBITS_ONE  # number of stop bits
#     # ser.timeout = None          #block read
#     ser_1.timeout = com[3]  # non-block read
#     # ser.timeout = 2              #timeout block read
#     # ser_2.xonxoff = False  # disable software flow control
#     # ser_2.rtscts = False  # disable hardware (RTS/CTS) flow control
#     # ser_2.dsrdtr = False  # disable hardware (DSR/DTR) flow control
#     ser_1.writeTimeout = com[4]  # timeout for write
#     try:
#         ser_1.port = com[0]
#         ser_1.open()
#         ser_1.close()
#     except:
#         ser_1.port = com[1]
#
#
# def ser_close():
#     try:
#         ser_1.close()
#     except Exception as e:
#         print("error close serial port: " + str(e))
#         exit()
#
#
# priem = 0
# read_delay = 0.5
# frames = []
#
#
# def ser_open():
#     try:
#         ser_1.open()
#     except Exception as e:
#         print("error open serial port: " + str(e))
#         exit()
#
#
# def ser_write(binary_message):
#     ser_1.flushInput()  # flush input buffer, discarding all its contents
#     ser_1.flushOutput()  # flush output buffer, aborting current output
#     if ser_1.isOpen():
#         i = 0
#         for frame in binary_message:
#             try:
#                 ser_1.write(frame)
#                 # print('WRITE', i, datetime.datetime.now())
#                 ser_1.flush()
#                 # print("write data: Hello")
#                 # time.sleep(0.0005)  # give the serial port sometime to receive the data
#                 i = i + 1
#             except Exception as e1:
#                 print("error communicating write...: " + str(e1))
#     else:
#         print("cannot open serial port ")
#
#
# def ser_read(ser=ser_1):
#     global priem
#     global frames
#     global read_delay
#     if ser.isOpen():
#         if ser.in_waiting == 0 and priem == 1:
#             priem = 0
#             read_delay = 0.5
#             channel.receive(frames)
#             frames = []
#         while ser.in_waiting > 0:
#             if priem == 0:
#                 priem = 1
#                 read_delay = 0.0001
#             print('in_waiting', ser_1.in_waiting)
#             while ser.in_waiting >= 238:
#                 response = ser.read(238)
#                 # print('READ', ser_2.in_waiting, datetime.datetime.now())
#                 frames.append(response)
#     else:
#         print("cannot open serial port ")
#         return 1
#     threading.Timer(read_delay, ser_read).start()
